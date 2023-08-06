"""nornir helpers
"""


def dry_run(nr: object, state: bool):
    """change nornir dry-run state

    :params nr: type obj
    :params state: type bool
    :returns: nornir instance
    """
    nr.state.dry_run = state

    return nr


def verbose_logging(nr: object, state: bool, level: str):
    """change nornir verbose logging state

    :params nr: type obj
    :params state: type bool
    :params level: type str
    :returns: nornir instance
    """
    nr.config.logging.level = level
    nr.config.logging.to_console = state

    return nr
