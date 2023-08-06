import json
import urllib.request
from importlib.metadata import version
from distutils.version import LooseVersion


def check():
    name = "bbrecon"
    installed_version = LooseVersion(version(name))

    pypi_url = f"https://pypi.org/pypi/{name}/json"
    response = urllib.request.urlopen(pypi_url).read().decode()
    latest_version = max(
        LooseVersion(s) for s in json.loads(response)["releases"].keys()
    )

    print("package:", name, "installed:", installed_version, "latest:", latest_version)
