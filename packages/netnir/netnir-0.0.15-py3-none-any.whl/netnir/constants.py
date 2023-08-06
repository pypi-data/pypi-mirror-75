from netnir.helpers import netnir_config
from nornir import InitNornir
import os

NETNIR_CONFIG = netnir_config()
NETNIR_DIRS = NETNIR_CONFIG["directories"]
HOSTVARS = NETNIR_DIRS.get("hostvars", None)
GROUPVARS = NETNIR_DIRS.get("groupvars", None)
TEMPLATES = NETNIR_DIRS.get("templates", None)
DOMAIN = NETNIR_CONFIG.get("domain", None)
OUTPUT_DIR = NETNIR_DIRS.get("output", None)
SERVICE_NAME = os.environ.get("NETNIR_SERVICE_NAME", "netnir")
NETNIR_USER = os.environ.get("NETNIR_USER")
NETNIR_PASS = os.environ.get("NETNIR_PASS")
NORNIR_CONFIG = NETNIR_CONFIG["nornir"]["config"]
HIER_DIR = NETNIR_DIRS.get("hier", None)
NR = InitNornir(config_file=os.path.expanduser(NORNIR_CONFIG))
