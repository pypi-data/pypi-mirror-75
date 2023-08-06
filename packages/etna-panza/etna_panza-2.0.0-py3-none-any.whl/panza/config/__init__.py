"""
Module providing helpers for panza's configuration
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AdditionalDockerDaemonConfiguration:
    network_bridge_mask: str
    # TODO: add support for picking custom DNS servers


@dataclass
class PanzaConfiguration:
    root_directory: str
    additional_docker_daemon: AdditionalDockerDaemonConfiguration


_config: Optional[PanzaConfiguration] = None


def init_config(config: PanzaConfiguration):
    """
    Initialize the configuration with given values

    :param config:                  the configuration to use for Panza
    """
    global _config
    _config = config


def get_config() -> PanzaConfiguration:
    """
    Retrieve the configuration
    """
    return _config
