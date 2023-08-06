import os
import yaml
import os.path as osp


SCENARIO_DIR = osp.dirname(osp.abspath(__file__))

# default subnet address for internet
INTERNET = 0

# scenario property keys
SUBNETS = "subnets"
TOPOLOGY = "topology"
SENSITIVE_HOSTS = "sensitive_hosts"
SERVICES = "services"
OS = "os"
EXPLOITS = "exploits"
SERVICE_SCAN_COST = "service_scan_cost"
OS_SCAN_COST = "os_scan_cost"
SUBNET_SCAN_COST = "subnet_scan_cost"
HOST_CONFIGS = "host_configurations"
FIREWALL = "firewall"
HOSTS = "host"
STEP_LIMIT = "step_limit"

# scenario exploit keys
EXPLOIT_SERVICE = "service"
EXPLOIT_OS = "os"
EXPLOIT_PROB = "prob"
EXPLOIT_COST = "cost"

# host configuration keys
HOST_SERVICES = "services"
HOST_OS = "os"


def load_yaml(file_path):
    """Load yaml file located at file path.

    Parameters
    ----------
    file_path : str
        path to yaml file

    Returns
    -------
    dict
        contents of yaml file

    Raises
    ------
    Exception
        if theres an issue loading file. """
    with open(file_path) as fin:
        content = yaml.load(fin, Loader=yaml.FullLoader)
    return content


def get_file_name(file_path):
    """Extracts the file or dir name from file path

    Parameters
    ----------
    file_path : str
        file path

    Returns
    -------
    str
        file name with any path and extensions removed
    """
    full_file_name = file_path.split(os.sep)[-1]
    file_name = full_file_name.split(".")[0]
    return file_name
