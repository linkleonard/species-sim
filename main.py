from argparse import ArgumentParser
import os.path
import yaml
import logging
from models import (
    DEATH_OLD_AGE,
    DEATH_STARVATION,
    DEATH_THIRST,
    DEATH_TOO_COLD,
    DEATH_TOO_HOT,
    GENDER_MALE,
    GENDER_FEMALE,
    MONTHS_IN_YEAR,
    SimulationStep,
    Animal,
    AgeCheck,
    FoodCheck,
    DrinkCheck,
    HeatCheck,
    ColdCheck,
)
import sys
from random import random
from conf_parser import habitat_from_config, species_from_config
from random import random

male_ratio = 0.5

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

log_path = os.path.join(
    os.path.dirname(__file__),
    'output.log',
)
logger.addHandler(logging.FileHandler(log_path))


def get_initial_simulation_step():
    male = Animal()
    male.gender = GENDER_MALE

    female = Animal()
    female.gender = GENDER_FEMALE

    simulation_step = SimulationStep()
    simulation_step.animals.append(male)
    simulation_step.animals.append(female)
    return simulation_step


def get_average_population(simulation_steps):
    total = sum(
        len(simulation_step.animals)
        for simulation_step in simulation_steps
    )
    return total / len(simulation_steps)


def get_max_population(simulation_steps):
    generator = (
        len(simulation_step.animals)
        for simulation_step in simulation_steps
    )
    return max(generator, default=0)


def simulate_species_in_habitat(species, habitat, simulation_years):
    simulation_step = get_initial_simulation_step()
    simulation_steps = [simulation_step]

    for month in range(simulation_years * 12):
        simulation_step = advance(simulation_step, species, habitat)
        simulation_steps.append(simulation_step)

        # No reason to continue if no more animals exist
        if not simulation_step.animals:
            break

    return simulation_steps


def advance(simulation_step, species, habitat):
    next_step = SimulationStep()

    next_month = simulation_step.month + 1
    logger.debug('Advancing to step %d', next_month)
    next_step.month = next_month

    # Copy over the existing animals
    alive_animals = simulation_step.animals

    age_check = AgeCheck(simulation_step, species)
    food_check = FoodCheck(simulation_step, habitat, species)
    drink_check = DrinkCheck(simulation_step, habitat, species)

    fluctuation = get_fluctuation()

    season = simulation_step.get_current_season()
    temperature = habitat.average_temperatures[season] + fluctuation
    logger.debug(
        'Current temperature: %d (%d%+d)',
        temperature,
        habitat.average_temperatures[season],
        fluctuation,
    )

    heat_check = HeatCheck(temperature, species)
    cold_check = ColdCheck(temperature, species)

    checks = [age_check, food_check, drink_check, cold_check, heat_check]

    for check in checks:
        for animal in alive_animals:
            check.update(animal)

        (alive_animals, dead_animals) = separate_alive_from_dead(
            alive_animals,
            lambda animal: check.is_still_alive(animal),
        )

        if dead_animals:
            logger.debug('Deaths due to %s: %d', check.name, len(dead_animals))
            next_step.deaths[check.death_type] = dead_animals

    next_step.animals = alive_animals

    # TODO: Probably should add a test condition, to not spawn if there are
    # no males
    females = tuple(
        animal
        for animal in next_step.animals
        if animal.gender == GENDER_FEMALE
    )

    born_animals = tuple(breed_animals(females, species, simulation_step))
    logger.debug('Animals born: %d', len(born_animals))
    next_step.animals += born_animals

    logger.debug('Population currently at: %d', len(next_step.animals))

    return next_step


def breed_animals(animals, species, simulation_step):
    new_animal_count = 0
    for animal in animals:
        if can_breed(animal, species, simulation_step):
            if animal.gestation_months == species.gestation_months:
                new_animal_count += 1
                animal.gestation_months = 0
            else:
                animal.gestation_months += 1

    return get_new_animals_from_breeding(
        new_animal_count,
        simulation_step.month + 1,
    )


def separate_alive_from_dead(animals, is_animal_alive):
    dead = []
    alive = []
    for animal in animals:
        if is_animal_alive(animal):
            alive.append(animal)
        else:
            dead.append(animal)
    return (alive, dead)


def get_new_animals_from_breeding(count, month):
    for female in range(count):
        gender = get_new_animal_gender()

        born_animal = Animal()
        born_animal.birth_month = month
        born_animal.last_feed_month = month - 1
        born_animal.gender = gender

        yield born_animal


def get_fluctuation():
    scale = 10 if random() < 0.95 else 30
    return (random() - 0.5) * scale


def can_breed(animal, species, simulation_step):
    month_age = species.minimum_breeding_age * MONTHS_IN_YEAR
    return simulation_step.month - animal.birth_month >= month_age


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
    output_stream = sys.stdout

    if arguments.output is not None:
        output_stream = open(arguments.output, 'w')

    try:
        # TODO: Do we need to validate the configuration file?
        with open(config_path) as config_file:
            configuration = yaml.safe_load(config_file)

        species_list = tuple(
            species_from_config(config)
            for config in configuration['species']
        )
        habitats = tuple(
            habitat_from_config(config)
            for config in configuration['habitats']
        )

        simulation_years = configuration['years']
        print(
            'Simulation ran for {count:d} years'.format(
                count=simulation_years,
            ),
            file=output_stream,
        )
        for species in species_list:
            print('{name}:'.format(name=species.name), file=output_stream)
            for habitat in habitats:
                print(
                    '\t{name:}:'.format(name=habitat.name),
                    file=output_stream,
                )
                simulation_steps = simulate_species_in_habitat(
                    species,
                    habitat,
                    simulation_years,
                )
                generate_simulation_report(simulation_steps, output_stream)
    finally:
        if arguments.output is not None:
            output_stream.close()


def generate_simulation_report(simulation_steps, output_stream):
    deaths_by_type = {
        DEATH_OLD_AGE: [],
        DEATH_THIRST: [],
        DEATH_STARVATION: [],
        DEATH_TOO_HOT: [],
        DEATH_TOO_COLD: [],
    }
    for simulation_step in simulation_steps:
        for death_reason, animals in simulation_step.deaths.items():
            deaths_by_type[death_reason] += animals

    average_population = get_average_population(simulation_steps)
    max_population = get_max_population(simulation_steps)

    logging.info('Average population: %d', average_population)
    logging.info('Maximum population: %d', max_population)

    total_deaths = sum(len(animals) for animals in deaths_by_type.values())

    total_born = total_deaths + len(simulation_step.animals)
    mortality_rate = total_deaths / total_born

    logging.info('Mortality rate: %.2f%%', mortality_rate * 100)

    lines = [
        '\t\tAverage Population: {count:.2f}'.format(count=average_population),
        '\t\tMax Population: {count:d}'.format(count=max_population),
        '\t\tMortality Rate: {rate:.2f}%'.format(rate=mortality_rate * 100),
        '\t\tCause of Death:',
    ]

    for death_reason, animals in deaths_by_type.items():
        logging.info('Deaths due to %s: %d', death_reason, len(animals))
        if total_deaths > 0:
            percentage = len(animals) / total_deaths * 100
        else:
            percentage = 0
        lines.append('\t\t\t{percentage: 6.2f}%  {reason}'.format(
            percentage=percentage,
            reason=death_reason,
        ))

    print('\n'.join(lines), file=output_stream)


def get_argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        'config',
        help='Path to a YAML environment configuration file',
    )
    parser.add_argument(
        '--output',
        required=False,
        help='Path of output file. If omitted, write to stdout'
    )
    return parser


if __name__ == '__main__':
    main()
