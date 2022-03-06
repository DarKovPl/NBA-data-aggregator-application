import json
import sys
from sqlalchemy.orm import sessionmaker
from marshmallow import Schema, fields
import pandas as pd
import api_requests
import folder_structure


class VisitorAndHomeTeam:
    def __init__(self, abbreviation, full_name):
        self.abbreviation = abbreviation
        self.full_name = full_name


class VisitorAndHomeTeamSchema(Schema):
    abbreviation = fields.String()
    full_name = fields.String()


class AllGamesInSeasonData:

    def __init__(self, home_team_score, visitor_team_score, home_team, visitor_team):
        self.home_team_score = home_team_score
        self.visitor_team_score = visitor_team_score
        self.home_team = home_team
        self.visitor_team = visitor_team


class AllGamesInSeasonDataSchema(Schema):
    home_team_score = fields.Integer()
    visitor_team_score = fields.Integer()
    home_team = fields.Nested(VisitorAndHomeTeamSchema)
    visitor_team = fields.Nested(VisitorAndHomeTeamSchema)


class TeamStats(api_requests.ApiRequests, folder_structure.FolderStructure, AllGamesInSeasonDataSchema):

    def __init__(self):
        super(TeamStats, self).__init__()
        self.season = list()
        self.teams_name_set = set()
        self.result_list = list()
        self.dict_list_with_no_key = list()

    def get_all_season_teams_stats(self, total_pages, year_season):
        for i in self.get_teams_stats(total_pages, year_season):
            self.season += AllGamesInSeasonDataSchema(many=True).dump(i)

    def create_teams_names_set(self):
        teams_name_list = []
        for z in self.season:
            teams_name_list.append(z['visitor_team']['full_name'] + f" ({z['visitor_team']['abbreviation']})")
            teams_name_list.append(z['home_team']['full_name'] + f" ({z['home_team']['abbreviation']})")
        self.teams_name_set = set(teams_name_list)

    def create_list_for_teams_statistic(self):
        for name in self.teams_name_set:
            result_dict = {'Team_name': name, 'Won_games_as_home_team': 0, 'Won_games_as_visitor_team': 0,
                           'Lost_games_as_home_team': 0, 'Lost_games_as_visitor_team': 0}
            self.result_list.append({name.replace(' ', '_')[:-6]: result_dict})

    def count_statistics_for_teams(self):

        for match in self.season:
            visitor_team_name = match['visitor_team']['full_name'].replace(' ', '_')
            home_team_name = match['home_team']['full_name'].replace(' ', '_')

            for team in self.result_list:
                try:
                    if team[visitor_team_name]:
                        if match['visitor_team_score'] > match['home_team_score']:
                            team[visitor_team_name]['Won_games_as_visitor_team'] += 1
                        else:
                            team[visitor_team_name]['Lost_games_as_visitor_team'] += 1
                except KeyError:
                    pass

                try:
                    if team[home_team_name]:
                        if match['visitor_team_score'] > match['home_team_score']:
                            team[home_team_name]['Lost_games_as_home_team'] += 1
                        else:
                            team[home_team_name]['Won_games_as_home_team'] += 1

                except KeyError:
                    continue

        self.dict_list_with_no_key = [v for k in self.result_list for v in list(k.values())]

    def write_teams_stats_to_csv(self):
        for k in self.result_list:
            df = pd.DataFrame.from_dict(k, orient='index')
            if self.check_teams_stats_csv_file():
                df.to_csv(self.teams_stats_csv_file, header=False, mode='a', index=False)
            else:
                df.to_csv(self.teams_stats_csv_file, header=True, index=False)

    def write_teams_stats_to_json(self):
        with open(self.teams_stats_json_file, 'w') as f:
            json.dump(self.dict_list_with_no_key, f)

    def write_teams_stats_to_sqlite_db(self):
        obj_list = []
        for record in self.dict_list_with_no_key:
            rec_low = {(k.lower(), v) for k, v in record.items()}

            data_obj = folder_structure.TeamsStats(**dict(rec_low))
            obj_list.append(data_obj)

            Session = sessionmaker(bind=folder_structure.engine)
            session = Session()
            session.add_all(obj_list)
            session.commit()
            session.close()

    def show_teams_stats_on_console(self):
        for i in self.dict_list_with_no_key:
            k_v_tup = [(k, v) for k, v in i.items()]
            sys.stdout.writelines(
                f"{k_v_tup[0][1]}\n\t"
                f"{k_v_tup[1][0]}: {k_v_tup[1][1]}\n\t"
                f"{k_v_tup[2][0]}: {k_v_tup[2][1]}\n\t"
                f"{k_v_tup[3][0]}: {k_v_tup[3][1]}\n\t"
                f"{k_v_tup[4][0]}: {k_v_tup[4][1]}\n".replace('_', ' ')
            )
