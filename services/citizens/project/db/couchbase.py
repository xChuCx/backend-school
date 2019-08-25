# services/citizens/project/db/couchbase.py
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator


# TO_DO логин пароль из переменой окружения!
def connect_db():
    cluster = Cluster('couchbase://couch')
    authenticator = PasswordAuthenticator('APP', 'APPpwd')
    cluster.authenticate(authenticator)
    bucket = cluster.open_bucket('analitycDB')
    return bucket


def log_error(e):
    ok, fail = e.split_results()
    for k, v in fail.items():
        print('Key {0} failed with error code {1}'.format(k, v.rc), flush=True)
    for k, v in ok.items():
        print('Retrieved {0} with value {1}'.format(k, v.value), flush=True)