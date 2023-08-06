from sample.person import Person
import unittest

		
class PersonTest(unittest.TestCase):
    """
    Tests for methods in the Person class.
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
		
    def test_set_name(self):
        
        person = Person()
        person_set_name=person.set_name(user_name='Dr. Tracy Maxwell DDS') 
        
        self.assertEqual('Dr. Tracy Maxwell DDS', person.get_name(0)) 

    def test_get_name(self):
        
        person = Person()
        person_get_name=person.get_name(user_id=1) 
        
        self.assertEqual(person_get_name, 'There is no such user') 
		