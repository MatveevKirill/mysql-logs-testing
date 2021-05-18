import pytest

from sqlalchemy.sql import func

from database.orm.models.Models import CountQueriesByType
from tests.base_test import BaseTestCase


class TestCountQueriesByType(BaseTestCase):

    def prepare(self):
        self.count_queries = self.parser.count_queries()

        self.count_queries_by_type = self.parser.count_queries_by_type()

        for key in self.count_queries_by_type.keys():
            row = CountQueriesByType(
                type=key,
                count=self.count_queries_by_type[key]
            )
            self.orm_client.session.add(row)

        self.orm_client.session.commit()

    @pytest.mark.MySQL
    def test(self):
        summa_queries = self.orm_client.session.query(func.sum(CountQueriesByType.count).label('summa')).first()

        # Количество строк в запросе всегда равно количество ключей, полученных через парсер.
        assert len(self.orm_client.session.query(CountQueriesByType).all()) == \
               len(list(self.count_queries_by_type.keys()))

        # Проверяем общую сумму запросов.
        assert summa_queries.summa == self.count_queries

        # Проверяем упорядоченность запросов в базе данных.
        i = 1
        for query in self.count_queries_by_type:
            current_db_element = self.orm_client.session.query(CountQueriesByType).filter_by(id=i).first()

            assert query == current_db_element.type
            assert self.count_queries_by_type[query] == current_db_element.count

            i += 1
