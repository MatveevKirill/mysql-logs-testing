class _TableNames(object):
    COUNT_QUERIES = 'count_queries'
    COUNT_QUERIES_BY_TYPE = 'count_queries_by_type'
    TOP_FREQUENT_REQUESTS = 'top_frequent_requests'
    TOP_BIGGEST_QUERIES_WITH_CLIENT_ERROR = 'top_biggest_queries_with_client_error'
    TOP_NUMBER_OF_REQUESTS_WITH_SERVER_ERROR = 'top_number_of_requests_with_server_error'

    def __dir__(self) -> list:
        return [
            self.COUNT_QUERIES,
            self.COUNT_QUERIES_BY_TYPE,
            self.TOP_FREQUENT_REQUESTS,
            self.TOP_BIGGEST_QUERIES_WITH_CLIENT_ERROR,
            self.TOP_NUMBER_OF_REQUESTS_WITH_SERVER_ERROR
        ]


tables = _TableNames()
