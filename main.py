from argparse import ArgumentParser
import os.path
import yaml
from models import (
    DEATH_OLD_AGE,
    DEATH_STARVATION,
    GENDER_MALE,
    GENDER_FEMALE,
    SimulationStep,
    Animal,
)
from random import random
from conf_parser import species_from_config

male_ratio = 0.5


def get_initial_simulation_step():
    male = Animal()
    male.gender = GENDER_MALE

    female = Animal()
    female.gender = GENDER_FEMALE

    simulation_step = SimulationStep()
    simulation_step.animals.append(male)
    simulation_step.animals.append(female)
    return simulation_step


def simulate_species_in_habitat(species, habitat, simulation_years):
    simulation_step = get_initial_simulation_step()

    for month in range(simulation_years * 12):
        simulation_step = advance(simulation_step, species, habitat)
        # TODO: Do stats tracking for each simulation step

    # TODO: Return stats


def advance(simulation_step, species, habitat):
    next_step = SimulationStep()

    next_month = simulation_step.month + 1
    next_step.month = next_month

    # Copy over the existing animals
    MONTHS_IN_YEAR = 12

    alive_animals = simulation_step.animals

    alive_cutoff_birth_month = next_month - species.life_span * MONTHS_IN_YEAR
    (dead_age_animals, alive_animals) = split_animals_by_birth_month(
        alive_animals,
        alive_cutoff_birth_month,
    )

    if dead_age_animals:
        next_step.deaths[DEATH_OLD_AGE] = dead_age_animals

    remaining_food = habitat.monthly_food
    for animal in alive_animals:
        if remaining_food >= species.monthly_food_consumption:
            remaining_food -= species.monthly_food_consumption
            animal.last_feed_month = simulation_step.month

    alive_cutoff_feed_month = next_month - 3
    (starved_animals, alive_animals) = split_animals_by_last_feed_month(
        alive_animals,
        alive_cutoff_feed_month,
    )

    if starved_animals:
        next_step.deaths[DEATH_STARVATION] = starved_animals

    next_step.animals = alive_animals

    # TODO: Probably should add a test condition, to not spawn if there are
    # no males
    females = tuple(
        animal
        for animal in next_step.animals
        if animal.gender == GENDER_FEMALE
    )
    next_step.animals += get_new_animals_from_breeding(
        len(females),
        next_month,
    )

    return next_step


def split_animals_by_birth_month(animals, birth_month):
    before = []
    after = []
    for animal in animals:
        if animal.birth_month <= birth_month:
            before.append(animal)
        else:
            after.append(animal)
    return (before, after)


def split_animals_by_last_feed_month(animals, month):
    before = []
    after = []
    for animal in animals:
        if animal.last_feed_month <= month:
            before.append(animal)
        else:
            after.append(animal)
    return (before, after)


def get_new_animals_from_breeding(count, month):
    for female in range(count):
        gender = get_new_animal_gender()

        born_animal = Animal()
        born_animal.birth_month = month
        born_animal.last_feed_month = month - 1
        born_animal.gender = gender

        yield born_animal


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

    species_list = tuple(
        species_from_config(config)
        for config in configuration['species']
    )
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
