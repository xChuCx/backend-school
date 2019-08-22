# services/citizens/project/api/citizens.py
from flask import Blueprint, request
from flask_restful import Resource, Api

# couchbase
from project.db.couchbase import connect_db, log_error
from couchbase.exceptions import CouchbaseError
from couchbase.n1ql import N1QLQuery

from project.common.utils import prep_params, calculateAge, response
from project.common.constants import COUCH_ERROR, WRONG_IMPORT, WRONG_CITIZEN
from project.schemas.validation import schema_validate
import numpy as np

citizens_blueprint = Blueprint('citizens', __name__)
api = Api(citizens_blueprint)
db = connect_db()


class DataImports(Resource):
    def post(self):
        post_data = request.get_json()
        er = schema_validate(post_data, 'import_schema')
        if er:
            return response(400, er)
        try:
            import_id = db.counter('import_id', delta=5, initial=1)
            # !!! если каунтер вернет 1 сделать индексы в бд
            post_data = post_data.pop('citizens')
            db.insert(str(import_id), post_data)
            response_object = response(201, {
                'data': {
                    'import_id': str(import_id)
                }
            })
            return response_object
        except CouchbaseError as e:
            log_error(e)
            return response(400, COUCH_ERROR)


class GetCitizens(Resource):
    def get(self, import_id):
        try:
            citizens = db.get(import_id).value
            if not citizens:
                return response(400, WRONG_IMPORT)
            citizens['data'] = citizens.pop('citizens')
            response_object = response(200, citizens)
            return response_object
        except CouchbaseError as e:
            log_error(e)
            return response(400, COUCH_ERROR)


class PatchCitizen(Resource):
    def patch(self, import_id, citizen_id):
        citizen_id = int(citizen_id)
        patch_data = request.get_json()
        # validate
        er = schema_validate(patch_data, 'patch_schema')
        if er:
            return response(400,er)
        # если изменяются связи(relatives)
        if "relatives" in patch_data:
            # найти всех граждан, для которых нужно изменить связи(relatives)
            query = 'SELECT FIRST v.relatives FOR v IN citizens WHEN v.citizen_id = $1 END as relatives FROM ' \
                    'analitycDB WHERE META().id = $2'
            try:
                relatives = db.n1ql_query(N1QLQuery(query, citizen_id, import_id)).get_single_result()
            except CouchbaseError as e:
                log_error(e)
                return response(400, COUCH_ERROR)
            if not relatives:
                return response(400, WRONG_CITIZEN)
            new = patch_data["relatives"]
            break_relatives = [x for x in relatives["relatives"] if x not in new]
            if break_relatives:
                # убрать связи(relatives)
                upd_query = 'UPDATE analitycDB SET i.relatives = ARRAY_REMOVE(i.relatives, $1)  FOR i IN citizens ' \
                            'WHEN i.citizen_id in $2 END WHERE META().id = $3'
                try:
                    db.n1ql_query(N1QLQuery(upd_query, citizen_id, break_relatives, import_id)).execute()
                except CouchbaseError as e:
                    log_error(e)
                    return response(400, COUCH_ERROR)
            add_relatives = [x for x in new if x not in relatives["relatives"]]
            if add_relatives:
                # добавить связи(relatives)
                upd_query = 'UPDATE analitycDB SET i.relatives = ARRAY_APPEND(i.relatives, $1)  FOR i IN citizens ' \
                            'WHEN i.citizen_id in $2 END WHERE META().id = $3'
                try:
                    db.n1ql_query(N1QLQuery(upd_query, citizen_id, add_relatives, import_id)).execute()
                except CouchbaseError as e:
                    log_error(e)
                    return response(400, COUCH_ERROR)

        # dynamic query for update
        values = ', '.join(
            'i.' + str(i) + ' = ' + prep_params(patch_data.get(i)) + 'FOR i IN citizens WHEN i.citizen_id=$1 END' for i
            in patch_data)
        query = 'UPDATE analitycDB SET %s WHERE META().id=$2 RETURNING ' \
                'FIRST v FOR v IN citizens WHEN v.citizen_id =$1 END as data' % values
        try:
            data = db.n1ql_query(N1QLQuery(query, citizen_id, import_id)).get_single_result()
        except CouchbaseError as e:
            log_error(e)
            return response(400, COUCH_ERROR)
        if not data:
            return response(400, WRONG_CITIZEN)
        response_object = response(200, data)
        return response_object


class PercentileAge(Resource):
    def get(self, import_id):
        query = 'SELECT c.town, ARRAY_AGG(c.birth_date) as ages FROM analitycDB USE KEYS $1 unnest citizens c group ' \
                'by c.town'
        data = []
        try:
            row_iter = db.n1ql_query(N1QLQuery(query, import_id))
            for row in row_iter: data.append(row)
        except CouchbaseError as e:
            log_error(e)
            return response(400, COUCH_ERROR)
        if not data:
            return response(400, WRONG_IMPORT)

        # !!! interpolation='linear'
        stats = []
        for i in data:
            i['ages'] = [calculateAge(x) for x in i['ages']]
            stat = {
                "town": i["town"],
                "p50": np.percentile(i['ages'], 50),
                "p75": np.percentile(i['ages'], 75),
                "p99": np.percentile(i['ages'], 99)
            }
            stats.append(stat)

        response_object = response(200, {
            'data': stats
        })
        return response_object


class Birthdays(Resource):
    def get(self, import_id):
        query = "select f.month, ARRAY_AGG({f.citizen_id, f.presents}) as data from (select c.id as citizen_id, " \
                "SUM(c.count) as presents, d.month as month from (select (select id as id, count(*) as count from " \
                "c.relatives id group by id) as counts, DATE_PART_STR((SUBSTR(c.birth_date,6,4)||'-'||SUBSTR(" \
                "c.birth_date,3,2)||'-'||SUBSTR(c.birth_date,0,2)),'month') as month from analitycDB USE KEYS $1 " \
                "unnest citizens c) d unnest counts c group by c.id, d.month) f group by f.month "
        data = []
        try:
            row_iter = db.n1ql_query(N1QLQuery(query, import_id))
            for row in row_iter: data.append(row)
        except CouchbaseError as e:
            log_error(e)
            return response(400, COUCH_ERROR)

        stats = {}
        for month in data:
            stats[str(month["month"])] = month["data"]

        data = {}
        for i in range(1, 13):
            if str(i) not in stats:
                data[str(i)] = []
            else:
                data[str(i)] = stats[str(i)]

        response_object = response(200, {
            "data": data
        })
        return response_object


api.add_resource(DataImports, '/imports')
api.add_resource(GetCitizens, '/imports/<import_id>/citizens')
api.add_resource(PatchCitizen, '/imports/<import_id>/citizens/<citizen_id>')
api.add_resource(Birthdays, '/imports/<import_id>/citizens/birthdays')
api.add_resource(PercentileAge, '/imports/<import_id>/towns/stat/percentile/age')
