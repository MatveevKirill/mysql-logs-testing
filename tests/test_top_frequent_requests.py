import pytest

from database.orm.models.Models import TopFrequentRequests
from tests.base_test import BaseTestCase


class TestTopFrequentRequests(BaseTestCase):

    def prepare(self):
        self.top_frequent_requests = self.parser.top_frequent_requests()

        for request in list(self.top_frequent_requests.keys())[::-1]:
            row = TopFrequentRequests(
                url=request,
                count_queries=self.top_frequent_requests[request]
            )
            self.orm_client.session.add(row)

        self.orm_client.session.commit()

    @pytest.mark.MySQL
    def test(self):

        # Количество строк в запросе всегда равно 10.
        assert len(self.orm_client.session.query(TopFrequentRequests).all()) == 10

        i = 1
        for element in list(self.top_frequent_requests)[::-1]:
            current_db_element = self.orm_client.session.query(TopFrequentRequests).filter_by(id=i).first()

            assert current_db_element.url == element
            assert current_db_element.count_queries == self.top_frequent_requests[element]

            i += 1
