from netnir.helpers.defaults import default_config, nornir_defaults
from netnir.helpers.colors import TextColor
import yaml
import os
import logging


"""initialize netnir helpers
"""


def device_mapper(os_type: str, proto: str = "netmiko"):
    """
    map an os type to a netmiko device_type

    :params os_type: type str
    :params proto: type str, default "netmiko"

    :returns: device_type string
    """
    if proto == "netmiko":
        device_types = {
            "ios": "cisco_ios",
            "iosxr": "cisco_xr",
            "iosxe": "cisco_xe",
            "nxos": "cisco_nxos",
            "eos": "arista_eos",
        }
        try:
            result = device_types[os_type]
        except KeyError:
            return os_type
    elif proto == "netconf":
        device_types = {
            "csr": "csr",
            "iosxr": "iosxr",
            "iosxe": "iosxe",
            "nxos": "nexus",
            "junos": "junos",
        }
        try:
            result = device_types[os_type]
        except KeyError:
            return "default"
    else:
        result = os_type

    return result


def render_filter(pattern: list):
    """
    take the --filter argument list and return a k,v dict

    :param pattern: type list

    :return: pattern dict
    """
    result = dict()

    for item in pattern:
        k, v = item.split(":")
        result.update({k: v})

    return result


def output_writer(nornir_results, output_file):
    """
    write results to text file

    :param nornir_results: type obj
    :param output_file: type str
    """
    from netnir.core.output import Output

    for host, data in nornir_results.items():
        o = Output(host=host, output_file=output_file)
        o.write(data.result)


def inventory_filter(nr, device_filter, type):
    """
    nornir inventory filter helper

    :param nr: typ obj
    :param device_filter: str or dict
    :param type: type str

    :return: nornir object
    """
    from nornir.core.filter import F

    if type == "host":
        nr = nr.filter(name=device_filter)
    elif type == "filter":
        nr = nr.filter(**render_filter(device_filter))
    elif type == "group":
        nr = nr.filter(F(group__contains=device_filter))

    return nr


def filter_type(host: str = None, filter: str = None, group: str = None):
    """
    define how nornir inventory filter should execute
    """
    if host:
        return {"type": "host", "data": host}
    elif filter:
        return {"type": "filter", "data": filter}
    elif group:
        return {"type": "group", "data": group}

    return {"type": None, "data": None}


def netnir_config(config_file: str = "netnir.yaml"):
    if os.environ.get("NETNIR_CONFIG", None):
        return yaml.load(open(os.environ.get("NETNIR_CONFIG")), Loader=yaml.SafeLoader)
    elif os.path.isfile(config_file):
        return yaml.load(open(config_file), Loader=yaml.SafeLoader)
    else:
        message = TextColor.red(
            message="netnir config doesn't exist. creating defaults."
        )
        logging.warning(message)
        netnir_config = yaml.dump(default_config)
        nornir_config = yaml.dump(nornir_defaults)

        for k, v in default_config["directories"].items():
            if not os.path.isdir(v):
                message = TextColor.green(message=f"creating directory {v}")
                logging.warning(message)
                os.makedirs(v)

        message = TextColor.green(message=f"creating {config_file} config")
        logging.warning(message)

        with open(config_file, "w") as f:
            f.write(netnir_config)

        message = TextColor.green(message="creating ./conf/nornir.yaml config")
        logging.warning(message)

        with open("./conf/nornir.yaml", "w") as f:
            f.write(nornir_config)

        message = TextColor.green(message="loading config_file config")
        logging.warning(message)

    return yaml.load(open(config_file), Loader=yaml.SafeLoader)


def plugins_import(tasks: dict, subparsers: object):
    """import plugins into python and load them into netnir

    :param tasks: type dictionary
    :param subparsers: argparse subparsers object

    :returns: loaded_plugins dictionary
    """
    loaded_plugins = dict()

    for task_key, task in tasks.items():
        plugin = task["class"].split(".")[:-1]
        app = task["class"].split(".")[-1]
        cmdparser = subparsers.add_parser(
            task_key, help=task["description"], description=task["description"],
        )
        plugin = getattr(__import__(".".join(plugin), fromlist=[app]), app)
        loaded_plugins.update({task_key: plugin})
        plugin.parser(cmdparser)

    return loaded_plugins
