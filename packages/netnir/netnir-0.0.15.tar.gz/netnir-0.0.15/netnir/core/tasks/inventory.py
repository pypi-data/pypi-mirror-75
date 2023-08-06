from netnir.helpers.scaffold.command import CommandScaffold


class Inventory(CommandScaffold):
    """
    cli based inventory search
    """

    def run(self):
        from netnir.plugins.facts import inventory_facts
        from nornir.plugins.functions.text import print_result

        self.nr = self._inventory()
        results = self.nr.run(task=inventory_facts)
        print_result(results)

        return results
