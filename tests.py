from models import (
    DEATH_OLD_AGE,
    GENDER_MALE,
    GENDER_FEMALE,
    Animal,
    SimulationStep,
    Species,
)
from unittest import TestCase
from main import get_new_animals_from_breeding, advance, split_animals_by_birth_month


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


class DeathTest(TestCase):
    def test(self):
        month = 13
        animal = Animal()

        # Males cannot reproduce, so we can use them to test if they will die
        # correctly.
        simulation_step = SimulationStep()
        simulation_step.males = [animal]

        species = Species()
        species.life_span = 1

        habitat = {}

        next_step = advance(simulation_step, species, habitat, month)
        self.assertEqual(0, len(next_step.males + next_step.females))
        self.assertIn(DEATH_OLD_AGE, next_step.deaths)


class SplitAnimalsByBirthMonthTest(TestCase):
    def test_lower(self):
        animal = Animal()
        animal.birth_month = 0
        animals = [animal]

        month_cutoff = 1

        (before, after) = split_animals_by_birth_month(animals, month_cutoff)
        self.assertEqual(1, len(before))
        self.assertEqual(0, len(after))
