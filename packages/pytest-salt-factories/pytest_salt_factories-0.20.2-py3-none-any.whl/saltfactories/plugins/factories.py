"""
..
    PYTEST_DONT_REWRITE


saltfactories.plugins.factories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Salt Daemon Factories PyTest Plugin
"""
import logging
import pathlib
import pprint

import pytest
import salt.config
import salt.loader  # pylint: disable=unused-import
import salt.utils.files
import salt.utils.verify
import salt.utils.yaml

import saltfactories
from saltfactories import hookspec
from saltfactories.factories import manager
from saltfactories.utils import ports
from saltfactories.utils.log_server import log_server_listener


log = logging.getLogger(__name__)


def pytest_addhooks(pluginmanager):
    """
    Register our custom hooks
    """
    pluginmanager.add_hookspecs(hookspec)


@pytest.fixture(scope="session")
def log_server_host():
    return "0.0.0.0"


@pytest.fixture(scope="session")
def log_server_port():
    return ports.get_unused_localhost_port()


@pytest.fixture(scope="session")
def log_server_level(request):
    # If PyTest has no logging configured, default to ERROR level
    levels = [logging.ERROR]
    logging_plugin = request.config.pluginmanager.get_plugin("logging-plugin")
    try:
        level = logging_plugin.log_cli_handler.level
        if level is not None:
            levels.append(level)
    except AttributeError:
        # PyTest CLI logging not configured
        pass
    try:
        level = logging_plugin.log_file_level
        if level is not None:
            levels.append(level)
    except AttributeError:
        # PyTest Log File logging not configured
        pass

    level_str = logging.getLevelName(min(levels))
    return level_str


@pytest.fixture(scope="session")
def log_server(log_server_host, log_server_port):
    log.info("Starting log server at %s:%d", log_server_host, log_server_port)
    with log_server_listener(log_server_host, log_server_port):
        log.info("Log Server Started")
        # Run tests
        yield


@pytest.fixture(scope="session")
def salt_factories_config(
    pytestconfig, tempdir, log_server_host, log_server_port, log_server_level
):
    """
    Return a dictionary with the keyword arguments for SaltFactoriesManager
    """
    return {
        "code_dir": saltfactories.CODE_ROOT_DIR.parent,
        "inject_coverage": True,
        "inject_sitecustomize": True,
        "log_server_host": log_server_host,
        "log_server_port": log_server_port,
        "log_server_level": log_server_level,
    }


@pytest.fixture(scope="session")
def salt_factories(
    request, pytestconfig, tempdir, log_server, salt_factories_config,
):
    if not isinstance(salt_factories_config, dict):
        raise RuntimeError("The 'salt_factories_config' fixture MUST return a dictionary")
    log.debug(
        "Instantiating the Salt Factories Manager with the following keyword arguments:\n%s",
        pprint.pformat(salt_factories_config),
    )
    _manager = manager.SaltFactoriesManager(
        pytestconfig,
        tempdir,
        stats_processes=request.session.stats_processes,
        **salt_factories_config
    )
    yield _manager
    _manager.event_listener.stop()


def pytest_saltfactories_minion_verify_configuration(request, minion_config, username):
    """
    This hook is called to verify the provided minion configuration
    """
    # verify env to make sure all required directories are created and have the
    # right permissions
    verify_env_entries = [
        str(pathlib.Path(minion_config["pki_dir"]) / "minions"),
        str(pathlib.Path(minion_config["pki_dir"]) / "minions_pre"),
        str(pathlib.Path(minion_config["pki_dir"]) / "minions_rejected"),
        str(pathlib.Path(minion_config["pki_dir"]) / "accepted"),
        str(pathlib.Path(minion_config["pki_dir"]) / "rejected"),
        str(pathlib.Path(minion_config["pki_dir"]) / "pending"),
        str(pathlib.Path(minion_config["log_file"]).parent),
        str(pathlib.Path(minion_config["cachedir"]) / "proc"),
        # minion_config['extension_modules'],
        minion_config["sock_dir"],
    ]
    salt.utils.verify.verify_env(verify_env_entries, username, pki_dir=minion_config["pki_dir"])


def pytest_saltfactories_minion_write_configuration(request, minion_config):
    """
    This hook is called to verify the provided minion configuration
    """
    config_file = minion_config.pop("conf_file")
    log.debug(
        "Writing to configuration file %s. Configuration:\n%s",
        config_file,
        pprint.pformat(minion_config),
    )

    # Write down the computed configuration into the config file
    with salt.utils.files.fopen(config_file, "w") as wfh:
        salt.utils.yaml.safe_dump(minion_config, wfh, default_flow_style=False)

    # Make sure to load the config file as a salt-master starting from CLI
    options = salt.config.minion_config(
        config_file, minion_id=minion_config["id"], cache_minion_id=True
    )
    return options


def pytest_saltfactories_master_verify_configuration(request, master_config, username):
    """
    This hook is called to verify the provided master configuration
    """
    # verify env to make sure all required directories are created and have the
    # right permissions
    verify_env_entries = [
        str(pathlib.Path(master_config["pki_dir"]) / "minions"),
        str(pathlib.Path(master_config["pki_dir"]) / "minions_pre"),
        str(pathlib.Path(master_config["pki_dir"]) / "minions_rejected"),
        str(pathlib.Path(master_config["pki_dir"]) / "accepted"),
        str(pathlib.Path(master_config["pki_dir"]) / "rejected"),
        str(pathlib.Path(master_config["pki_dir"]) / "pending"),
        str(pathlib.Path(master_config["log_file"]).parent),
        str(pathlib.Path(master_config["cachedir"]) / "proc"),
        str(pathlib.Path(master_config["cachedir"]) / "jobs"),
        # master_config['extension_modules'],
        master_config["sock_dir"],
    ]
    verify_env_entries += master_config["file_roots"]["base"]
    verify_env_entries += master_config["file_roots"]["prod"]
    verify_env_entries += master_config["pillar_roots"]["base"]
    verify_env_entries += master_config["pillar_roots"]["prod"]

    salt.utils.verify.verify_env(verify_env_entries, username, pki_dir=master_config["pki_dir"])


def pytest_saltfactories_master_write_configuration(request, master_config):
    """
    This hook is called to verify the provided master configuration
    """
    config_file = master_config.pop("conf_file")
    log.debug(
        "Writing to configuration file %s. Configuration:\n%s",
        config_file,
        pprint.pformat(master_config),
    )

    # Write down the computed configuration into the config file
    with salt.utils.files.fopen(config_file, "w") as wfh:
        salt.utils.yaml.safe_dump(master_config, wfh, default_flow_style=False)

    # Make sure to load the config file as a salt-master starting from CLI
    options = salt.config.master_config(config_file)
    return options


def pytest_saltfactories_syndic_verify_configuration(request, syndic_config, username):
    """
    This hook is called to verify the provided syndic configuration
    """
    # verify env to make sure all required directories are created and have the
    # right permissions
    verify_env_entries = [
        str(pathlib.Path(syndic_config["syndic_log_file"]).parent),
    ]
    salt.utils.verify.verify_env(
        verify_env_entries, username,
    )


def pytest_saltfactories_syndic_write_configuration(request, syndic_config):
    """
    This hook is called to verify the provided syndic configuration
    """
    config_file = syndic_config.pop("conf_file")
    log.debug(
        "Writing to configuration file %s. Configuration:\n%s",
        config_file,
        pprint.pformat(syndic_config),
    )

    # Write down the computed configuration into the config file
    with salt.utils.files.fopen(config_file, "w") as wfh:
        salt.utils.yaml.safe_dump(syndic_config, wfh, default_flow_style=False)

    conf_dir = pathlib.Path(config_file).parent.parent
    master_config_file = str(conf_dir / "master")
    minion_config_file = str(conf_dir / "minion")

    # Make sure to load the config file as a salt-master starting from CLI
    options = salt.config.syndic_config(master_config_file, minion_config_file)
    return options


def pytest_saltfactories_proxy_minion_verify_configuration(request, proxy_minion_config, username):
    """
    This hook is called to verify the provided proxy_minion configuration
    """
    # verify env to make sure all required directories are created and have the
    # right permissions
    verify_env_entries = [
        str(pathlib.Path(proxy_minion_config["log_file"]).parent),
        # proxy_proxy_minion_config['extension_modules'],
        proxy_minion_config["sock_dir"],
    ]
    salt.utils.verify.verify_env(
        verify_env_entries, username, pki_dir=proxy_minion_config["pki_dir"]
    )


def pytest_saltfactories_proxy_minion_write_configuration(request, proxy_minion_config):
    """
    This hook is called to verify the provided proxy_minion configuration
    """
    config_file = proxy_minion_config.pop("conf_file")
    log.debug(
        "Writing to configuration file %s. Configuration:\n%s",
        config_file,
        pprint.pformat(proxy_minion_config),
    )

    # Write down the computed configuration into the config file
    with salt.utils.files.fopen(config_file, "w") as wfh:
        salt.utils.yaml.safe_dump(proxy_minion_config, wfh, default_flow_style=False)

    # Make sure to load the config file as a salt-master starting from CLI
    options = salt.config.proxy_config(
        config_file, minion_id=proxy_minion_config["id"], cache_minion_id=True
    )
    return options


def pytest_saltfactories_handle_key_auth_event(
    factories_manager, master_id, minion_id, keystate, payload
):
    """
    This hook is called for every auth event on the masters
    """
    salt_key_cli = factories_manager.get_salt_key_cli(master_id)
    if keystate == "pend":
        ret = salt_key_cli.run("--yes", "--accept", minion_id)
        assert ret.exitcode == 0
