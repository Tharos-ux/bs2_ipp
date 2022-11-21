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
        self.interactome2 = Interactome("test_files/toy_example2.txt")
        self.interactome_Human = Interactome("test_files/Human_HighQuality.txt")

    def test_object_instance(self):
        "Tests if object instance is created"
        self.assertTrue(isinstance(self.interactome, Interactome))

    def test_object_file_in_type(self):
        "Tests if interactime.file_in is a str"
        self.assertTrue(isinstance(self.interactome.file_in, str))

    def test_object_file_in_property(self):
        "Tests if interactome.file_in is well initialized"
        self.assertEquals(self.interactome.file_in,
                          "test_files/toy_example.txt")

    def test_object_file_out_type(self):
        "Tests if interactome.file_out is a str"
        self.assertTrue(isinstance(self.interactome.file_out, str))

    def test_object_file_out_property(self):
        "Tests if interactome.file_out is well initialized"
        self.assertEquals(self.interactome.file_out, "clean_int_graph.txt")

    def test_object_int_list_type(self):
        "Tests if interactome.int_list is a list"
        self.assertTrue(isinstance(self.interactome.int_list, list))

    def test_object_int_list_property(self):
        #######################
        # ATTENTION TEST FAUX, (D E) ET (E D) SONT LA MEME CHOSE ET DEVRAIENT SAUTER
        # => MODIF FAITE
        #######################
        "Tests if interactome.int_list is well initialized"
        self.assertEquals(self.interactome.int_list, [('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('D', 'E'), ('D', 'F'), ('G', 'A'), ('G', 'C'), ('G', 'B')])

    def test_object_int_dict_type(self):
        "Tests if interactome.int_dict is a dict"
        self.assertTrue(isinstance(self.interactome.int_dict, dict))

    def test_object_int_dict_property(self):
        #######################
        # ATTENTION TEST FAUX, (D E) ET (E D) SONT LA MEME CHOSE ET DEVRAIENT SAUTER
        # => MODIF FAITE
        #######################
        "Tests if interactome.int_dict is well initialized"
        self.assertEquals(self.interactome.int_dict, {'A': ['B', 'C'], 'B': ['C', 'D'], 'D': ['E', 'F'], 'G': ['A', 'C', 'B']})

    def test_object_proteins_type(self):
        "Tests if interactome.proteins is a list"
        self.assertTrue(isinstance(self.interactome.proteins, list))

    def test_object_file_property(self):
        "Tests if interactome.proteins is well initialized"
        self.assertEquals(self.interactome.proteins, ['A', 'B', 'C', 'D', 'E', 'F', 'G'])

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
        self.interactome2 = Interactome("test_files/toy_example2.txt")
        self.interactome_Human = Interactome("test_files/Human_HighQuality.txt")

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
        
    # NEW ADDITIONS STARTING HERE => A TESTER
        
    def test_file_separator(self):
        "Tests a file with a semicolon as separator"
        self.assertTrue(is_interaction_file("test_files/test_06.txt"))
        self.assertEquals(self.interactome.int_list, [('A', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'D')])

    def test_file_with_random_spaces(self):
        "Tests a file with random spaces in file"
        self.assertTrue(is_interaction_file("test_files/test_07.txt"))
        self.assertEquals(self.interactome.int_list, [('A', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'D')])
        
    def test_file_triple_interaction(self):
        "Tests a file with an interaction with 3 nodes instead of 2"
        self.assertFalse(is_interaction_file("test_files/test_08.txt"))
        
    # TEST METHOD count_vertices
    
    def test_count_vertices(self):
        "Tests if the number of vertices of a graph is well counted"
        self.assertEquals(self.interactome.count_vertices(), 7)
    
    # TEST METHOD count_edges
    def test_count_edges(self):
        "Tests if the number of edges of a graph is well counted"
        self.assertEquals(self.interactome.count_edges(), 9)
    
    # TEST METHOD clean_interactome
    # Flemme
    
    # TEST METHOD get_degree
    def test_get_degree_mult(self):
        "Tests if the number of degrees of a protein is well counted"
        self.assertEquals(self.interactome.get_degree("A"), 3)

    def test_get_degree_single(self):
        "Tests if the number of degrees of a protein is well counted"
        self.assertEquals(self.interactome.get_degree("E"), 1)
    
    def test_get_degree_human(self):
        "Tests if the number of degrees of a protein is well counted"
        self.assertEquals(self.interactome_Human.get_degree("1433B_HUMAN"), 49)

    def test_get_degree_error(self):
        "Tests if the number of degrees of a protein which is non-exitent"
        self.assertRaises(ValueError,self.interactome.get_degree("Y"))
    
    # TEST METHOD get_max_degree
    def get_max_degree(self):
        #######################
        # NE FONCTIONNE PAS, NE TIENS PAS COMPTE QUE LE GRAPHE EST NON ORIENTE, il faut parcourir la liste et compter le nombre d'occurence de chaque prot
        # => MODIF FAITE
        #######################
        "Tests if the degree max of a graph is well calculated"
        self.assertEquals(self.interactome.get_max_degree(), (4, ['B']))
    
    # TEST METHOD get_ave_degree
    def get_ave_degree(self):
        #######################
        # NE FONCTIONNE PAS, NE TIENS PAS COMPTE QUE LE GRAPHE EST NON ORIENTE, il faut parcourir la liste et compter le nombre d'occurence de chaque prot
        # => MODIF FAITE, float
        # => pas sure de la fonction equivalente en networkx ou si on repond bien à la consigne
        #######################
        "Tests if the average degree of a graph is well calculated"
        self.assertEquals(round(self.interactome.get_ave_degree(),2), 2.57)
    
    # TEST METHOD count_degree
    def count_degree(self):
        #######################
        # NE FONCTIONNE PAS, NE TIENS PAS COMPTE QUE LE GRAPHE EST NON ORIENTE, il faut parcourir la liste et compter le nombre d'occurence de chaque prot
        # => MODIF FAITE
        #######################
        "Tests if the number of proteins with a given degree is well calculated"
        self.assertEquals(self.interactome.count_degree(3), 4)
        self.assertEquals(self.interactome.count_degree(0), 0)
        self.assertEquals(self.interactome.count_degree(4), 1)
        self.assertEquals(self.interactome.count_degree(1), 2)
    
    # TEST METHOD histogram_degree
    # Flemme

    # TEST METHOD density
    def density(self):
        "Tests if the density of a graph is well calculated"
        self.assertEquals(round(self.interactome.density(),2), 0.43)
        self.assertEquals(round(self.interactome2.density(),2), 0.48)
        self.assertEquals(round(self.interactome_Human.density(),8), 0.00059248)
    
    # TEST METHOD clustering
    def clustering(self):
        "Tests if the clustering coefficient of a protein is well calculated"
        self.assertEquals(round(self.interactome.clustering("A"),4), 1.0)
        self.assertEquals(round(self.interactome.clustering("C"),4), 1.0)
        self.assertEquals(round(self.interactome.clustering("D"),4), 0.0)
        self.assertEquals(round(self.interactome2.clustering("D"),4), 0.3333)
        self.assertEquals(round(self.interactome_Human.clustering("1433B_HUMAN"),4), 0.0527)
    
    # TEST METHOD erdos_renyi_graph
    # count number of nodes and edges
    '''Afin de vérifier votre méthode, construisez un graphe aléatoire de paramètre p = 0.3
    et calculez ensuite la distribution des degrés des sommets. Pour ce faire, vous devriez
    vous servir de méthodes implémentées au chapitre 2
    '''    
    
    # TEST METHOD barabasi_albert_graph
    
    
        

if __name__ == "__main__":
    system("python -m unittest -v unit_tests.py")
