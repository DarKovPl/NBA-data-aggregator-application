import os


class FolderStructure:

    def __init__(self):
        super(FolderStructure, self).__init__()
        self.current_directory = os.getcwd()
        self.folder_name = r'files'
        self.folder_for_files = os.path.join(self.current_directory, self.folder_name)
        self.player_stats_csv_file = os.path.join(self.folder_for_files, r'player_stats.csv')

    def create_folder_structure(self):
        if not os.path.exists(self.folder_for_files):
            os.makedirs(self.folder_for_files)

    def check_player_stats_csv_file(self):
        if os.path.isfile(self.player_stats_csv_file):
            return True
        else:
            return False

    def delete_existing_files(self):
        if os.path.isfile(self.player_stats_csv_file):
            os.remove(self.player_stats_csv_file)
