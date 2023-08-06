from nornir.core.deserializer.inventory import Inventory
import os
import yaml


"""dynamic inventory builder class"""


class NornirInventory(Inventory):
    """
    default inventory module to dynamically create inventory objects from host_vars and group_vars
    and load the inventory objects into nornir's inventory system.
    """

    def __init__(self, **kwargs):
        """
        initialize the NornirInventory class and load the data into nornir
        """
        super().__init__(
            hosts=self.nhosts(), groups=self.ngroups(), defaults=self.ndefaults()
        )

    def nhosts(self):
        from netnir.helpers import device_mapper
        from netnir.core.credentials import Credentials
        from netnir.constants import (
            HOSTVARS,
            TEMPLATES,
            DOMAIN,
        )

        """
        load devices from host_vars and load them into the nornir inventory schema
        """
        data = dict()
        hosts = os.listdir(os.path.expanduser(HOSTVARS))
        creds = Credentials()
        creds = creds.fetch()

        for host in hosts:
            domain = DOMAIN
            host_vars = yaml.load(
                open(os.path.expanduser(HOSTVARS) + "/" + host), Loader=yaml.SafeLoader,
            )
            data[host] = {
                "hostname": f"{host}.{domain}" if domain else host,
                "username": host_vars.get("username", creds["username"]),
                "password": host_vars.get("password", creds["password"]),
                "port": host_vars.get("port", 22),
                "platform": device_mapper(host_vars["os"]),
                "groups": host_vars.get("groups", list()),
                "data": {
                    **host_vars,
                    "name": host,
                    "template_path": "/".join(
                        [
                            os.path.expanduser(TEMPLATES),
                            host_vars["provider"],
                            host_vars["os"],
                        ],
                    ),
                    "mgmt_protocol": host_vars.get("mgmt_protocol", "ssh"),
                },
                "connection_options": {
                    "netconf": {
                        "hostname": f"{host}.{domain}" if domain else host,
                        "username": host_vars.get("username", creds["username"]),
                        "password": host_vars.get("password", creds["password"]),
                        "platform": device_mapper(
                            os_type=host_vars["os"], proto="netconf"
                        ),
                        "port": host_vars.get("port", 830),
                        "extras": {"hostkey_verify": False},
                    },
                },
            }

        return data

    def ngroups(self):
        """
        load groups from group_vars and load them into the nornir inventory schema
        """
        from netnir.constants import GROUPVARS

        data = dict()
        groups = os.listdir(os.path.expanduser(GROUPVARS))
        if "all" in groups:
            groups.remove("all")

        for group in groups:
            group_vars = yaml.load(
                open(os.path.expanduser(GROUPVARS) + "/" + group),
                Loader=yaml.SafeLoader,
            )
            data[group] = {"data": group_vars}

        return data

    def ndefaults(self):
        """
        load the defaults from group_vars/all and load them into the nornir inventory schema
        """
        from netnir.constants import GROUPVARS

        if os.path.isfile(os.path.expanduser(GROUPVARS) + "/all"):
            default_vars = yaml.load(
                open(os.path.expanduser(GROUPVARS) + "/all"), Loader=yaml.SafeLoader,
            )
        else:
            default_vars = dict()

        return {"data": default_vars}
