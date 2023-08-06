"""default configuration
"""
default_config = {
    "directories": {
        "hostvars": "./host_vars",
        "groupvars": "./group_vars",
        "templates": "./templates",
        "output": "./output",
        "hier": "./conf/hier",
    },
    "domain": "example.net",
    "nornir": {"config": "./conf/nornir.yaml"},
    "plugins": {
        "user": {
            "class": "netnir.core.tasks.user.User",
            "description": "netnir user commands",
        },
        "inventory": {
            "class": "netnir.core.tasks.inventory.Inventory",
            "description": "inventory search command",
        },
        "cp": {
            "class": "netnir.core.tasks.config_plan.ConfigPlan",
            "description": "config plan commands",
        },
        "ssh": {
            "class": "netnir.core.tasks.ssh.Ssh",
            "description": "command and config execution over SSH",
        },
        "netconf": {
            "class": "netnir.core.tasks.netconf.NetConf",
            "description": "command and config execution over NETCONF",
        },
        "fetch": {
            "class": "netnir.core.tasks.fetch.Fetch",
            "description": "fetch commands",
        },
    },
}

"""default nornir config
"""
nornir_defaults = {
    "core": {"num_workers": 20},
    "inventory": {"plugin": "netnir.core.inventory.NornirInventory"},
}
