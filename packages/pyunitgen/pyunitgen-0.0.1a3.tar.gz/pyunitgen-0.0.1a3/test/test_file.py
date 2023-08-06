from sample.file import TestFile
import unittest

		
class TestFileTest(unittest.TestCase):
    """
    Tests for methods in the TestFile class.
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
		
    def test_test_glob(self):
        
        testfile = TestFile()
        testfile_test_glob = testfile.test_glob() 
        
        self.assertIsNone(testfile_test_glob) 
		