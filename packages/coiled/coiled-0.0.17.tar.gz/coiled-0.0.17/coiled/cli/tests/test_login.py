import os
from unittest import mock

from click.testing import CliRunner
import dask

from coiled.utils import normalize_server
from coiled.cli.login import login


def test_login(sample_user, tmp_path):
    with mock.patch("os.path.expanduser") as mock_expanduser:
        mock_expanduser.return_value = str(tmp_path)
        token = sample_user.user.auth_token.key
        server = dask.config.get("coiled.server")
        server = normalize_server(server)

        runner = CliRunner()
        result = runner.invoke(login, input=token)

        # Test output of command
        assert result.exit_code == 0
        assert "login" in result.output
        assert server in result.output
        assert "saved" in result.output

        # Ensure credentials were saved to config file
        config_file = os.path.join(tmp_path, ".config", "dask", "coiled.yaml")
        [config] = dask.config.collect_yaml([config_file])
        assert config["coiled"]["user"] == sample_user.user.username
        assert config["coiled"]["token"] == token
        assert config["coiled"]["server"] == server


def test_login_raises(sample_user):
    token = "not-a-valid-token"

    runner = CliRunner()
    result = runner.invoke(login, input=token)

    assert result.exit_code != 0
    err_msg = str(result.exception).lower()
    assert "invalid" in err_msg
    assert "token" in err_msg
