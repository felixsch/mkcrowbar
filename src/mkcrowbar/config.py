import os
import yaml

from mkcrowbar.pretty import fatal


def load(path=None):
    if not path:
        path = os.environ.get('MKCROWBAR_CONFIG')

    if not path:
        fatal('You need to specify a configuration file')

    if not os.path.isfile(path):
        fatal('Could not open configuration file (No such file)')

    try:
        config = yaml.safe_load(open(path))
        validate(config)
    except yaml.scanner.ScannerError as e:
        fatal('Parsing configuration file failed: {}'.format(e))

    return config


def validate(config):
    required = ['hostname', 'interface']

    for key in required:
        if key not in config:
            fatal("Configuration option '{}' is mandatory. Please update your configuration".format(key))
