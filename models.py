GENDER_MALE = 'male'
GENDER_FEMALE = 'female'
GENDER_UNKNOWN = None

DEATH_OLD_AGE = 'old age'
DEATH_STARVATION = 'starvation'


class Animal(object):
    def __init__(self):
        self.gender = GENDER_UNKNOWN

        # Month number when an animal was born.
        self.birth_month = 0
        self.last_feed_month = -1


class SimulationStep(object):
    def __init__(self):
        self.animals = []
        self.deaths = {}
        self.month = 0


class Species(object):
    def __init__(self):
        self.name = ''
        # Life span in years
        self.life_span = 0
        self.monthly_food_consumption = 0


class Habitat(object):
    def __init__(self):
        self.name = ''
        self.monthly_food = 0
