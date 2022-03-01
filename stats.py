import pandas as pd
import api_requests
import json

import folder_structure


class PlayerStats(api_requests.ApiRequests, folder_structure.FolderStructure):

    def __init__(self):
        super(PlayerStats, self).__init__()
        self.get_players_stats_columns = self.get_players_stats_columns()

    def save_player_stats_locally(self):
        for i in self.get_player_stats():
            json_resp = json.loads(i)
            df = pd.json_normalize(json_resp, 'data')

            if self.check_player_stats_csv_file():
                df.to_csv(self.player_stats_csv_file, header=False, mode='a', index=False)
            else:
                df.to_csv(self.player_stats_csv_file, header=True, index=False)

    def get_players_stats_columns(self):
        df = pd.read_csv(self.player_stats_csv_file, na_values=' ')
        df.sort_index()
        columns = df[['first_name', 'last_name', 'height_feet', 'height_inches', 'weight_pounds']]
        return columns

    def get_player_stats_by_name(self, name):

        for column in self.get_players_stats_columns:

            try:
                grouped = self.get_players_stats_columns.groupby(column)
                players_height = grouped.get_group(name).sort_values([
                    'height_feet',
                    'height_inches'
                ], ascending=False).head(10)

                if not players_height.isna().head(1)['height_feet'].bool():
                    meter_height = round(
                        (players_height['height_feet'] + (players_height['height_inches'] * 0.083333333)) * 0.3048, 2
                    )

                    first_row = float(meter_height[:1])
                    for index, value in players_height.iterrows():

                        if first_row == meter_height[index]:
                            print(
                                f"The tallest player: {value['first_name']} {value['last_name']} {meter_height[index]} meters")
                else:
                    first_or_last = 'by first name' if column == 'first_name' else 'by last name'
                    print(f'The tallest player: Not found {first_or_last}')

                #  There is a weight
                players_weight = grouped.get_group(name).sort_values(
                    'weight_pounds',
                    ascending=False).head(10)

                if not players_weight.isna().head(1)['weight_pounds'].bool():
                    kilogram_weight = round(players_weight['weight_pounds'] * 0.453592, 0)

                    first_row = float(kilogram_weight[:1])
                    for index, value in players_weight.iterrows():

                        if first_row == kilogram_weight[index]:
                            print(
                                f"The heaviest player: {value['first_name']} {value['last_name']} {int(kilogram_weight[index])} kilograms")
                else:
                    first_or_last = 'by first name' if column == 'first_name' else 'by last name'
                    print(f'The heaviest player: Not found {first_or_last}')

            except KeyError:
                continue
