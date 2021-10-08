import datetime
import logging
import os
from pathlib import Path

import yaml
from string import Template

ASSETS_DIR = Path(__file__).parent / "../assets"
DEFAULT_CONFIG_DIR = ASSETS_DIR / "config"

logger = logging.getLogger(__name__)


class Config(dict):

    def __init__(self, *config_files):
        super().__init__()

        if not config_files:
            config_files = ['DEFAULT_DATA_SOURCES', 'DEFAULT_DATA_MAP']

        for file in config_files:
            if file == "DEFAULT_DATA_SOURCES":
                file = DEFAULT_CONFIG_DIR / "annex-a-merge.yml"
            elif file == "DEFAULT_DATA_MAP":
                file = DEFAULT_CONFIG_DIR / "data-map.yml"
            self.load_config(file, conditional=False)

        self['config_date'] = datetime.datetime.now().isoformat()
        try:
            self['username'] = os.getlogin()
        except OSError:
            # This happens when tests are not run under a login shell, e.g. CI pipeline
            pass

    def load_config(self, filename, conditional=False, warn=False):
        """
        Load configuration from yaml file. Any loaded configuration
        is only set if the values don't already exist in CONFIG.

        Files can contain ${} placeholders following the Python string.Template format.
        The context will include any keys already existing in the configuration, any keys
        from the current file - however, if these include placeholders, the placeholders
        will not be replaced. Finally, environment variables can be referenced with
        `os_environ_VARIABLE_NAME`.

        Keyword arguments:
        filename -- Filename to load from
        conditional -- If True, ignore file if it doesn't exist. If False, fail. (default False)
        """
        if conditional and not os.path.isfile(filename):
            if warn:
                logger.warning('Missing optional file {}'.format(filename))

            return

        with open(filename) as FILE:
            user_config = yaml.load(FILE, Loader=yaml.FullLoader)

        logger.info("Loading {} configuration values from '{}'.".format(len(user_config), filename))

        environment_dict = {'os_environ_{}'.format(k): v for k, v in os.environ.items()}

        variables = dict(self)
        variables.update(user_config)
        variables.update(environment_dict)

        with open(filename, 'rt') as FILE:
            user_config_string = FILE.read()

        user_config_template = Template(user_config_string)
        user_config_string = user_config_template.substitute(variables)

        user_config = yaml.load(user_config_string, Loader=yaml.FullLoader)

        self.update(user_config)


class ConfigError(UserWarning):
    """
    An error with a configuration, such as a missing or invalid value.
    """
