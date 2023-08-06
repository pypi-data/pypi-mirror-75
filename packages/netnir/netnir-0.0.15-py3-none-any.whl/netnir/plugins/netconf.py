from nornir.core.task import Task, Result


def netconf_get_config(
    task: Task,
    source: str = "candidate",
    nc_filter: str = None,
    nc_filter_type: str = None,
) -> Result:
    """nornir netconf get config task

    :params task: type object
    :params source: type str - configuration source
    :params nc_filter: type str - netconf filter
    :params nc_filter_type: type str
    :returns: nornir result object
    """
    manager = task.host.get_connection(
        connection="netconf", configuration=task.nornir.config
    )
    if nc_filter and nc_filter_type:
        result = manager.get_config(source=source, filter=(nc_filter_type, nc_filter))
    else:
        result = manager.get_config(source=source)

    return Result(result=result, host=task.host)


def netconf_edit_config(
    task: Task, target: str = "candidate", nc_config: str = None
) -> Result:
    """nornir netconf edit config task

    :params task: type object
    :params target: type str - configuration target
    :params nc_config: type str - yang config model
    :returns: nornir result object
    """
    manager = task.host.get_connection(
        connection="netconf", configuration=task.nornir.config
    )
    with manager.lock(target=target):
        config_response = manager.edit_config(target=target, config=nc_config)
        config_validate = manager.validate(source=target)

        if config_response.ok and config_validate.ok:
            result = {
                "config_response": config_response.ok,
                "config_validate": config_validate.ok,
            }
            failed = False
            manager.commit()
        else:
            result = {
                "config_response": config_response.error,
                "config_validate": config_validate.error,
            }
            failed = True
            manager.discard_changes()

    return Result(result=result, host=task.host, failed=failed)
