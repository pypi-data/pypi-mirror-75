from click.testing import CliRunner
import pytest
import shutil

import coiled
from coiled.cli.install import install


if shutil.which("conda") is None:
    pytest.skip(
        "Conda is needed to create local software environments", allow_module_level=True
    )


@pytest.mark.slow
def test_install(sample_user):
    name = "my-env"
    coiled.create_software_environment(name=name, conda=["toolz"])
    runner = CliRunner()
    result = runner.invoke(install, [name])

    assert result.exit_code == 0
    output = result.output.lower()
    assert "conda activate" in output
    assert name in output


def test_install_raises(sample_user):
    bad_name = "not-a-software-environment"
    runner = CliRunner()
    result = runner.invoke(install, [bad_name])

    assert result.exit_code != 0
    err_msg = str(result.exception).lower()
    assert "could not find" in err_msg
    assert bad_name in err_msg
