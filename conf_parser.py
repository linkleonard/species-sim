from models import Species


def species_from_config(config):
    species = Species()
    species.life_span = config['attributes']['life_span']

    return species
