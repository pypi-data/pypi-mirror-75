"""common cli arguments
"""


def filter_host(parser, required: bool = False):
    """
    common argument to display the --host flag.
    """
    parser.add_argument(
        "--host", help="specify a specific host", default=str(), required=required,
    )


def filter_hosts(parser, required: bool = False):
    """
    common argument to display the --filter flag.
    """
    parser.add_argument(
        "--filter",
        "-f",
        help="filter inventory by key:value criteria",
        required=required,
        type=lambda x: x.split(","),
        default=dict(),
    )


def filter_group(parser, required: bool = False):
    """
    common argument to display the --group flag.
    """
    parser.add_argument(
        "--group",
        "-g",
        help="filter inventory by group",
        default=str(),
        required=required,
    )


def num_workers(parser, required: bool = False):
    """
    common argument to display the --workers flag.
    """
    parser.add_argument(
        "--workers",
        "-w",
        help="number of workers to utilize",
        default=20,
        required=required,
    )


def make_changes(parser, required: bool = False):
    """
    common argument to display the -X flag.
    """
    parser.add_argument(
        "-X",
        help="disables nornir dry-run",
        default=True,
        const=False,
        nargs="?",
        required=required,
    )


def verbose(parser, required: bool = False):
    """
    common argument to display the --verbose flag.
    """
    parser.add_argument(
        "--verbose",
        "-v",
        help="verbose logging",
        default=20,
        const=10,
        nargs="?",
        required=required,
    )


def output(parser, required: bool = False):
    """
    common argument to display the --output flag.
    """
    parser.add_argument(
        "--output", "-o", help="write output to file", required=required,
    )


def commands(parser, required: bool = False):
    """
    common argument to execute a list of commands with the --commands flag.
    """
    parser.add_argument(
        "--commands",
        "-c",
        help="commands to execute",
        action="append",
        required=required,
    )


def config(parser, required: bool = False):
    """
    common argument to execute commands in config mode with the --config flag.
    """
    parser.add_argument(
        "--config",
        help="execute commands in config mode",
        required=required,
        nargs="?",
        const=True,
    )


def netconf_source(parser, required: bool = False):
    """
    common argument to fetch a netconf config from source with the --source flag.
    """
    parser.add_argument(
        "--source",
        help="the source config config for netconf to get",
        choices=["candidate", "running"],
        required=required,
    )


def netconf_target(parser, required: bool = False):
    """
    common argument to edit a target config via netconf with the --target flag.
    """
    parser.add_argument(
        "--target",
        help="the target config for netconf to edit",
        choices=["candidate", "running", "startup"],
        required=required,
    )


def netconf_filter(parser, required: bool = False):
    """
    common argument to filter netconf get_config operations with the --nc-filter flag.
    """
    parser.add_argument(
        "--nc-filter",
        help="filter netconf get_config operation",
        choices=["subtree", "xpath"],
        required=required,
    )


def netconf_config(parser, required: bool = False):
    """
    common argument to define what to retrieve from a device or config to a device
    via netconf with the --nc-config flag.
    """
    parser.add_argument(
        "--nc-config",
        help="yang config file that defines what to fetch from a device or edit on a device",
        required=required,
    )
