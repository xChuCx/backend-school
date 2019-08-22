# services/citizens/project/common/utils.py
import datetime
from flask import jsonify


# обвязка строкых значений для динамических запросов
def prep_params(value):
    if isinstance(value, str):
        value = '"' + value + '"'
    else:
        value = str(value)
    return value


# определение возраста
def calculateAge(born):
    date_format = '%d.%m.%Y'
    born = datetime.datetime.strptime(born, date_format).date()
    today = datetime.date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year,
                                month=born.month + 1, day=1)

    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year


# формирование ответа
def response(code=400, body='Bad Request'):
    response_object = jsonify(body)
    response_object.status_code = code
    return response_object
