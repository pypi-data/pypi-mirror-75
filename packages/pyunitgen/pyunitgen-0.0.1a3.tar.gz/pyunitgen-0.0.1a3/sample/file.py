from unittest import TestCase
from os import listdir
from application.object.file import File


class TestFile(TestCase):

    def test_glob(self):
        test_directory = "../blackcreek-standalone"
        file_object = File()
        file_object.refactor_file(test_directory)

        self.assertEqual(True, True)
