from os import system
from unittest import TestCase
from semaine12 import is_interaction_file


class TestMethods(TestCase):

    def test_file_does_not_exists(self):
        "Tests when file does not exists"
        self.assertFalse(is_interaction_file("test_files/test00.txt"))

    def test_file_without_number(self):
        "Tests a file without its number of interactions at first line"
        self.assertFalse(is_interaction_file("test_files/test01.txt"))

    def test_file_incorrect_number(self):
        "Tests a file with incorrect number of interactions at first line"
        self.assertFalse(is_interaction_file("test_files/test02.txt"))

    def test_file_empty(self):
        "Tests a file which is empty"
        self.assertFalse(is_interaction_file("test_files/test03.txt"))

    def test_default_file(self):
        "Tests the file which was given as toy example"
        self.assertTrue(is_interaction_file("test_files/toy_example.txt"))

    def test_human_file(self):
        "Tests the file which was given as human example"
        self.assertTrue(is_interaction_file(
            "test_files/Human_HighQuality.txt"))

    def test_correct_file(self):
        "Tests a file with a single interaction"
        self.assertTrue(is_interaction_file("test_files/test_04.txt"))


if __name__ == "__main__":
    system("python -m unittest -v unit_tests.py")
