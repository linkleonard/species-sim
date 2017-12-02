from argparse import ArgumentParser
import os.path
import yaml
from models import GENDER_MALE, GENDER_FEMALE, SimulationStep, Animal
from random import random
from itertools import chain

male_ratio = 0.5


def get_initial_simulation_step():
    male = Animal()
    male.gender = GENDER_MALE

    female = Animal()
    female.gender = GENDER_FEMALE

    simulation_step = SimulationStep()
    simulation_step.males.append(male)
    simulation_step.females.append(female)
    return simulation_step


def simulate_species_in_habitat(species, habitat, simulation_years):
    simulation_step = get_initial_simulation_step()

    for month in range(simulation_years * 12):
        simulation_step = advance(simulation_step, species, habitat, month)
        # TODO: Do stats tracking for each simulation step

    # TODO: Return stats


def advance(simulation_step, species, habitat, month):
    next_step = SimulationStep()
    # Copy over the existing animals
    next_step.males = simulation_step.males[:]
    next_step.females = simulation_step.females[:]

    # TODO: Probably should add a test condition, to not spawn if there are
    # no males
    new_animals = get_new_animals_from_breeding(len(next_step.females), month)
    next_step.males += new_animals[GENDER_MALE]
    next_step.females += new_animals[GENDER_FEMALE]

    return next_step


def get_new_animals_from_breeding(count, month):
    new_females = []
    new_males = []

    for female in range(count):
        gender = get_new_animal_gender()

        born_animal = Animal()
        born_animal.birth_month = month
        born_animal.gender = gender

        if gender == GENDER_FEMALE:
            new_females.append(born_animal)
        else:
            new_males.append(born_animal)

    return {
        GENDER_MALE: new_males,
        GENDER_FEMALE: new_females,
    }


def get_new_animal_gender():
    # The % of male(or female) births may change, so we'll generate random
    # floats between 0 and 1 instead of using choice() to select between two
    # items.
    if random() <= male_ratio:
        return GENDER_MALE
    return GENDER_FEMALE


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
