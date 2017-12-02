from argparse import ArgumentParser
import os.path
import yaml


def main():
    parser = get_argument_parser()
    arguments = parser.parse_args()
    config_path = os.path.abspath(arguments.config)

    # TODO: Do we need to validate the configuration file?
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

    # TODO: Until we actually run an import, just print out the config so we're
    # doing *something*.
    print(config)


def get_argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        'config',
        help='Path to a YAML environment configuration file',
    )
    return parser


if __name__ == '__main__':
    main()
