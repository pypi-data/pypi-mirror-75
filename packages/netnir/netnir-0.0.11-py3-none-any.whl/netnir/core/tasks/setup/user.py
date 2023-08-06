from netnir.core.credentials import Credentials
from netnir.constants import SERVICE_NAME, NETNIR_USER
from pprint import pprint

"""setup user cli commands
"""


class User:
    """
    cli user administration to create/fetch/delete a user
    """

    def __init__(self, args):
        """initialize the class
        """
        self.args = args

    @staticmethod
    def parser(parser):
        """parse cli arguments

        :param parser: type obj
        """
        parser.add_argument(
            "--create",
            help="create network device authentication credentials",
            required=False,
            nargs="?",
            default=False,
            const=True,
        )
        parser.add_argument(
            "--fetch",
            help="fetch network device authentication credentials",
            required=False,
            nargs="?",
            default=False,
            const=True,
        )
        parser.add_argument(
            "--delete",
            help="delete network device authentication credentials",
            required=False,
            nargs="?",
            default=False,
            const=True,
        )

    def run(self):
        """execute cli task

        :return: credentials result
        """
        creds = Credentials(service_name=SERVICE_NAME, username=NETNIR_USER)

        if self.args.create:
            return pprint(creds.create())
        elif self.args.fetch:
            return pprint(creds.fetch())
        elif self.args.delete:
            return pprint(creds.delete())
