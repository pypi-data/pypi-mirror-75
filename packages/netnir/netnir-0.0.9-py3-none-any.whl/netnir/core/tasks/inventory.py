from netnir.constants import NR
from netnir.helpers.common.args import filter_host, filter_hosts, filter_group
from netnir.helpers import filter_type, inventory_filter
from netnir.plugins.facts import inventory_facts
from nornir.plugins.functions.text import print_result


"""inventory cli commands
"""


class Inventory:
    """
    cli based inventory search

    :param args: type obj
    """

    def __init__(self, args):
        """
        initialize the inventory class
        """
        self.args = args
        self.nr = NR

    @staticmethod
    def parser(parser):
        """
        cli command parser
        """
        filter_host(parser)
        filter_hosts(parser)
        filter_group(parser)

    def run(self):
        """
        cli execution
        """
        devices_filter = filter_type(
            host=self.args.host, filter=self.args.filter, group=self.args.group
        )
        self.nr = inventory_filter(
            nr=self.nr,
            device_filter=devices_filter["data"],
            type=devices_filter["type"],
        )
        results = self.nr.run(task=inventory_facts)
        print_result(results)

        return results
