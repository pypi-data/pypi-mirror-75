import os

import sqlalchemy as sa
import pytest

from agreement_api.app import app as flask_app, DB
from agreement_api.models import Agreement
from pytest_postgresql.factories import init_postgresql_database, drop_postgresql_database

from agreement_api.models import User

DB_OPTS = {"user": "postgres", "host": "localhost", "port": 5432, "database": "test_2", "password": "postgres"}
PG_USER = "postgres"
PG_PASSWORD = "postgres"
PG_PORT = 5432
SQLALCHEMY_DATABASE_URI = "postgresql://{username}:{password}" \
                          "@localhost:{port}/flask_testing".format(username=PG_USER,
                                                                   password=PG_PASSWORD,
                                                                   port=PG_PORT)
"""
https://github.com/jeancochrane/pytest-flask-sqlalchemy/blob/master/tests/_conftest.py
"""

# Retrieve a database connection string from the shell environment
try:
    DB_CONN = os.environ['TEST_DATABASE_URL']
except KeyError:
    raise KeyError('TEST_DATABASE_URL not found. You must export a database ' +
                   'connection string to the environmental variable ' +
                   'TEST_DATABASE_URL in order to run tests.')
else:
    DB_OPTS = sa.engine.url.make_url(DB_CONN).translate_connect_args()

pytest_plugins = ['pytest-flask-sqlalchemy']


@pytest.fixture(scope='session')
def database(request):
    '''
    Create a Postgres database for the tests, and drop it when the tests are done.
    '''
    pg_host = DB_OPTS.get("host")
    pg_port = DB_OPTS.get("port")
    pg_user = DB_OPTS.get("username")
    pg_db = DB_OPTS["database"]

    init_postgresql_database(pg_user, pg_host, pg_port, pg_db, password="postgres")

    @request.addfinalizer
    def drop_database():
        drop_postgresql_database(pg_user, pg_host, pg_port, pg_db, 9.6, password="postgres")


SQLALCHEMY_DATABASE = None


@pytest.fixture(scope='session')
def app(database):
    '''
    Create a Flask app context for the tests.
    '''
    # _app.config.from_object('config.TestConfig')
    # flask_app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONN

    yield flask_app


@pytest.fixture(scope='session')
def _db(app):
    """
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    """
    DB.create_all()
    return DB


@pytest.fixture(scope="function")
def agreement_object(db_session):
    user = User(email='testing@mail.com')
    DB.session.add(user)

    expected = {'agreement_status': False, 'user_id': user.id}
    agreement = Agreement(**expected)
    DB.session.add(agreement)
    DB.session.commit()

    yield {"agreement": agreement.id, "user": user.id}
