import os
import pytest
from _pytest.config import Config

from _pytest.fixtures import Parser, FixtureRequest

from database.orm.client import ORMClient


def pytest_addoption(parser: Parser) -> None:
    parser.addoption('--username', default="root")
    parser.addoption('--password', default="pass")
    parser.addoption('--database', default="TEST_SQL")
    parser.addoption('--port', default=3306)


def pytest_configure(config: Config) -> None:
    if not hasattr(config, 'workerinput'):
        client = ORMClient(username='root', password='pass', database='TEST_SQL')

        client.recreate_database()
        client.connect()
        client.create_tables()
        client.disconnect()


@pytest.fixture(scope="session")
def abs_path() -> str:
    return os.path.abspath(os.path.join(__file__, os.pardir))


@pytest.fixture(scope="session")
def orm_client(db_configuration: dict) -> ORMClient:
    client = ORMClient(username=db_configuration['username'],
                       password=db_configuration['password'],
                       database=db_configuration['database'],
                       port=db_configuration['port'])

    client.connect()
    yield client
    client.disconnect()


@pytest.fixture(scope="session")
def db_configuration(request: FixtureRequest) -> dict:
    username = request.config.getoption('--username')
    password = request.config.getoption('--password')
    database = request.config.getoption('--database')
    port = int(request.config.getoption('--port'))

    return {
        'username': username,
        'password': password,
        'database': database,
        'port': port
    }
