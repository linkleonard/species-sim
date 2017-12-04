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
