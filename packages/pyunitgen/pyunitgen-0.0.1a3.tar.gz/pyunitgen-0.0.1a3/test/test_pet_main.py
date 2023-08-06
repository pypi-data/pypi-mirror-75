from sample.pet_main import create_pet,create_pet_with_empty_return_object,create_pet_return_true,create_animal,create_pet_return_false,create_pet_return_none
from sample.pet import Pet as AnimalPet
from sample.pet import Dog
from sample.pet import Pet
from sample.animal import Animal
import unittest

		
class pet_mainTest(unittest.TestCase):
    """
    Tests for functions in the "pet_main" file.
    """

    @classmethod
    def setUpClass(cls):
        pass #TODO

    @classmethod
    def tearDownClass(cls):
        pass #TODO

    def setUp(self):
        pass #TODO

    def tearDown(self):
        pass #TODO
		
    def test_create_pet(self):
        
        pet_main = create_pet(name='Sydney Jones',species='Rachel Jackson',age=8502) 
        
        self.assertEqual(pet_main, Pet('Sydney Jones','Rachel Jackson')) 

    def test_create_pet_with_empty_return_object(self):
        
        pet_main = create_pet_with_empty_return_object(name='Katherine Watson',species='Heather Frost',age=5056) 
        
        self.assertIsInstance(pet_main, Pet) 

    def test_create_pet_return_true(self):
        
        pet_main = create_pet_return_true(name='Michelle Nelson',species='Jessica Alexander',age=7813) 
        
        self.assertEqual(pet_main, 'Michelle Nelson') 

    def test_create_animal(self):
        
        pet_main = create_animal(species='Amanda Rodriguez') 
        
        self.assertIsInstance(pet_main, Animal) 

    def test_create_pet_return_false(self):
        
        pet_main = create_pet_return_false(name='Andrea Ross',species='Scott Ramsey',age=9826) 
        
        self.assertFalse(pet_main,False)

    def test_create_pet_return_none(self):
        
        pet_main = create_pet_return_none(name='Gabrielle Peterson',species='Bruce Peterson',age=838669) 
        
        self.assertFalse(pet_main,False)
		