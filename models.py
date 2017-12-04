from math import floor

GENDER_MALE = 'male'
GENDER_FEMALE = 'female'
GENDER_UNKNOWN = None

DEATH_OLD_AGE = 'old age'
DEATH_STARVATION = 'starvation'
DEATH_THIRST = 'thirst'
DEATH_TOO_HOT = 'too hot'
DEATH_TOO_COLD = 'too cold'

SEASON_SPRING = 'spring'
SEASON_SUMMER = 'summer'
SEASON_FALL = 'fall'
SEASON_WINTER = 'winter'


class Animal(object):
    def __init__(self):
        self.gender = GENDER_UNKNOWN

        # Month number when an animal was born.
        self.birth_month = 0
        self.last_feed_month = -1
        self.last_drink_month = -1

        self.consecutive_hot_months = 0
        self.consecutive_cold_months = 0


class SimulationStep(object):
    def __init__(self):
        self.animals = []
        self.deaths = {}
        self.month = 0

    def get_current_season(self):
        seasons_by_index = [
            SEASON_SPRING,
            SEASON_SUMMER,
            SEASON_FALL,
            SEASON_WINTER,
        ]
        month = self.month % 12
        return seasons_by_index[floor(month / 3)]


class StepCheck(object):
    name = 'Check Name'
    death_type = None

    def update(self, animal):
        pass

    def is_still_alive(self, animal):
        return True


class AgeCheck(StepCheck):
    name = 'Age'
    death_type = DEATH_OLD_AGE

    def __init__(self):
        self.minimum_birth_month = 0

    def is_still_alive(self, animal):
        return animal.birth_month >= self.minimum_birth_month


class ResourceCheck(StepCheck):
    resource_field = ''

    def __init__(self):
        self.resource = 0
        self.consumption = 0
        self.simulation_month = 0
        self.minimum_month = 0

    def update(self, animal):
        if self.resource >= self.consumption:
            setattr(animal, self.resource_field, self.simulation_month)
            self.resource -= self.consumption

    def is_still_alive(self, animal):
        return getattr(animal, self.resource_field) >= self.minimum_month


class FoodCheck(ResourceCheck):
    name = 'Food'
    death_type = DEATH_STARVATION
    resource_field = 'last_feed_month'


class DrinkCheck(ResourceCheck):
    name = 'Drink'
    death_type = DEATH_THIRST
    resource_field = 'last_drink_month'


class Species(object):
    def __init__(self):
        self.name = ''
        # Life span in years
        self.life_span = 0
        self.monthly_food_consumption = 0
        self.monthly_water_consumption = 0
        self.minimum_temperature = 0
        self.maximum_temperature = 0


class Habitat(object):
    def __init__(self):
        self.name = ''
        self.monthly_food = 0
        self.monthly_water = 0
        self.average_temperatures = {
            SEASON_SPRING: 0,
            SEASON_SUMMER: 0,
            SEASON_FALL: 0,
            SEASON_WINTER: 0,
        }
