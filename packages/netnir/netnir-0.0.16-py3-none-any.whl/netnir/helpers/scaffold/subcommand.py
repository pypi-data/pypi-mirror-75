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
        from netnir.helpers import plugins_import

        subparsers = parser.add_subparsers(title=cls.title, dest="command")
        plugins_import(tasks=cls.tasks, subparsers=subparsers)

    def run(self):
        """
        execute the subcommand parser.
        """
        command = self.args.command
        action = self.tasks[command]["class"]
        plugin = action.split(".")[:-1]
        app = action.split(".")[-1]
        action_class = getattr(__import__(".".join(plugin), fromlist=[app]), app)
        action = action_class(self.args)
        action.run()
