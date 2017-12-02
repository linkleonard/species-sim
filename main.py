from argparse import ArgumentParser
import os.path
import yaml


def simulate_species_in_habitat(species, habitat, simulation_years):
    for year in range(simulation_years):
        pass


def main():
    parser = get_argument_parser()
    arguments = parser.parse_args()
    config_path = os.path.abspath(arguments.config)

    # TODO: Do we need to validate the configuration file?
    with open(config_path) as config_file:
        configuration = yaml.safe_load(config_file)

    species_list = configuration['species']
    habitats = configuration['habitats']

    simulation_years = 100
    for species in species_list:
        for habitat in habitats:
            simulate_species_in_habitat(species, habitat, simulation_years)


def get_argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        'config',
        help='Path to a YAML environment configuration file',
    )
    return parser


if __name__ == '__main__':
    main()
