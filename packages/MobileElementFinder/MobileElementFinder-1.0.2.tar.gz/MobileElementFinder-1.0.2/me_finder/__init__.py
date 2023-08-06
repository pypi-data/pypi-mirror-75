"""Initiate mge_finder cli program."""

import logging
import logging.config
from io import BytesIO

import yaml
from pkg_resources import resource_string

from .version import __version__

# read logging config from package resource
LOGGER_CONFIG = resource_string(__name__, 'logging.yml')


def _setup_logger(cfg_path):
    """Read logging config."""
    yml = yaml.safe_load(BytesIO(LOGGER_CONFIG))
    logging.config.dictConfig(yml)


_setup_logger(LOGGER_CONFIG)
