class SubCommandParser:
    """
    A base class for parsing subcommands. It's meant to be used as an inherited
    class.

    .. code:: python

       from netnir.helpers.scaffold.subcommand import SubCommandParser

       class SomeCommand(SubCommandParser):
           tasks = {"cmd1": {"class": "app.to.import.Class", "description": "task description"}}
           title = "app title"

           def __init__(self, args):
               self.args = args

               super().__init__(args=self.args)

    :params args: type obj
    """

    tasks = dict()
    title = str()

    def __init__(self, args):
        """initialize class

        :param args: type obj
        """
        self.args = args

    @classmethod
    def parser(cls, parser):
        """
        sub command parser.
        """
        subparsers = parser.add_subparsers(title=cls.title, dest="command")

        for task_key, task in cls.tasks.items():
            cmdparser = subparsers.add_parser(
                task_key, help=task["description"], description=task["description"],
            )
            task["class"].parser(cmdparser)

    def run(self):
        """
        execute the subcommand parser.
        """
        command = self.args.command
        action_class = self.tasks[command]["class"]
        action = action_class(self.args)
        action.run()
