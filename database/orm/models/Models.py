from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from database.orm.models.TableNames import tables

Base = declarative_base()


class CountQueries(Base):
    __tablename__ = tables.COUNT_QUERIES
    __tableargs__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    count_queries = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<CountQueriesModel(' \
               f'id={self.id} ' \
               f'count_queries={self.count_queries}' \
               f') />'


class CountQueriesByType(Base):
    __tablename__ = tables.COUNT_QUERIES_BY_TYPE
    __tableargs__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(500), nullable=False)
    count = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<CountQueriesByType(' \
               f'id={self.id} ' \
               f'type={self.type} ' \
               f'count={self.count}' \
               f') />'


class TopFrequentRequests(Base):
    __tablename__ = tables.TOP_FREQUENT_REQUESTS
    __tableargs__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), nullable=False)
    count_queries = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<TopFrequentRequests(' \
               f'id={self.id} ' \
               f'url={self.url} ' \
               f'count={self.count}' \
               f') />'


class TopBiggestQueriesWithClientError(Base):
    __tablename__ = tables.TOP_BIGGEST_QUERIES_WITH_CLIENT_ERROR
    __tableargs__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), nullable=False)
    status_code = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    ip_address = Column(String(15), nullable=False)

    def __repr__(self):
        return f'<TopBiggestQueriesWithClientError(' \
               f'id={self.id} ' \
               f'url={self.url} ' \
               f'status_code={self.status_code}' \
               f'size={self.size}' \
               f'ip_address={self.ip_address}' \
               f') />'


class TopNumberOfRequestsWithServerError(Base):
    __tablename__ = tables.TOP_NUMBER_OF_REQUESTS_WITH_SERVER_ERROR
    __tableargs__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String(14), nullable=False)
    count = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<TopBiggestQueriesWithClientError(' \
               f'id={self.id} ' \
               f'ip_address={self.ip_address} ' \
               f'count={self.count}' \
               f') />'
