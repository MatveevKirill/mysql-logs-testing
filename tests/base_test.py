import os
import pytest

from database.orm.client import ORMClient
from logparser.pyparser import LogParser


class BaseTestCase(object):
    orm_client: ORMClient = None
    parser: LogParser = None

    def prepare(self):
        pass

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, abs_path: str, orm_client: ORMClient) -> None:
        self.parser = LogParser(os.path.join(abs_path, 'logs', 'access.log'))
        self.orm_client = orm_client

        self.prepare()

        yield

        del self.parser
