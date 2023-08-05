"""
    tests.integration.utils.processes.test_helpers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Integration tests for saltfactories.utils.processes.helpers
"""
import time

import pytest
import salt.defaults.exitcodes

from saltfactories.exceptions import FactoryNotStarted
from saltfactories.factories.daemons.master import MasterFactory
from saltfactories.utils import cli_scripts


@pytest.fixture(scope="package")
def daemons_id():
    return "set-exitcodes"


@pytest.fixture(scope="package")
def shell_tests_salt_master_config(request, salt_factories, daemons_id):
    return salt_factories.configure_master(
        request, daemons_id, config_overrides={"user": "unknown-user"}
    )


@pytest.mark.skip_on_windows
def test_exit_status_unknown_user(request, salt_factories, shell_tests_salt_master_config):
    """
    Ensure correct exit status when the master is configured to run as an unknown user.
    """
    script_path = cli_scripts.generate_script(
        salt_factories.scripts_dir,
        "salt-master",
        code_dir=salt_factories.code_dir,
        inject_coverage=salt_factories.inject_coverage,
        inject_sitecustomize=salt_factories.inject_sitecustomize,
    )
    proc = MasterFactory(cli_script_name=script_path, config=shell_tests_salt_master_config)
    proc.start()
    iterations = salt_factories.start_timeout
    while proc.is_running():
        if not iterations:  # pragma: no cover
            break
        time.sleep(1)
        iterations -= 1
    ret = proc.terminate()
    assert ret.exitcode == salt.defaults.exitcodes.EX_NOUSER, ret
    assert "The user is not available." in ret.stderr, ret

    # Now spawn_<daemon> should behave the same
    with pytest.raises(FactoryNotStarted) as exc:
        salt_factories.spawn_master(
            request, shell_tests_salt_master_config["id"], max_start_attempts=1
        )

    assert exc.value.exitcode == salt.defaults.exitcodes.EX_NOUSER, str(exc.value)
    assert "The user is not available." in exc.value.stderr, str(exc.value)
