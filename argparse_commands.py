from argparse import ArgumentParser


class ArgparseCommands:

    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument('grouped-teams', type=str)
        self.parser.parse_args(namespace=self)


