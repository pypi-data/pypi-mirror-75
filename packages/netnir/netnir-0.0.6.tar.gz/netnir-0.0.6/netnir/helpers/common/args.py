"""common cli arguments
"""


def filter_host(parser, required=False):
    """
    common argument to display the --host flag.
    """
    parser.add_argument(
        "--host", help="specify a specific host", default=str(), required=required,
    )


def filter_hosts(parser, required=False):
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


def filter_group(parser, required=False):
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


def num_workers(parser, required=False):
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


def make_changes(parser, required=False):
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


def verbose(parser, required=False):
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


def output(parser, required=False):
    """
    common argument to display the --output flag.
    """
    parser.add_argument(
        "--output", "-o", help="write output to file", required=required,
    )
