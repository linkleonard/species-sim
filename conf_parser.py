from models import Habitat, Species


def species_from_config(config):
    species = Species()
    species.life_span = config['attributes']['life_span']

    return species


def habitat_from_config(config):
    habitat = Habitat()
    habitat.monthly_food = config['monthly_food']

    return habitat
