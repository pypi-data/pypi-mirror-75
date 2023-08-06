from netnir.helpers.common.args import (
    filter_host,
    filter_group,
    filter_hosts,
    num_workers,
)
from netnir.helpers import filter_type, inventory_filter, output_writer
from netnir.core.networking import Networking
from netnir.constants import NR
from nornir.plugins.functions.text import print_result

"""fetch remove device configs
"""


class FetchConfig:
    """
    cli command to fetch remote device configs via nornir's netmiko_show_command plugin
    """

    def __init__(self, args):
        """initialize the class
        """
        self.args = args
        self.nr = NR

    @staticmethod
    def parser(parser):
        """cli command parser

        :param parser: type obj
        """
        filter_host(parser)
        filter_group(parser)
        filter_hosts(parser)
        num_workers(parser)

    def run(self):
        """execute the cli task

        :return: nornir results
        """

        device_filter = filter_type(
            host=self.args.host, filter=self.args.filter, group=self.args.group
        )
        self.nr = inventory_filter(
            nr=self.nr, device_filter=device_filter["data"], type=device_filter["type"]
        )
        networking = Networking(nr=self.nr, num_workers=self.args.workers)
        results = networking.fetch(commands="show running")
        output_writer(nornir_results=results, output_file="running.conf")

        return print_result(results)
