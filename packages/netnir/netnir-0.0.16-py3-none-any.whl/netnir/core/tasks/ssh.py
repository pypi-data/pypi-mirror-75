from netnir.helpers.scaffold.command import CommandScaffold
from netnir.core.networking import Networking
from netnir.helpers import output_writer
from netnir.helpers.common.args import (
    output,
    num_workers,
    commands,
    config,
)
from nornir.plugins.functions.text import print_result
import sys

"""ssh cli commands"""


class Ssh(CommandScaffold):
    """
    cli command to execute show and config commands via SSH
    """

    @staticmethod
    def parser(parser):
        """
        cli command parser
        """
        CommandScaffold.parser(parser)
        output(parser)
        num_workers(parser)
        commands(parser)
        config(parser)

    def run(self):
        """
        cli command execution
        """

        self.nr = self._inventory()
        networking = Networking(nr=self.nr, num_workers=self.args.workers,)

        if self.args.config:
            results = networking.config(self.args.commands)
        elif self.args.commands:
            results = networking.fetch(self.args.commands)
        else:
            sys.exit()

        if isinstance(results, str):
            results = [results]

        for task in results:
            if self.args.output:
                output_writer(nornir_results=task, output_file=self.args.output)

            print_result(task)

        return results
