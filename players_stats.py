import json
import sys
import pandas as pd
import api_requests
import folder_structure


class PlayerStats(api_requests.ApiRequests, folder_structure.FolderStructure):

    def __init__(self):
        super(PlayerStats, self).__init__()
        self.columns = None

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
        self.columns = df[['first_name', 'last_name', 'height_feet', 'height_inches', 'weight_pounds']]

    def view_player_stats_by_name(self, name: str):
        err = 0
        for column_name in self.columns:
            try:
                grouped = self.columns.groupby(column_name)
                players_height = grouped.get_group(name).sort_values([
                    'height_feet',
                    'height_inches'
                ], ascending=False).head(10)

                if not players_height.isna().head(1)['height_feet'].bool():
                    meter_height = round(
                        (players_height['height_feet']
                         + (players_height['height_inches'] * 0.083333333)) * 0.3048, 2)

                    first_row = float(meter_height[:1])
                    for index, value in players_height.iterrows():

                        if first_row == meter_height[index]:
                            sys.stdout.writelines(
                                f"The tallest player: "
                                f"{value['first_name']} "
                                f"{value['last_name']} "
                                f"{meter_height[index]} meters\n"
                            )
                else:
                    first_or_last = 'by first name' if column_name == 'first_name' else 'by last name'
                    sys.stdout.writelines(f'The tallest player: Not found {first_or_last}\n')

                #  There is a weight
                players_weight = grouped.get_group(name).sort_values(
                    'weight_pounds',
                    ascending=False).head(10)

                if not players_weight.isna().head(1)['weight_pounds'].bool():
                    kilogram_weight = round(players_weight['weight_pounds'] * 0.453592, 0)

                    first_row = float(kilogram_weight[:1])
                    for index, value in players_weight.iterrows():

                        if first_row == kilogram_weight[index]:
                            sys.stdout.writelines(
                                f"The heaviest player:"
                                f" {value['first_name']}"
                                f" {value['last_name']}"
                                f" {int(kilogram_weight[index])} kilograms\n")
                else:
                    first_or_last = 'by first name' if column_name == 'first_name' else 'by last name'
                    sys.stdout.writelines(f'The heaviest player: Not found {first_or_last}\n')

            except KeyError:
                err += 1
                continue

        if err == self.columns.shape[1]:
            sys.stdout.writelines(f'There is probably a misspell in "--name" parameter: {name}\n'
                                  f'If you need help, write main.py -h\n')
