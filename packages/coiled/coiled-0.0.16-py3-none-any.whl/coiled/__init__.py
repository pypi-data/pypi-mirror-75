from .core import (
    create_software_environment,
    list_software_environments,
    delete_software_environment,
    create_cluster_configuration,
    list_cluster_configurations,
    delete_cluster_configuration,
    create_cluster,
    list_clusters,
    delete_cluster,
    Cloud,
)
from .cluster import Cluster

# Get function backing "coiled install" command
from .cli.install import install as _install

install = _install.callback
del _install

from . import config

del config

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
