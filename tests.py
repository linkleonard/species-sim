from models import (
    DEATH_OLD_AGE,
    DEATH_STARVATION,
    GENDER_MALE,
    GENDER_FEMALE,
    Animal,
    Habitat,
    SimulationStep,
    Species,
)
from unittest import TestCase
from main import get_new_animals_from_breeding, advance, split_animals_by_birth_month


class BreedingTest(TestCase):
    def test(self):
        month = 1
        animals = tuple(get_new_animals_from_breeding(1, month))
        self.assertEqual(1, len(animals))

        animal = animals[0]
        self.assertEqual(month, animal.birth_month)

    # TODO: Test that animals are placed in the right list, depending on
    # generated gender


class DeathTest(TestCase):
    def test_old_age(self):
        month = 13
        animal = Animal()

        # Males cannot reproduce, so we can use them to test if they will die
        # correctly.
        simulation_step = SimulationStep()
        simulation_step.animals = [animal]

        species = Species()
        species.life_span = 1

        habitat = {}

        next_step = advance(simulation_step, species, habitat, month)
        self.assertEqual(0, len(next_step.animals))
        self.assertIn(DEATH_OLD_AGE, next_step.deaths)

    def test_starvation(self):
        month = 3
        animal = Animal()

        # Males cannot reproduce, so we can use them to test if they will die
        # correctly.
        simulation_step = SimulationStep()
        simulation_step.animals = [animal]

        species = Species()
        species.life_span = 100
        species.monthly_food_consumption = 1

        habitat = Habitat()
        habitat.monthly_food = 0

        next_step = advance(simulation_step, species, habitat, month)
        self.assertEqual(0, len(next_step.animals))
        self.assertIn(DEATH_STARVATION, next_step.deaths)

    def test_no_death(self):
        month = 0
        animal = Animal()

        # Males cannot reproduce, so we can use them to test if they will die
        # correctly.
        simulation_step = SimulationStep()
        simulation_step.animals = [animal]

        species = Species()
        species.life_span = 100
        species.monthly_food_consumption = 1

        habitat = Habitat()
        habitat.monthly_food = 1

        next_step = advance(simulation_step, species, habitat, month)
        self.assertEqual(1, len(next_step.animals))
        self.assertEqual(0, len(next_step.deaths))


class SplitAnimalsByBirthMonthTest(TestCase):
    def test_lower(self):
        animal = Animal()
        animal.birth_month = 0
        animals = [animal]

        month_cutoff = 1

        (before, after) = split_animals_by_birth_month(animals, month_cutoff)
        self.assertEqual(1, len(before))
        self.assertEqual(0, len(after))
