from netnir.constants import NR
from netnir.core.networking import Networking
from netnir.helpers import output_writer, filter_type, inventory_filter
from netnir.helpers.common.args import (
    filter_host,
    filter_hosts,
    filter_group,
    output,
    num_workers,
)
from nornir.plugins.functions.text import print_result
import sys

"""ssh cli commands
"""


class Ssh:
    """
    cli command to execute show and config commands via SSH

    :params args: type obj
    """

    def __init__(self, args):
        """
        initialize the ssh class
        """
        self.args = args
        self.nr = NR

    @staticmethod
    def parser(parser):
        """
        cli command parser
        """
        filter_host(parser)
        filter_group(parser)
        filter_hosts(parser)
        output(parser)
        num_workers(parser)

        parser.add_argument(
            "--commands",
            "-c",
            help="commands to execute",
            action="append",
            required=False,
        )
        parser.add_argument(
            "--config",
            help="execute commands in config mode",
            required=False,
            nargs="?",
            const=True,
        )

    def run(self):
        """
        cli command execution
        """

        device_filter = filter_type(
            host=self.args.host, filter=self.args.filter, group=self.args.group
        )
        hosts = inventory_filter(
            self.nr, device_filter=device_filter["data"], type=device_filter["type"]
        )
        networking = Networking(nr=hosts, num_workers=self.args.workers,)

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
