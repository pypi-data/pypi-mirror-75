from netnir.helpers.scaffold.subcommand import SubCommandParser


"""fetch subcommands initialization
"""


class Fetch(SubCommandParser):
    """
    fetch subcommand parser
    """

    title = "fetch commands"
    tasks = {
        "config": {
            "class": "netnir.core.tasks.fetch.config.FetchConfig",
            "description": "fetch current config from a network device",
        },
    }

    def __init__(self, args):
        """initialize the class
        """
        self.args = args

        super().__init__(args=self.args)
