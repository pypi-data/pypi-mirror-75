from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config


"""ssh networking class
"""


class Networking:
    """
    a networking class that utilizes nornir's netmiko plugin to interact with devices
    via SSH.

    :params nr: type obj (required)
    :params mgmt_protocol: type str (optional)
    :params num_workers: type int (optional)

    .. code:: python

       from netnir.core import Networking
       from nornir import InitNornir

       nr = InitNornir()
       networking = Networking(nr=nr)
       networking.fetch(commands=['show version'])
       networking.config(commands=['ip route 10.0.0.0 255.0.0.0 null0'])
    """

    def __init__(
        self, nr: object, mgmt_protocol: str = "ssh", num_workers: int = None,
    ):
        """
        initialize the networking class
        """
        self.nr = nr
        self.mgmt_protocol = mgmt_protocol
        self.nr.config.core.num_workers = (
            num_workers if num_workers else self.nr.config.core.num_workers
        )

    def fetch(self, commands):
        """
        execute show commands on the remote device and return the results

        :param commands: type list
        :return: nornir results object
        """
        if isinstance(commands, list):
            output = list()

            for command in commands:
                result = self.nr.run(task=netmiko_send_command, command_string=command)
                output.append(result)
        else:
            output = self.nr.run(task=netmiko_send_command, command_string=commands)

        return output

    def config(self, commands):
        """
        execute configuration commands on a remote device and return the results

        :param commands: type list
        :return: nornir results object
        """
        output = self.nr.run(task=netmiko_send_config, config_commands=commands)

        return output
