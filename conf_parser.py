from models import Habitat, Species


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

    return habitat
