GENDER_MALE = 'male'
GENDER_FEMALE = 'female'
GENDER_UNKNOWN = None


class Animal(object):
    def __init__(self):
        self.gender = GENDER_UNKNOWN

        # Month number when an animal was born.
        self.birth_month = 0


class SimulationStep(object):
    def __init__(self):
        self.males = []
        self.females = []
