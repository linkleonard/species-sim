from models import GENDER_MALE, GENDER_FEMALE
from unittest import TestCase
from main import get_new_animals_from_breeding


class BreedingTest(TestCase):
    def test(self):
        month = 1
        animals = get_new_animals_from_breeding(1, month)

        self.assertIn(GENDER_FEMALE, animals)
        self.assertIn(GENDER_MALE, animals)

        all_animals = animals[GENDER_FEMALE] + animals[GENDER_MALE]
        self.assertEqual(1, len(all_animals))

        animal = all_animals[0]
        self.assertEqual(month, animal.birth_month)

    # TODO: Test that animals are placed in the right list, depending on
    # generated gender
