import pytest

from database.orm.models.Models import CountQueries
from tests.base_test import BaseTestCase


class TestCountQueries(BaseTestCase):

    def prepare(self):
        self.count_queries = self.parser.count_queries()

        row = CountQueries(
            count_queries=self.count_queries
        )

        self.orm_client.session.add(row)
        self.orm_client.session.commit()

    @pytest.mark.MySQL
    def test(self):
        count_queries = self.orm_client.session.query(CountQueries).filter_by(id=1)

        # Количество строк должно быть равно всегда 1.
        assert len(count_queries.all()) == 1

        # Проверяем количество запросов в БД и полученные через парсер.
        assert count_queries.first().count_queries == self.count_queries
