from sample.test import AnchorPeer
import unittest

		
class AnchorPeerTest(unittest.TestCase):
    """
    Tests for methods in the AnchorPeer class.
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
		
    def test_dump(self):
        
        anchorpeer = AnchorPeer()
        anchorpeer_dump = anchorpeer.dump() 
        
        self.assertIsNone(anchorpeer_dump) 

    def test_test_unit_that_return_dict(self):
        
        anchorpeer = AnchorPeer()
        anchorpeer_test_unit_that_return_dict = anchorpeer.test_unit_that_return_dict() 
        
        self.assertEqual(anchorpeer_test_unit_that_return_dict, {"name":4}) 

    def test_test_unit_that_return_dict_with_a_dictionary_type(self):
        
        anchorpeer = AnchorPeer()
        anchorpeer_test_unit_that_return_dict_with_a_dictionary_type = anchorpeer.test_unit_that_return_dict_with_a_dictionary_type() 
        
        self.assertEqual(anchorpeer_test_unit_that_return_dict_with_a_dictionary_type, {"name":4}) 

    def test_test_unit_with_email(self):
        
        anchorpeer = AnchorPeer()
        anchorpeer_test_unit_with_email=anchorpeer.test_unit_with_email(test1='lbrown@hotmail.com') 
        
        self.assertTrue(anchorpeer_test_unit_with_email,True)

    def test_test_unit_with_default_test2_value_and_string(self):
        
        anchorpeer = AnchorPeer()
        anchorpeer_test_unit_with_default_test2_value_and_string=anchorpeer.test_unit_with_default_test2_value_and_string(test1='Alexander',test2='Fangnikoue') 
        
        self.assertTrue(anchorpeer_test_unit_with_default_test2_value_and_string,True)

    def test_test_unit_with_number_and_string(self):
        
        anchorpeer = AnchorPeer()
        anchorpeer_test_unit_with_number_and_string=anchorpeer.test_unit_with_number_and_string(test1='Reginald',test2=2148287) 
        
        self.assertTrue(anchorpeer_test_unit_with_number_and_string,True)

    def test_test_unit_with_address(self):
        
        anchorpeer = AnchorPeer()
        anchorpeer_test_unit_with_address=anchorpeer.test_unit_with_address(address='39193 Barton Key') 
        
        self.assertTrue(anchorpeer_test_unit_with_address,True)

    def test_test_unit_with_boolean_and_string(self):
        
        anchorpeer = AnchorPeer()
        anchorpeer_test_unit_with_boolean_and_string=anchorpeer.test_unit_with_boolean_and_string(test1='Larry Fitzpatrick',test2=False) 
        
        self.assertTrue(anchorpeer_test_unit_with_boolean_and_string,True)

    def test_test_unit_that_return_a_list(self):
        
        anchorpeer = AnchorPeer()
        anchorpeer_test_unit_that_return_a_list = anchorpeer.test_unit_that_return_a_list() 
        
        self.assertEqual(anchorpeer_test_unit_that_return_a_list, ['1', '2', '3', '4']) 

    def test_test_unit_that_return_a_list_with_a_list_type(self):
        
        anchorpeer = AnchorPeer()
        anchorpeer_test_unit_that_return_a_list_with_a_list_type = anchorpeer.test_unit_that_return_a_list_with_a_list_type() 
        
        self.assertEqual(anchorpeer_test_unit_that_return_a_list_with_a_list_type, ['1', '2', '3', '4']) 

    def test_test_unit_3(self):
        
        anchorpeer = AnchorPeer()
        anchorpeer_test_unit_3 = anchorpeer.test_unit_3() 
        
        self.assertIsNone(anchorpeer_test_unit_3) 

    def test_test_unit_4(self):
        
        anchorpeer = AnchorPeer()
        anchorpeer_test_unit_4 = anchorpeer.test_unit_4() 
        
        self.assertIsNone(anchorpeer_test_unit_4) 
		