import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from database.orm.models.TableNames import tables
from database.orm.models.Models import Base


class ORMClient(object):
    connection = None
    session = None
    engine = None

    username: str = None
    password: str = None
    database: str = None
    hostname: str = None
    port: int = None

    def __init__(self, username: str, password: str, database: str, port: int = 3306) -> None:
        self.username = username
        self.password = password
        self.database = database
        self.port = port

        self.hostname = "127.0.0.1"

    def __del__(self) -> None:
        self.disconnect()

    def connect(self, database_created: bool = True) -> None:
        database = self.database if database_created else ''

        self.engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.username}:{self.password}@{self.hostname}:{self.port}/{database}',
            encoding="utf8"
        )

        self.connection = self.engine.connect()
        self.session = sessionmaker(bind=self.connection.engine,
                                    autocommit=False,
                                    expire_on_commit=False
                                    )()

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def execute_query(self, query: str, fetch: bool = False):
        result = self.connection.execute(query)
        if fetch:
            return result

    def recreate_database(self):
        self.connect(database_created=False)
        self.execute_query(f'DROP DATABASE IF EXISTS {self.database}', fetch=False)
        self.execute_query(f'CREATE DATABASE {self.database}', fetch=False)
        self.disconnect()

    def create_tables(self):
        for table in dir(tables):
            if not inspect(self.engine).has_table(table):
                Base.metadata.tables[table].create(self.engine)
