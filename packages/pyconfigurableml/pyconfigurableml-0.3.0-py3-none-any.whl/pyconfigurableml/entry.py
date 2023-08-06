'''
Utilities around programatic entry point.
'''


# PyLint doesn't recognize that the decorators for, e.g. munchify, change
# method signature.
# pylint: disable=no-value-for-parameter


import argparse
import logging
import os
from typing import Callable
from typeguard import typechecked
import yaml
import pyconfigurableml.azure
import pyconfigurableml.logging
import pyconfigurableml.munch


config_actions = [
    pyconfigurableml.logging.set_logger_levels,
    pyconfigurableml.azure.resolve_azure_secrets,
    pyconfigurableml.munch.munchify
]


@typechecked
def run(main: Callable[[object, logging.Logger], None],
        file: str,
        name: str = '__main__') -> None:
    '''
    Handle log levels and parsing a YAML configuration file. The default
    path to the configuration file is `<caller directory>/config.yml`.

        Parameters:
            main: programatic entry point for your program.
            file: should be __file__ in the entry point of your script.
            name: optionally __name__ in your script. This function will only
                  call main if __name__ == '__main__'.
    '''

    if name == '__main__':
        caller_dir = os.path.dirname(os.path.abspath(file))

        parser = argparse.ArgumentParser()

        parser.add_argument('--config', default=os.path.join(caller_dir, 'config.yml'))
        parser.add_argument('--level', default='INFO')
        args = parser.parse_args()

        with open(args.config, 'r') as config_file:
            config = yaml.safe_load(config_file)

        logging.basicConfig(level=args.level)

        for func in config_actions:
            config = func(config)

        logger = logging.getLogger()
        main(config, logger)
