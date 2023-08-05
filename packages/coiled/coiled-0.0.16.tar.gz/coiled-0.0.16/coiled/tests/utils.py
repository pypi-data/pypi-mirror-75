import platform

import pytest

from cloud.apps import CloudConfig
from backends import in_process


def skip_in_process_backend_not_on_linux():
    if (
        isinstance(CloudConfig.backend, in_process.ClusterManager)
        and platform.system() != "Linux"
    ):
        pytest.skip("TODO: allow for conda solve + build on non-linux platforms")
