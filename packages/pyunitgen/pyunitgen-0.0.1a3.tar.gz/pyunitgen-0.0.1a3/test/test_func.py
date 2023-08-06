from sample.func import name,set_username,get_username,test_boolean_true,test_boolean_false
import unittest

		
class funcTest(unittest.TestCase):
    """
    Tests for functions in the "func" file.
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
		
    def test_name(self):
        
        func = name() 
        
        self.assertEqual(func, 'Evarist') 

    def test_set_username(self):
        
        func = set_username(name='Mandy Owens') 
        
        self.assertTrue(func,True)

    def test_test_boolean_true(self):
        
        func = test_boolean_true(first_name='Gregory Sanchez') 
        
        self.assertTrue(func,True)

    def test_test_boolean_false(self):
        
        func = test_boolean_false(first_name='Lauren Brooks') 
        
        self.assertFalse(func,False)
		