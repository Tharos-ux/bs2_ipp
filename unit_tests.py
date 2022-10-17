from os import system
from unittest import TestCase
from interactome import Interactome, is_interaction_file
from numpy import ndarray, asarray


class TestObject(TestCase):

    @property
    def interactome(self):
        """ Getter of the attribute interactome. """
        return self.__interactome

    @interactome.setter
    def interactome(self, new_interactome):
        """ Setter of the attribute interactome. """
        if not isinstance(new_interactome, Interactome):
            raise ValueError("Expecting a Interactome")
        self.__interactome = new_interactome

    def __init__(self, *args, **kwargs):
        "Custom constructor"
        super(TestObject, self).__init__(*args, **kwargs)
        self.interactome = Interactome("test_files/toy_example.txt")

    def test_object_instance(self):
        "Tests if object instance is created"
        self.assertTrue(isinstance(self.interactome, Interactome))

    def test_object_file_in_type(self):
        "Tests if interactime.file_in is a str"
        self.assertTrue(isinstance(self.interactome.file_in, str))

    def test_object_file_in_property(self):
        "Tests if interactime.file_in is well initialized"
        self.assertEquals(self.interactome.file_in,
                          "test_files/toy_example.txt")

    def test_object_file_out_type(self):
        "Tests if interactime.file_out is a str"
        self.assertTrue(isinstance(self.interactome.file_out, str))

    def test_object_file_out_property(self):
        "Tests if interactime.file_out is well initialized"
        self.assertEquals(self.interactome.file_out, "clean_int_graph.txt")

    def test_object_int_list_type(self):
        "Tests if interactime.int_list is a list"
        self.assertTrue(isinstance(self.interactome.int_list, list))

    def test_object_int_list_property(self):
        "Tests if interactime.int_list is well initialized"
        self.assertEquals(self.interactome.int_list, [('A', 'B'), ('A', 'C'), ('B', 'C'), (
            'B', 'D'), ('D', 'E'), ('D', 'F'), ('E', 'D'), ('G', 'A'), ('G', 'C'), ('G', 'B')])

    def test_object_int_dict_type(self):
        "Tests if interactime.int_dict is a dict"
        self.assertTrue(isinstance(self.interactome.int_dict, dict))

    def test_object_int_dict_property(self):
        "Tests if interactime.int_dict is well initialized"
        self.assertEquals(self.interactome.int_dict, {'A': ['B', 'C'], 'B': [
                          'C', 'D'], 'D': ['E', 'F'], 'E': ['D'], 'G': ['A', 'C', 'B']})

    def test_object_proteins_type(self):
        "Tests if interactime.proteins is a list"
        self.assertTrue(isinstance(self.interactome.proteins, list))

    def test_object_file_property(self):
        "Tests if interactime.proteins is well initialized"
        self.assertEquals(self.interactome.proteins, [
                          'A', 'B', 'C', 'D', 'E', 'F', 'G'])

    def test_object_mat_type(self):
        "Tests if interactome.mat is an array"
        self.assertTrue(isinstance(self.interactome.int_mat, ndarray))

    def test_object_mat_property(self):
        "Tests if interactome.mat is well initialized"
        self.assertTrue((self.interactome.int_mat & asarray([[0, 1, 1, 0, 0, 0, 1], [1, 0, 1, 1, 0, 0, 1], [1, 1, 0, 0, 0, 0, 1], [
            0, 1, 0, 0, 1, 1, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0]])).any())


class TestIO(TestCase):

    @property
    def interactome(self):
        """ Getter of the attribute interactome. """
        return self.__interactome

    @interactome.setter
    def interactome(self, new_interactome):
        """ Setter of the attribute interactome. """
        if not isinstance(new_interactome, Interactome):
            raise ValueError("Expecting a Interactome")
        self.__interactome = new_interactome

    def __init__(self, *args, **kwargs):
        "Custom constructor"
        super(TestIO, self).__init__(*args, **kwargs)
        self.interactome = Interactome("test_files/test_05.txt")

    def test_clean_interactome(self):
        "Tests if file is correctly cleaned"
        self.assertEquals(self.interactome.clean_interactome(
        ), ([['A', 'B'], ['A', 'C'], ['B', 'C'], ['C', 'D']], 4))


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
