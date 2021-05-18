import re


class LogParser(object):
    logs: list = []

    def __init__(self, log_file: str) -> None:
        self.logs.clear()

        with open(log_file, 'rt') as f:
            for log_line in f.readlines():
                pattern = re.compile(r"^((\d{1,3}.\d{1,3}.\d{1,3}\.\d{1,3}) - - (\[\d{1,31}/.+"
                                     r"/\d{4}:\d{2}:\d{2}:\d{2} \+\d+]) \"(.+) (.+)"
                                     r"HTTP/1\.(0|1)\" (\d{3}) .* \"(.*)\" \"(.*)\" \"(.*)\")$")

                match = pattern.match(log_line.split('\n')[0])

                # Весь запрос.
                query = match.groups()[0]

                # IP адрес.
                ip_address = match.groups()[1]

                # Дата создания лога.
                date_create_log = match.groups()[2]

                # Метод.
                method = match.groups()[3].replace(' ', '')

                # Ссылка
                url = match.groups()[4]

                # Версия HTTP
                http_version = f'HTTP/1.{match.groups()[5]}'

                # Статус ответа
                status_code = match.groups()[6]

                self.logs.append({
                    'query': query,
                    'ip_address': ip_address,
                    'date_create_log': date_create_log,
                    'method': method,
                    'url': url,
                    'http_version': http_version,
                    'status_code': status_code
                })

    def __del__(self):
        self.logs.clear()

    @staticmethod
    def sort_dict(dictionary: dict, child: str = None, count_queries: int = 5) -> dict:
        list_d = list(dictionary.items())

        if child is None:
            list_d.sort(key=lambda x: x[1])
        else:
            list_d.sort(key=lambda x: x[1][child])

        size_list_d = len(list_d)
        return dict(list_d[size_list_d - count_queries::])

    def count_queries(self) -> int:
        return len(self.logs)

    def count_queries_by_type(self) -> dict:
        types = {}

        for log in self.logs:
            if log['method'] not in types:
                types[log['method']] = 1
            else:
                types[log['method']] += 1

        return types

    def top_frequent_requests(self, count_queries: int = 10) -> dict:
        count_queries_dict = {}

        for log in self.logs:
            if log['url'] not in count_queries_dict:
                count_queries_dict[log['url']] = 1
            else:
                count_queries_dict[log['url']] += 1

        return self.sort_dict(count_queries_dict, count_queries=count_queries)

    def top_biggest_queries_size_with_client_error(self, count_queries: int = 5) -> dict:
        queries = {}

        for log in self.logs:
            if re.match(r'^(4[0-9]{2})$', log['status_code']) is not None:
                if log['url'] not in queries:
                    queries[log['url']] = {
                        'count': 1,
                        'status_code': log['status_code'],
                        'size_query': len(log['url']),
                        'ip_address': log['ip_address']
                    }
                else:
                    queries[log['url']]['count'] += 1

        return self.sort_dict(queries, child='size_query', count_queries=count_queries)

    def top_number_of_requests_with_server_error(self, count_queries: int = 5) -> dict:
        ip_addresses = {}

        for log in self.logs:
            if re.match(r'^(5[0-9]{2})$', log['status_code']) is not None:
                if log['ip_address'] not in ip_addresses:
                    ip_addresses[log['ip_address']] = 1
                else:
                    ip_addresses[log['ip_address']] += 1

        return self.sort_dict(ip_addresses, count_queries=count_queries)
