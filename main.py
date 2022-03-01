from api_requests import ApiRequests
from grouped_teams import GroupedTeams
from argparse_commands import ArgparseCommands


def main():
    ArgparseCommands()
    resp_all_teams = ApiRequests().get_all_teams()
    grouped = GroupedTeams(resp_all_teams)
    grouped.get_unique_divisions()
    grouped.show_results(grouped.create_grouped_teams())



if __name__ == '__main__':
    main()
