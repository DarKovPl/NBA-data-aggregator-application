import os
from sqlalchemy import Column, String, create_engine, Table
from sqlalchemy.orm import declarative_base


class FolderStructure:

    def __init__(self):
        super(FolderStructure, self).__init__()
        self.current_directory = os.getcwd()
        self.folder_name = r'files'
        self.folder_for_files = os.path.join(self.current_directory, self.folder_name)
        self.player_stats_csv_file = os.path.join(self.folder_for_files, r'player_stats.csv')
        self.teams_stats_csv_file = os.path.join(self.folder_for_files, r'output.csv')
        self.teams_stats_json_file = os.path.join(self.folder_for_files, r'output.json')
        self.teams_stats_sqlite_database = os.path.join(self.folder_for_files, r'output.sqlite')

    def create_folder_structure(self):
        if not os.path.exists(self.folder_for_files):
            os.makedirs(self.folder_for_files)

    def check_player_stats_csv_file(self):
        if os.path.isfile(self.player_stats_csv_file):
            return True
        else:
            return False

    def check_teams_stats_csv_file(self):
        if os.path.isfile(self.teams_stats_csv_file):
            return True
        else:
            return False

    def delete_existing_csv_files(self):
        if os.path.isfile(self.player_stats_csv_file):
            os.remove(self.player_stats_csv_file)

        if os.path.isfile(self.teams_stats_csv_file):
            os.remove(self.teams_stats_csv_file)

    def delete_teams_stats_json_file(self):
        if os.path.isfile(self.teams_stats_json_file):
            os.remove(self.teams_stats_json_file)


FolderStructure().create_folder_structure()
base_path = FolderStructure().teams_stats_sqlite_database

if os.path.exists(base_path):
    os.remove(base_path)

engine = create_engine(f"sqlite:///{base_path}", echo=False)
Base = declarative_base()


class TeamsStats(Base):
    __table__ = Table(
        'teams_stats',
        Base.metadata,
        Column('team_name', String, primary_key=True),
        Column('won_games_as_home_team', String),
        Column('won_games_as_visitor_team', String),
        Column('lost_games_as_home_team', String),
        Column('lost_games_as_visitor_team', String),
    )


Base.metadata.create_all(engine)
