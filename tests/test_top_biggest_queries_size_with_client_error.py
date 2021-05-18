import pytest

from database.orm.models.Models import TopBiggestQueriesWithClientError
from tests.base_test import BaseTestCase


class TestTopBiggestQueriesWithClientError(BaseTestCase):

    def prepare(self):
        self.top_biggest_queries_with_client_error = self.parser.top_biggest_queries_size_with_client_error()

        for request in list(self.top_biggest_queries_with_client_error.keys())[::-1]:
            row = TopBiggestQueriesWithClientError(
                url=request,
                status_code=self.top_biggest_queries_with_client_error[request]['status_code'],
                size=self.top_biggest_queries_with_client_error[request]['size_query'],
                ip_address=self.top_biggest_queries_with_client_error[request]['ip_address']
            )
            self.orm_client.session.add(row)

        self.orm_client.session.commit()

    @pytest.mark.MySQL
    def test(self):

        # Количество строк в запросе всегда равно 5.
        assert len(self.orm_client.session.query(TopBiggestQueriesWithClientError).all()) == 5

        # Проверяем запросы в БД и полученные в парсере.
        i = 1
        for url in list(self.top_biggest_queries_with_client_error.keys())[::-1]:
            current_db_element = self.orm_client.session.query(TopBiggestQueriesWithClientError).filter_by(id=i).first()

            assert current_db_element.url == url
            assert current_db_element.status_code == int(self.top_biggest_queries_with_client_error[url]['status_code'])
            assert current_db_element.size == self.top_biggest_queries_with_client_error[url]['size_query']
            assert current_db_element.ip_address == self.top_biggest_queries_with_client_error[url]['ip_address']

            i += 1
