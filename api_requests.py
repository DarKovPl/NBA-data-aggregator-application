import requests


class ApiRequests:

    def __init__(self):
        self.req_get = requests.get

    def get_all_teams(self):
        response = self.req_get('https://www.balldontlie.io/api/v1/teams')
        return response

