from netnir.helpers.scaffold.command import CommandScaffold


class NetConf(CommandScaffold):
    """netconf commands"""

    def run(self):
        """execute netconf commands

        :returns: nornir Result object
        """
        from netnir.plugins.netconf import netconf_get
        from nornir.plugins.functions.text import print_result

        self.nr = self._inventory()
        results = self.nr.run(task=netconf_get, name="NETCONF GET CONFIG AND STATE")
        print_result(results)

        return results
