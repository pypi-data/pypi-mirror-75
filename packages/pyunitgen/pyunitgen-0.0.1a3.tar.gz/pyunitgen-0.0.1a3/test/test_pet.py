from sample.pet import Pet,Dog
import unittest

		
class PetTest(unittest.TestCase):
    """
    Tests for methods in the Pet class.
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
		
    def test_get_name(self):
        
        pet = Pet('Robert Williams','Dalton Madden')
        pet_get_name = pet.get_name() 
        
        self.assertEqual(pet_get_name, 'Robert Williams') 

    def test_lower(self):
        
        pet_lower=Pet.lower(s='April Flowers')
        
        self.assertEqual(pet_lower, 'april flowers') 
		