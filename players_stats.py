import json
import pandas as pd
import api_requests
import folder_structure


class PlayerStats(api_requests.ApiRequests, folder_structure.FolderStructure):
    def __init__(self):
        super(PlayerStats, self).__init__()
        self.df_player_stats = None
        self.ds_by_first_name = None
        self.ds_by_last_name = None
        self.filtered_df_by_first_and_last_name = None

    def save_player_stats_locally(self):
        if not self.check_player_stats_csv_file():

            for i in self.get_player_stats():
                json_resp = json.loads(i)
                df = pd.json_normalize(json_resp, "data")

                if self.check_player_stats_csv_file():
                    df.to_csv(
                        self.player_stats_csv_file, header=False, mode="a", index=False
                    )
                else:
                    df.to_csv(self.player_stats_csv_file, header=True, index=False)

    def streamline_players_stats_data_frame(self):
        columns = [
            "id",
            "first_name",
            "last_name",
            "height_feet",
            "height_inches",
            "weight_pounds",
        ]

        self.df_player_stats = pd.read_csv(
            self.player_stats_csv_file, usecols=columns, index_col="id"
        )

        self.df_player_stats.fillna(
            value={columns[3]: 0, columns[4]: 0, columns[5]: 0}, inplace=True
        )

        self.df_player_stats["first_name"] = self.df_player_stats["first_name"].astype(
            "category"
        )
        self.df_player_stats["last_name"] = self.df_player_stats["last_name"].astype(
            "category"
        )

        self.df_player_stats["height_feet"] = self.df_player_stats[
            "height_feet"
        ].astype("uint8")
        self.df_player_stats["height_inches"] = self.df_player_stats[
            "height_inches"
        ].astype("uint8")

        self.df_player_stats["weight_pounds"] = self.df_player_stats[
            "weight_pounds"
        ].astype("uint16")

    def convert_imperial_to_metric(self):
        self.df_player_stats["height_metric"] = round(
            self.df_player_stats["height_feet"] * 0.3048
            + self.df_player_stats["height_inches"] * 0.0254,
            2,
        )

        self.df_player_stats["weight_kilograms"] = round(
            self.df_player_stats["weight_pounds"] * 0.453592, 0
        )

        self.df_player_stats["weight_kilograms"] = self.df_player_stats[
            "weight_kilograms"
        ].astype("uint8")

    def filter_players(self, name):

        self.ds_by_first_name = (
            self.df_player_stats["first_name"].squeeze().sort_values()
        )
        self.ds_by_last_name = self.df_player_stats["last_name"].squeeze().sort_values()

        self.ds_by_first_name = self.ds_by_first_name[self.ds_by_first_name == name]
        self.ds_by_last_name = self.ds_by_last_name[self.ds_by_last_name == name]

        indexes_list = (
            self.ds_by_first_name.index.tolist() + self.ds_by_last_name.index.tolist()
        )

        self.filtered_df_by_first_and_last_name = self.df_player_stats.loc[indexes_list]

    def get_tallest_and_heaviest_players(self):

        tallest_players, heaviest_players = pd.DataFrame([]), pd.DataFrame([])

        filtered_players = self.filtered_df_by_first_and_last_name[
            ["first_name", "last_name", "height_metric", "weight_kilograms"]
        ]

        if (filtered_players["height_metric"] > 0).any():
            tallest_players = filtered_players["height_metric"].rank().copy("deep")
            tallest_players = filtered_players.loc[
                tallest_players[tallest_players == tallest_players.max()].index
            ]

        if (filtered_players["weight_kilograms"] > 0).any():
            heaviest_players = filtered_players["weight_kilograms"].rank().copy("deep")
            heaviest_players = filtered_players.loc[
                heaviest_players[heaviest_players == heaviest_players.max()].index
            ]

        return tallest_players, heaviest_players

    def __str__(self):

        tallest, heaviest = (
            self.get_tallest_and_heaviest_players()[0],
            self.get_tallest_and_heaviest_players()[1],
        )

        height_output = ""
        weight_output = ""

        if not tallest.empty:
            tallest = tallest.T
            tallest = list(tallest.to_dict().values())

            for value in tallest:
                height_output += (
                    f"The tallest player: "
                    f"{value['first_name']} "
                    f"{value['last_name']} "
                    f"{value['height_metric']} meters\n"
                )
        else:
            height_output += "The tallest player: Not found\n"

        if not heaviest.empty:
            heaviest = heaviest.T
            heaviest = list(heaviest.to_dict().values())

            for value in heaviest:
                weight_output += (
                    f"The heaviest player: "
                    f"{value['first_name']} "
                    f"{value['last_name']} "
                    f"{value['weight_kilograms']} kilograms\n"
                )

        else:
            weight_output += "The heaviest player: Not found"

        return f"{height_output}{weight_output}"
