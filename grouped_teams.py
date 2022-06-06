import sys
import itertools


class GroupedTeams:
    def __init__(self, response):

        self.response = response
        self.divisions = []
        self.unique_divisions = set()

    def get_unique_divisions(self) -> set:

        for i in self.response.json()["data"]:
            self.divisions.append(i["division"])
            self.unique_divisions = set(self.divisions)
        return self.unique_divisions

    def create_grouped_teams(self) -> dict:
        groups = {key: [] for key in self.unique_divisions}

        for uniq_div, data in itertools.product(
            self.unique_divisions, self.response.json()["data"]
        ):
            if uniq_div == data["division"]:
                groups[uniq_div].append(f"{data['full_name']} ({data['abbreviation']})")
        return groups

    @staticmethod
    def show_results(groups):
        new_line_tab = "\n\t"
        for k, v in groups.items():
            sys.stdout.writelines(f"{k}\n\t{new_line_tab.join(v)}\n")
