from threading import Event
import sys
import requests


def connection_err_decorator(func, retry=3):
    def retry_wrapper(*args, **kwargs):
        counter = 0
        while counter < retry:
            try:
                return func(*args, **kwargs)
            except requests.ConnectionError:
                sys.stdout.writelines('Connection problem. Let me try again.\n')
                counter += 1
                Event().wait(2)
                if counter == 3:
                    sys.stdout.writelines("I can't connect to the https://www.balldontlie.io webpage.\n")
                    exit()

    return retry_wrapper


class ApiRequests:

    def __init__(self):
        super(ApiRequests, self).__init__()
        self.req_get = requests.get

    @connection_err_decorator
    def get_all_teams(self) -> requests.Response:
        response = self.req_get('https://www.balldontlie.io/api/v1/teams')
        return response

    @connection_err_decorator
    def get_meta_players_stats_total_pages(self) -> int:
        response = self.req_get('https://www.balldontlie.io/api/v1/players?page=0&per_page=100')
        total_pages = response.json()['meta']['total_pages']
        return total_pages

    @connection_err_decorator
    def get_player_stats(self) -> str:
        for k in range(1, self.get_meta_players_stats_total_pages() + 1):
            response = self.req_get(f'https://www.balldontlie.io/api/v1/players?page={k}&per_page=100')
            yield response.content.decode('utf-8')

    @connection_err_decorator
    def get_meta_teams_stats_total_pages(self, year_season) -> int:
        response = self.req_get(
            f'https://www.balldontlie.io/api/v1/games?page=1&per_page=100&seasons[]={year_season}')
        total_pages = response.json()['meta']['total_pages']
        return total_pages

    @connection_err_decorator
    def get_teams_stats(self, total_pages, year_season):
        for k in range(1, total_pages + 1):
            response = self.req_get(
                f'https://www.balldontlie.io/api/v1/games?page={k}&per_page=100&seasons[]={year_season}'
            )
            yield response.json()['data']
