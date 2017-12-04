from models import Habitat, Species


def species_from_config(config):
    attributes = config['attributes']

    species = Species()
    species.name = config['name']
    species.life_span = attributes['life_span']
    species.monthly_food_consumption = attributes['monthly_food_consumption']

    return species


def habitat_from_config(config):
    habitat = Habitat()
    habitat.name = config['name']
    habitat.monthly_food = config['monthly_food']

    return habitat
