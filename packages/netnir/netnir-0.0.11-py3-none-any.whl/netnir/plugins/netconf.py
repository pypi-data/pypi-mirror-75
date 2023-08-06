from nornir.core.task import Task, Result


def netconf_get(task: Task) -> Result:
    """nornir netconf get task

    :params task: type object
    """
    manager = task.host.get_connection(
        connection="netconf", configuration=task.nornir.config
    )
    result = manager.get()

    return Result(result=result, host=task.host)
