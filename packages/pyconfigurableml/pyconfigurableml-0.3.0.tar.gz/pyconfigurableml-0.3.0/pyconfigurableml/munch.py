'''
Logic for converting "nested Python objects" to JavaScript-style objects.
'''


from typeguard import typechecked
from pyconfigurableml._core import run_with_specified_config


@run_with_specified_config(__name__)
@typechecked
def munchify(config, inner_config: bool):
    '''
    Decide (using `inner_config`) whether to apply `munchify_transform` to
    `config`, and do so if necessary.
    '''
    if inner_config:
        config = munchify_transform(config)

    return config


def munchify_transform(config):
    '''
    Convert a nested dictionary into a JavaScript-style object (Munch).
    '''
    from munch import DefaultMunch
    return DefaultMunch.fromDict(config)
