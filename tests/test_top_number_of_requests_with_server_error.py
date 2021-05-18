import pytest

from database.orm.models.Models import TopNumberOfRequestsWithServerError
from tests.base_test import BaseTestCase


class TestTopNumberOfRequestsWithServerError(BaseTestCase):

    def prepare(self):
        self.top_number_of_requests_with_server_error = self.parser.top_number_of_requests_with_server_error()

        for request in list(self.top_number_of_requests_with_server_error.keys())[::-1]:
            row = TopNumberOfRequestsWithServerError(
                ip_address=request,
                count=self.top_number_of_requests_with_server_error[request]
            )
            self.orm_client.session.add(row)

        self.orm_client.session.commit()

    @pytest.mark.MySQL
    def test(self):

        # Количество строк в запросе всегда равно 5.
        assert len(self.orm_client.session.query(TopNumberOfRequestsWithServerError).all()) == 5

        # Проверяем запросы в БД и полученные в парсере.
        i = 1
        for ip_address in list(self.top_number_of_requests_with_server_error.keys())[::-1]:
            current_db_element = self.orm_client.session.query(TopNumberOfRequestsWithServerError).filter_by(id=i).first()

            assert current_db_element.ip_address == ip_address
            assert current_db_element.count == self.top_number_of_requests_with_server_error[ip_address]

            i += 1
