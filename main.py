import argparse
from api_requests import ApiRequests
from grouped_teams import GroupedTeams
from folder_structure import FolderStructure
from players_stats import PlayerStats
from teams_stats import TeamStats


def grouped_teams():
    resp_all_teams = ApiRequests().get_all_teams()
    grouped = GroupedTeams(resp_all_teams)
    grouped.get_unique_divisions()
    grouped.show_results(grouped.create_grouped_teams())


def players_stats(name):
    # import wdb; wdb.set_trace()
    player_stats = PlayerStats()
    # player_stats.save_player_stats_locally()
    player_stats.get_players_stats_columns()
    player_stats.view_player_stats_by_name(name)


def teams_stats(year_season):
    season_teams_stats = TeamStats()
    total_pages = season_teams_stats.get_meta_teams_stats_total_pages(year_season)

    season_teams_stats.delete_existing_csv_files()
    season_teams_stats.delete_teams_stats_json_file()

    season_teams_stats.get_all_season_teams_stats(total_pages, year_season)
    season_teams_stats.create_teams_names_set()
    season_teams_stats.create_list_for_teams_statistic()
    season_teams_stats.count_statistics_for_teams()

    season_teams_stats.write_teams_stats_to_csv()
    season_teams_stats.write_teams_stats_to_json()
    season_teams_stats.write_teams_stats_to_sqlite_db()
    season_teams_stats.show_teams_stats_on_console()

if __name__ == '__main__':
    # FolderStructure().create_folder_structure()
    # FolderStructure().delete_existing_files()

    # parser = argparse.ArgumentParser()
    # subparsers = parser.add_subparsers(dest='command', required=True)
    #
    # grouped_teams_parser = subparsers.add_parser('grouped_teams', help='Grouped')
    #
    # players_stats_parser = subparsers.add_parser('players_stats', help='Show help')
    # players_stats_parser.add_argument('--name', action='store', type=str, help='Name')
    #
    # args = parser.parse_args()
    #
    # if args.command == 'grouped_teams':
    #     grouped_teams()
    #
    # if args.command == 'players_stats' and args.name is not None:
    #     players_stats(args.name)
    teams_stats(2017)
