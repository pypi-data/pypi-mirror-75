from netnir import __version__
from netnir.constants import NETNIR_CONFIG
from pprint import pprint
import argparse
import sys


"""cli class to build and execute cli commands
"""


class Cli:
    """
    a class object used to setup the netnir cli.
    """

    def __init__(self):
        """
        A class object used to setup the netnir cli, consume the available commands from plugins,
        display the available commands, and execute the available commands based on user input.
        """
        self.plugins = NETNIR_CONFIG["plugins"]
        self.loaded_plugins = dict()
        self.parser = MyParser(prog="netnir")
        self.parser.add_argument(
            "--version", default=False, action="store_true", help="display version"
        )

        subparsers = self.parser.add_subparsers(title="netnir commands", dest="command")

        for task_key, task in self.plugins.items():
            plugin = task["class"].split(".")[:-1]
            app = task["class"].split(".")[-1]
            cmdparser = subparsers.add_parser(
                task_key, help=task["description"], description=task["description"],
            )

            try:
                plugin = getattr(__import__(".".join(plugin), fromlist=[app]), app)
                self.loaded_plugins.update({task_key: plugin})
            except ModuleNotFoundError:
                raise

            plugin.parser(cmdparser)

        self.args = self.parser.parse_args()

        if self.args.version:
            sys.exit(f"netnir version {__version__}")

    def dispatch(self):
        """
        Consume and display the available commands from plugins.
        """
        command = self.args.command

        if command is None:
            return self.parser.error(message="too few commands")

        plugin_class = self.loaded_plugins.get(command, None)

        if plugin_class is None:
            command = sys.argv[1]
            plugin_class = self.loaded_plugins.get(command, None)

        plugin = plugin_class(self.args)

        return pprint(plugin.run())


class MyParser(argparse.ArgumentParser):
    """
    overwrite the argparse.ArgumentParser defaults.
    """

    def error(self, message):
        """
        overwrite the default error
        """
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)
