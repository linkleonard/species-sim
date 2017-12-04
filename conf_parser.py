from models import (
    Habitat,
    Species,
    SEASON_SPRING,
    SEASON_SUMMER,
    SEASON_FALL,
    SEASON_WINTER,
)


def species_from_config(config):
    attributes = config['attributes']

    species = Species()
    species.name = config['name']
    species.life_span = attributes['life_span']
    species.monthly_food_consumption = attributes['monthly_food_consumption']
    species.monthly_water_consumption = attributes['monthly_water_consumption']

    return species


def habitat_from_config(config):
    habitat = Habitat()
    habitat.name = config['name']
    habitat.monthly_food = config['monthly_food']
    habitat.monthly_water = config['monthly_water']

    config_temperatures = config['average_temperature']
    habitat.average_temperatures[SEASON_SPRING] = config_temperatures['spring']
    habitat.average_temperatures[SEASON_SUMMER] = config_temperatures['summer']
    habitat.average_temperatures[SEASON_FALL] = config_temperatures['fall']
    habitat.average_temperatures[SEASON_WINTER] = config_temperatures['winter']

    return habitat
