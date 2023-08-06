from netnir.constants import NR
from netnir.helpers.common.args import filter_host, filter_hosts, filter_group
from netnir.helpers import render_filter


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
        self.nr = NR

        if self.args.host:
            hosts = self.nr.filter(name=self.args.host)
            return {"hosts": hosts.inventory.hosts}
        elif self.args.filter:
            hosts = self.nr.filter(**render_filter(self.args.filter))
            return {
                "hosts": hosts.inventory.hosts,
                "pattern": render_filter(self.args.filter),
            }
        elif self.args.group:
            hosts = self.nr.inventory.children_of_group(self.args.group)
            return {"hosts": hosts, "group": self.args.group}
        return {"hosts": self.nr.inventory.hosts, "groups": self.nr.inventory.groups}
