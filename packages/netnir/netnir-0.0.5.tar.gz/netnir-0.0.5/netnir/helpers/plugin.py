"""fetch plugin helpers
"""


def load_plugins(plugins, subparsers, parser):
    """
    fetch and load the plugins to display their commands in the cli.

    :param plugins: type dict
    :param subparsers: type obj
    :param parser: type obj

    :return: arguments namespace
    """
    loaded_plugins = dict()

    for task_key, task in plugins.items():
        plugin_path = task["class"].split(".")[:-1]
        app = task["class"].split(".")[-1]
        cmdparser = subparsers.add_parser(
            task_key, help=task["description"], description=task["description"],
        )

        try:
            plugin = getattr(__import__(".".join(plugin_path), fromlist=[app]), app)
            loaded_plugins.update({task_key: plugin})
        except ModuleNotFoundError:
            raise

        plugin.parser(cmdparser)

        return parser.parse_args()
