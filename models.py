GENDER_MALE = 'male'
GENDER_FEMALE = 'female'
GENDER_UNKNOWN = None

DEATH_OLD_AGE = 'old age'


class Animal(object):
    def __init__(self):
        self.gender = GENDER_UNKNOWN

        # Month number when an animal was born.
        self.birth_month = 0


class SimulationStep(object):
    def __init__(self):
        self.males = []
        self.females = []

        self.deaths = {}


class Species(object):
    def __init__(self):
        self.name = ''
        # Life span in years
        self.life_span = 0
