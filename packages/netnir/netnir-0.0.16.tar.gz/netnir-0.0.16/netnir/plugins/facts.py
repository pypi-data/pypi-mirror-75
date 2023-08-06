from nornir.core.task import Task, Result


"""nornir facts plugins
"""


def inventory_facts(task: Task) -> Result:
    """gather inventory facts

    :params task: type object

    :returns: inventory host facts dictionary
    """
    return Result(
        host=task.host, result={"facts": task.host.data, "groups": task.host.groups},
    )
