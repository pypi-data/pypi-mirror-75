from sample.animal import Animal
import unittest

		
class AnimalTest(unittest.TestCase):
    """
    Tests for methods in the Animal class.
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
		
    def test_getSpecies(self):
        
        animal = Animal()
        animal_getSpecies = animal.getSpecies() 
        
        self.assertIsNone(animal_getSpecies) 
		