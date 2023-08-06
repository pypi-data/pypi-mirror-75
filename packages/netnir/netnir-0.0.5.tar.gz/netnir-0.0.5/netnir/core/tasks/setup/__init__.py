from netnir.core.tasks.setup.user import User
from netnir.helpers.scaffold.subcommand import SubCommandParser

"""setup subcommand initialization
"""


class Setup(SubCommandParser):
    """
    class to setup the setup subcommand structure
    """

    title = "setup commands"
    tasks = {
        "user": {"class": User, "description": "user administration tasks"},
    }

    def __init__(self, args):
        """
        :param args: type obj
        """
        self.args = args

        super().__init__(args=self.args)
