""" netnir command scaffolding """


class CommandScaffold:
    """ scaffold class """

    def __init__(self, args):
        """initialize the class

        :params args: type object
        """
        from netnir.constants import NR

        self.args = args
        self.nr = NR

    @staticmethod
    def parser(parser):
        """command parser function

        :params parser: type object
        """
        from netnir.helpers.common.args import filter_host, filter_hosts, filter_group

        filter_host(parser)
        filter_hosts(parser)
        filter_group(parser)

    def run(self):
        """things to do"""
        return "things to do"

    def _inventory(self):
        """filter inventory

        :returns: filtered nornir inventory object
        """
        from netnir.helpers import inventory_filter, filter_type

        devices_filter = filter_type(
            host=self.args.host, filter=self.args.filter, group=self.args.group
        )
        self.nr = inventory_filter(
            nr=self.nr,
            device_filter=devices_filter["data"],
            type=devices_filter["type"],
        )

        return self.nr
