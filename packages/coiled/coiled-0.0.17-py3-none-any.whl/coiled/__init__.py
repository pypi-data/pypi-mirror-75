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

# Get function backing "coiled upload" command
from .cli.upload import upload as _upload

upload = _upload.callback
del _upload

# Register coiled configuration values with Dask's config system
from . import config

del config

# Top-level coiled.config attribute
def __getattr__(name):
    if name == "config":
        import dask

        return dask.config.get("coiled")
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# Use versioneer to handle package versioning
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
