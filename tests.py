from models import (
    DEATH_OLD_AGE,
    DEATH_STARVATION,
    DEATH_THIRST,
    DEATH_TOO_HOT,
    DEATH_TOO_COLD,
    GENDER_FEMALE,
    Animal,
    Habitat,
    SimulationStep,
    Species,
    SEASON_SPRING,
    SEASON_SUMMER,
    SEASON_FALL,
    SEASON_WINTER,
)
from unittest import TestCase
from main import (
    get_new_animals_from_breeding,
    advance,
    separate_alive_from_dead,
    breed_animals,
)


class GetNewAnimalsFromBreedingTest(TestCase):
    def test(self):
        month = 1
        animals = tuple(get_new_animals_from_breeding(1, month))
        self.assertEqual(1, len(animals))

        animal = animals[0]
        self.assertEqual(month, animal.birth_month)

    # TODO: Test that animals are placed in the right list, depending on
    # generated gender


class BreedAnimalsTest(TestCase):
    def test_start_breeding(self):
        simulation_step = SimulationStep()

        animal = Animal()
        animal.gender = GENDER_FEMALE
        animal.gestation_months = 0

        species = Species()
        species.gestation_months = 1

        new_animals = tuple(breed_animals([animal], species, simulation_step))
        self.assertEqual(1, animal.gestation_months)
        self.assertEqual(0, len(new_animals))

    def test_mid_breeding(self):
        simulation_step = SimulationStep()

        animal = Animal()
        animal.gender = GENDER_FEMALE
        animal.gestation_months = 1

        species = Species()
        species.gestation_months = 2

        new_animals = tuple(breed_animals([animal], species, simulation_step))
        self.assertEqual(2, animal.gestation_months)
        self.assertEqual(0, len(new_animals))

    def test_finish_breeding(self):
        simulation_step = SimulationStep()

        animal = Animal()
        animal.gender = GENDER_FEMALE
        animal.gestation_months = 1

        species = Species()
        species.gestation_months = 1

        new_animals = tuple(breed_animals([animal], species, simulation_step))
        self.assertEqual(0, animal.gestation_months)
        self.assertEqual(1, len(new_animals))


class AdvanceTest(TestCase):
    def test_feed(self):
        animals = [Animal(), Animal()]

        # Males cannot reproduce, so we can use them to test if they will die
        # correctly.
        simulation_step = SimulationStep()
        simulation_step.month = 4
        simulation_step.animals = animals

        species = Species()
        species.life_span = 1
        species.monthly_food_consumption = 1

        habitat = Habitat()
        habitat.monthly_food = 1

        next_step = advance(simulation_step, species, habitat)
        # One animal should have died due to starvation from not enough food
        self.assertEqual(1, len(next_step.animals))
        self.assertIn(DEATH_STARVATION, next_step.deaths)

    def test_old_age(self):
        animal = Animal()

        # Males cannot reproduce, so we can use them to test if they will die
        # correctly.
        simulation_step = SimulationStep()
        simulation_step.month = 13
        simulation_step.animals = [animal]

        species = Species()
        species.life_span = 1

        habitat = Habitat()

        next_step = advance(simulation_step, species, habitat)
        self.assertEqual(0, len(next_step.animals))
        self.assertIn(DEATH_OLD_AGE, next_step.deaths)

    def test_starvation(self):
        animal = Animal()

        # Males cannot reproduce, so we can use them to test if they will die
        # correctly.
        simulation_step = SimulationStep()
        simulation_step.month = 3
        simulation_step.animals = [animal]

        species = Species()
        species.life_span = 100
        species.monthly_food_consumption = 1

        habitat = Habitat()
        habitat.monthly_food = 0

        next_step = advance(simulation_step, species, habitat)
        self.assertEqual(0, len(next_step.animals))
        self.assertIn(DEATH_STARVATION, next_step.deaths)

    def test_thirst(self):
        animal = Animal()

        # Males cannot reproduce, so we can use them to test if they will die
        # correctly.
        simulation_step = SimulationStep()
        simulation_step.month = 3
        simulation_step.animals = [animal]

        species = Species()
        species.life_span = 100
        species.monthly_water_consumption = 1

        habitat = Habitat()
        habitat.monthly_water = 0

        next_step = advance(simulation_step, species, habitat)
        self.assertEqual(0, len(next_step.animals))
        self.assertIn(DEATH_THIRST, next_step.deaths)

    def test_no_death(self):
        animal = Animal()

        # Males cannot reproduce, so we can use them to test if they will die
        # correctly.
        simulation_step = SimulationStep()
        simulation_step.animals = [animal]

        species = Species()
        species.life_span = 100
        species.monthly_food_consumption = 1
        species.monthly_food_consumption = 1

        habitat = Habitat()
        habitat.monthly_food = 1
        habitat.monthly_water = 1

        next_step = advance(simulation_step, species, habitat)
        self.assertEqual(1, len(next_step.animals))
        self.assertEqual(0, len(next_step.deaths))

    def test_too_hot(self):
        animal = Animal()
        animal.consecutive_hot_months = 1

        # Males cannot reproduce, so we can use them to test if they will die
        # correctly.
        simulation_step = SimulationStep()
        simulation_step.animals = [animal]

        species = Species()
        species.life_span = 100
        species.minimum_temperature = 100
        species.maximum_temperature = 200

        habitat = Habitat()
        habitat.monthly_food = 1
        habitat.monthly_water = 1
        habitat.average_temperatures[SEASON_SPRING] = 1000

        next_step = advance(simulation_step, species, habitat)
        self.assertEqual(0, len(next_step.animals))
        self.assertIn(DEATH_TOO_HOT, next_step.deaths)

    def test_too_cold(self):
        animal = Animal()
        animal.consecutive_cold_months = 1

        # Males cannot reproduce, so we can use them to test if they will die
        # correctly.
        simulation_step = SimulationStep()
        simulation_step.animals = [animal]

        species = Species()
        species.life_span = 100
        species.minimum_temperature = 100
        species.maximum_temperature = 200

        habitat = Habitat()
        habitat.monthly_food = 1
        habitat.monthly_water = 1
        habitat.average_temperatures[SEASON_SPRING] = -1000

        next_step = advance(simulation_step, species, habitat)
        self.assertEqual(0, len(next_step.animals))
        self.assertIn(DEATH_TOO_COLD, next_step.deaths)


class SeparateAliveFromDeadTest(TestCase):
    def test_dead(self):
        animals = [Animal()]

        (alive, dead) = separate_alive_from_dead(animals, lambda x: True)
        self.assertEqual(1, len(alive))
        self.assertEqual(0, len(dead))

    def test_alive(self):
        animals = [Animal()]

        (alive, dead) = separate_alive_from_dead(animals, lambda x: False)
        self.assertEqual(0, len(alive))
        self.assertEqual(1, len(dead))


class SimulationStepTest(TestCase):
    def test_get_current_season(self):
        months_in_seasons = {
            SEASON_SPRING: [0, 1, 2],
            SEASON_SUMMER: [3, 4, 5],
            SEASON_FALL: [6, 7, 8],
            SEASON_WINTER: [9, 10, 11],
        }
        for season, months in months_in_seasons.items():
            for month in months:
                with self.subTest(month=month):
                    simulation_step = SimulationStep()
                    simulation_step.month = month
                    self.assertEqual(
                        season,
                        simulation_step.get_current_season(),
                    )
