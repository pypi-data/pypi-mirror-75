from netnir.constants import HIER_DIR
from netnir.core.output import Output
from nornir.core.task import Task, Result
from hier_config import Host
import logging
import os
import yaml

"""hier_config nornir plugin
"""


def hier_host(
    task: Task,
    include_tags: list = None,
    exclude_tags: list = None,
    running_config: str = None,
    compiled_config: str = None,
    config_path: str = None,
    load_file: bool = False,
) -> Result:
    """
    hier_config task for nornir

    :param task: type object
    :param incude_tags: type list
    :param exclude_tags: type list
    :param running_config: type str
    :param compiled_config: type str
    :param config_path: type str
    :param load_file: type bool

    :returns: hier remediation object
    """

    operating_system = task.host.data["os"]
    hier_options_file = "/".join([HIER_DIR, operating_system, "options.yml"])
    hier_tags_file = "/".join([HIER_DIR, operating_system, "tags.yml"])
    running_config = "/".join([config_path, task.host.name, running_config])
    compiled_config = "/".join([config_path, task.host.name, compiled_config])

    if os.path.isfile(hier_options_file):
        hier_options = yaml.load(open(hier_options_file), Loader=yaml.SafeLoader)
    else:
        return Result(
            host=task.host,
            result=f"{hier_options_file} does not exist",
            failed=True,
            severity_level=logging.WARN,
        )

    host = Host(
        hostname=task.host.name, os=operating_system, hconfig_options=hier_options
    )
    host.load_config_from(
        config_type="running", name=running_config, load_file=load_file
    )
    host.load_config_from(
        config_type="compiled", name=compiled_config, load_file=load_file
    )

    if os.path.isfile(hier_tags_file):
        host.load_tags(hier_tags_file)
    else:
        return Result(
            host=task.host,
            result=f"{hier_tags_file} does not exist",
            failed=True,
            severity_level=logging.WARN,
        )

    host.load_remediation()

    output = Output(host=task.host.name, output_file="remediation.conf")
    output.write(
        host.filter_remediation(include_tags=include_tags, exclude_tags=exclude_tags)
    )

    return Result(host=task.host, result=output.read())
