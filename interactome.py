from random import choice, choices
from string import ascii_uppercase
import numpy as np
from itertools import chain, permutations, combinations
from typing import Callable, Tuple
from statistics import mean
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
from os import path, system


def is_interaction_file(filename: str) -> bool:
    """Checks if file is correct

    Raises:
        ValueError: happens if any line is badly formatted
        AssertionError: happens if number of lines is not correct
        TypeError: happens if first line is not a int
        FileNotFoundError: happens if file does not exists

    Returns:
        bool: status of file
    """
    status: bool = False
    try:
        if not path.exists(filename):
            raise FileNotFoundError
        with open(filename, 'r') as handler:
            first_line: int = int(handler.readline().replace('\n', ''))
            for i, line in enumerate(handler):
                if len(line.replace('\n', '').split()) != 2:
                    raise ValueError
            if i+1 != first_line:
                raise AssertionError
        status = True
    except AssertionError:
        print(AssertionError(
            f"File {filename} has incorrect number of lines. Described : {i}, awaited {first_line}"))
    except TypeError:
        print(TypeError(f"File {filename} has incorrect first line."))
    except ValueError:
        print(ValueError(f"File contains error on line {i}."))
    except FileNotFoundError:
        print(FileNotFoundError(f"File {filename} does not exists."))
    finally:
        return status


def check_interaction_file(f: Callable) -> Callable:
    """Decorator to check if file is correctly formatted

    Args:
        f (Callable): function to call

    Returns:
        Callable: call to function to call
    """
    def wrapper(*args: list, **kwargs: dict) -> object:
        """Inner part of decorator, responsible for checks

        Returns:
            Object: the object returned by the Callable
        """
        if 'method' in kwargs:
            if kwargs['method'] != 'default':
                return f(*args, **kwargs)
        if is_interaction_file(args[1]):
            return f(*args, **kwargs)
        exit()

    return wrapper


class Interactome:

    @property
    def file_in(self):
        """ Getter of the attibute file_in. """
        return self.__file_in

    @file_in.setter
    def file_in(self, new_file_in: str):
        """ Setter of the attribute file_in. """
        if not isinstance(new_file_in, str):
            raise ValueError("Expecting a string")
        self.__file_in = new_file_in

    @property
    def file_out(self):
        """ Getter of the attibute file_out. """
        return self.__file_out

    @file_out.setter
    def file_out(self, new_file_out: str):
        """ Setter of the attribute file_out. """
        if not isinstance(new_file_out, str):
            raise ValueError("Expecting a string")
        self.__file_out = new_file_out

    @property
    def int_list(self):
        """ Getter of the attribute int_list. """
        return self.__int_list

    @int_list.setter
    def int_list(self, new_int_list):
        """ Setter of the attribute int_list. """
        if not isinstance(new_int_list, list):
            raise ValueError("Expecting a list")
        self.__int_list = new_int_list

    @property
    def int_mat(self):
        """ Getter of the attribute int_mat. """
        return self.__int_mat

    @int_mat.setter
    def int_mat(self, new_int_mat):
        """ Setter of the attribute int_mat. """
        if not isinstance(new_int_mat, np.ndarray):
            raise ValueError("Expecting an array")
        self.__int_mat = new_int_mat

    @property
    def int_dict(self):
        """ Getter of the attribute int_dict. """
        return self.__int_dict

    @int_dict.setter
    def int_dict(self, new_int_dict):
        """ Setter of the attribute int_dict. """
        if not isinstance(new_int_dict, dict):
            raise ValueError("Expecting a dict")
        self.__int_dict = new_int_dict

    @property
    def proteins(self):
        """ Getter of the attribute proteins. """
        return self.__proteins

    @proteins.setter
    def proteins(self, new_proteins):
        """ Setter of the attribute proteins. """
        if not isinstance(new_proteins, list):
            raise ValueError("Expecting a list")
        self.__proteins = new_proteins

    @check_interaction_file
    def __init__(self, file: str, fileout="clean_int_graph.txt", method='default', kwargs={}):
        """Creates a list and a dictionary from the interactome file as well as the list of ordered proteins.

        Parameters
        ----------
            file (str): A path to an interactome file in txt format
            fileout (str, optional) : Output path for a cleaned interactome txt file
            method (str, optional): Alternative methods to generate graphs. Defaults to 'default'.
            kwargs (dict, optional): Additionnal arguments for alternative methods. Defaults to {}.
        """
        match method:
            case 'default':
                # path to input.txt file
                self.file_in = file
                # path to output.txt file
                self.file_out = fileout
                # interactome file cleaning
                self.write_clean_interactome()
                # interactions as list and dict
                self.int_list, self.int_dict = self.read_interaction_file()
                # matrix of distance and list of proteins in interactome
                self.int_mat, self.proteins = self.read_interaction_file_mat()
                # list of all proteins, resp. to their interactions
                self.flat_list = list(chain(*self.int_list))
            case 'erdos-renyi':
                self.proteins = []
                self.__save_graph(self.erdos_renyi_graph(**kwargs))
                self.__init__(".temp_graph.txt", method='default')
                system("rm .temp_graph.txt")
            case 'barabasi-albert':
                self.int_list, self.int_dict = [], {}
                self.int_mat, self.proteins = np.ndarray([]), []
                self.flat_list = []
                self.__save_graph(self.__barabasi_albert(**kwargs))
                self.__init__(".temp_graph.txt", method='default')
                system("rm .temp_graph.txt")

    def __str__(self):
        return f"Interactome object with {len(self.proteins)} nodes and {len(self.int_list)} interactions."

    def __no_color(self, graph: nx.Graph):
        return [0 for _ in list(graph.nodes())]

    def color_by_neighbors(self, graph: nx.Graph):
        return [len(graph.adj[node]) for node in list(graph.nodes())]

    def color_by_connectivity(self, graph: nx.Graph):
        components: list = [
            list(x) for x in nx.algorithms.components.connected_components(graph)]
        flattened: list = [item for sublist in components for item in sublist]
        codes: list = [i for i, sublist in enumerate(
            components) for _ in sublist]
        return [codes[flattened.index(node)] for node in list(graph.nodes())]

    def draw(self, method: Callable = __no_color, colormap=plt.cm.Purples):
        plt.cla()
        graph = nx.Graph()
        for prot_a, prot_b in self.int_list:
            graph.add_edge(prot_a, prot_b)

        colors = method(self, graph)

        options = {
            "font_size": 6,
            "node_size": 300,
            "cmap": colormap,
            "node_color": colors,
            "edgecolors": "black",
            "linewidths": 1,
            "width": 1,
        }

        nx.draw_networkx(graph, None, **options)

        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        plt.show()

    def clean_interactome(self) -> Tuple[list[Tuple[str, str]], int]:
        """Cleans data from file by removing redundant interactions.
         Count the number of interactions

        Parameters
        ----------
        filein : str
            The interactome file to clean.

        Returns
        -------
        list, int
            List of non redundant interactions, number of interactions.
        """
        list_interactions = list()
        with open(self.file_in, "r") as f:
            next(f)
            for line in f:
                line_interaction = line.split()
                if line_interaction[::-1] not in list_interactions and line_interaction[0] != line_interaction[1] and line_interaction not in list_interactions:
                    list_interactions.append(line_interaction)
        return list_interactions, len(list_interactions)

    def write_clean_interactome(self) -> None:
        """ Writes the cleaned data to the output file.
        Parameters
        ----------
        filein : str
            The interactome file to clean.
        fileout : str
            The cleaned interactome file
        """
        list_interactions, nb_interactions = self.clean_interactome()
        with open(self.file_out, 'w') as handler:
            handler.write('\n'.join(
                [str(nb_interactions)]+[f"{key} {value}" for (key, value) in list_interactions]))

    def read_interaction_file(self) -> Tuple[list[Tuple[str, str]], dict[str, list[str]]]:
        """ Reads an interaction file and format the interactions in the form of a dictionary and a list.

        Parameters
        ----------
        file : str
            Path to the interaction file

        Returns
        -------
        list, dict
            The list of interactions and the dictionary of interactions
        """
        list_interactions = list()
        dict_interactions = dict()
        with open(self.file_out, "r") as f:
            next(f)
            for line in f:
                list_interactions.append(tuple(line.split()))
                key, value = line.split()
                dict_interactions.setdefault(key, []).append(value)
        return list_interactions, dict_interactions

    def read_interaction_file_mat(self) -> Tuple[np.ndarray, list[str]]:
        """Reads a dictionary of interactions and format the interactions in the form of a matrix.
        The matrix size is equal to the number of dual interactions in the file.

        Returns
        -------
        np.ndarray, list[str]
            The matrix of interactions and the list of the graph's vertices.
            The order of the vertices in the list is representative of the order in the matrix.
        """
        key = list(self.int_dict.keys())
        value = list(self.int_dict.values())
        nodes_list = sorted(set(key + list(chain(*value))))
        dim = len(nodes_list)
        matrix = np.zeros([dim, dim], dtype=int)
        for key2, value2 in self.int_dict.items():
            col = nodes_list.index(key2)
            for item in value2:
                line = nodes_list.index(item)
                matrix[line][col] = 1
                matrix[col][line] = 1
        return np.asarray(matrix), nodes_list

    def count_vertices(self) -> int:
        """ Count the number of unique vertices from a dictionary,
        including the ones that are only present in the values of the dictionary.

        Returns
        -------
        int
            Number of unique vertices in the graph
        """
        return len(self.proteins)

    def count_edges(self) -> int:
        """ Count the number of edges from a dictionary.

        Returns
        -------
        int
            Number of unique edges in the graph
        """
        return len(self.int_list)

    def get_degree(self, prot: str) -> int:
        """Count the number of interactions for a specific protein.

        Parameters
        ----------
        prot : str
            The name or ID of the protein.

        Returns
        -------
        int
            The number of edges linked to a specific protein if the protein exists, else raise a ValueError.
        """
        if prot in self.proteins:
            degree = self.flat_list.count(prot)
        else:
            raise ValueError("Protein does not exist")
        return degree

    def get_max_degree(self) -> Tuple[int, list]:
        """Gets the protein with the highest number of interactions and the number of interactions associated.

        Returns
        -------
        Tuple[int, list]
            The number of interaction max and the names of the proteins associated.
        """
        list_degrees = [self.get_degree(prot) for prot in self.proteins]
        max_degree = max(list_degrees)
        prot_max_degree = [self.proteins[i] for i, degree in enumerate(
            list_degrees) if degree == max_degree]
        return max_degree, prot_max_degree

    def get_ave_degree(self) -> float:
        """Gives the approximate average degree

        Returns
        -------
        float
            The average degree of PPI interactions
        """
        return mean([self.get_degree(prot) for prot in self.proteins])

    def count_degree(self, deg: int) -> int:
        """Counts the number of proteins with a given degree deg

        Parameters
        ----------
        deg : int
            The given degree

        Returns
        -------
        int
            The number of proteins in the graph with the given degree deg
        """
        list_degrees = [self.get_degree(prot) for prot in self.proteins]
        return len([self.proteins[i] for i, degree in enumerate(list_degrees) if degree == deg])

    def __output_histogram(self, data: Counter) -> None:
        """Plots histogram from counter

        Parameters
        ----------
        data : Counter
            Number of number of edges to a node
        """
        plt.bar(data.keys(), data.values())
        plt.xticks(np.arange(min(data.values()), max(data.values())+1, 1))
        plt.show()
        plt.savefig("degree_histogram.png")

    def histogram_degree(self, dmin: int, dmax: int) -> None:
        """Filters some proteins by degree within range

        Parameters
        ----------
        dmin : int
            lower boundary
        dmax : int
            upper boundary

        """
        self.__output_histogram(Counter(deg for deg in [len(
            value) for value in self.int_dict.values()] if deg >= dmin and deg <= dmax))

    def __neighbors(self, prot: str) -> list:
        return [a if b == prot else b for (a, b) in self.int_list if a == prot or b == prot]

    def __clique(self, prot: str) -> int:
        """Get neighbors of prot

        Args:
            prot (str): protein to check

        Returns:
            int: clique
        """
        number_neighbors: int = len(self.__neighbors(prot))
        return ((number_neighbors - 1) * number_neighbors)/2

    def density(self) -> float:
        """Computes the density of the graph

        Returns
        -------
        float
            The density calculated
        """
        return (2*self.count_edges())/(self.count_vertices()*(self.count_vertices()-1))

    def clustering(self, prot: str) -> float:
        """Computes the clustering coefficient of a node in a graph

        Parameters
        ----------
        prot : str
            The protein of which we want to know the clustering coefficient

        Returns
        -------
        float
            The clustering coefficient of the protein prot, 0 if it has no neighbors
        """
        if self.get_degree(prot) <= 1:
            return 0
        number_neighbors_interactions: int = len(
            [0 for x in self.int_list if x in list(
                permutations(self.__neighbors(prot), r=2))]
        )
        return number_neighbors_interactions/self.__clique(prot)

    def __generate_protein(self, length: int = 5) -> str:
        while True:
            prot_name: str = ''.join(choice(ascii_uppercase)
                                     for i in range(length))
            if prot_name not in self.proteins:
                break
        self.proteins = self.proteins + [prot_name]
        return prot_name

    def __save_graph(self, graph: list) -> None:
        """Saves a graph from a list

        Args:
            graph (list): _description_
        """
        with open(".temp_graph.txt", 'w') as handler:
            handler.write('\n'.join(
                [str(len(graph))]+[f"{key} {value}" for (key, value) in graph]))

    def erdos_renyi_graph(self, n: int, q: float, oriented=False):
        """Creates a random graph with n nodes and generate edges randomly between each set of nodes, with respect to the probability q.

        Parameters
        ----------
        n : int
            The number of nodes
        q : float
            The probability for the edges' creation
        oriented : bool, optional
            True if the graph is oriented, else False (default)
        Returns
        -------
        List
            the erdos renyi graph
        """
        nodes = [self.__generate_protein() for i in range(1, n+1)]
        list_all_edges = list((combinations(nodes, 2)))
        proba_array = [choices([0, 1], weights=[1-q, q])[0]
                       for _ in range(len(list_all_edges))]

        graph = [edge for i, edge in enumerate(
            list_all_edges) if proba_array[i]]
        return graph

    def __barabasi_albert(self, m: int) -> None:
        """Creates a random graph according to the Barabasi Albert model, starting from a empty graph.

        Parameters
        ----------
        graph : dict
            The original graph
        m : int
            The number of nodes to add, following the Barabasi-Albert algorithm

        Returns
        -------
        list[Tuple[str, str]]
            The new graph containing all the new nodes, linked to the original nodes according to the Barabasi algorithm
        """
        nodes = [self.__generate_protein() for _ in range(m)]
        self.int_dict[nodes[0]] = [nodes[1]]
        self.int_list = [(nodes[0], nodes[1])]

        for node in nodes[2:]:
            self.int_dict[node] = []
            connected_node: bool = False
            while not connected_node:
                for key in self.int_dict.keys():
                    if key != node and key in list(chain(*self.int_list)):
                        #probability = self.get_degree(key) / (2*self.count_edges())
                        probability = (self.get_degree(key)+1) / \
                            (2*self.count_edges() + self.count_vertices())
                        if choices([0, 1], weights=[1-probability, probability])[0] or self.int_list == []:
                            self.int_list.append((node, key))
                            self.int_dict[key].append(node)
                            connected_node = True
        return self.int_list

    def barabasi_albert_graph(self, m: int) -> None:
        """Creates a random graph according to the Barabasi Albert model, starting from a random graph generated by the Erdos Renyi algorithm.

        Parameters
        ----------
        graph : dict
            The original graph
        m : int
            The number of nodes to add, following the Barabasi-Albert algorithm

        Returns
        -------
        list[Tuple[str, str]]
            The new graph containing all the new nodes, linked to the original nodes according to the Barabasi algorithm
        """
        for node in [self.__generate_protein() for _ in range(m)]:
            self.int_dict[node] = []
            connected_node: bool = False
            while not connected_node:
                for key in self.int_dict.keys():
                    if key != node and key in list(chain(*self.int_list)):
                        probability = (self.get_degree(key)) / \
                            (2*self.count_edges())
                        if choices([0, 1], weights=[1-probability, probability])[0]:
                            self.int_list.append((node, key))
                            self.int_dict[key].append(node)
                            connected_node = True
        self.int_mat, self.proteins = self.read_interaction_file_mat()

    def extract_all_CC(self) -> dict:
        """ Extracts all the paths from a graph

        Returns
        -------
        dict
            A dictionnary where the key is the path's number, and the value is the list of nodes belonging to the path.
        """
        nodes_left = self.proteins
        CC_dict = dict()
        i = 1
        while nodes_left:
            prot = nodes_left[0]
            CC_dict[i] = self.extract_CC(prot)
            nodes_left = list(
                filter(lambda x: x not in CC_dict[i], nodes_left))
            i += 1
        return CC_dict

    def extract_CC(self, prot: str, path=list(), i=0) -> list:
        """Identifies all the nodes contained in the same path as the protein given in argument

        Parameters
        ----------
        prot : str
            The protein
        path :
            A list that will contain the path including the protein
        i : 
            An integer initialised at 0        
        Returns
        -------
        list
            A list that contains the path including the protein
        """
        path = path+[prot]
        # i is there in case the starting node only has one edge
        if self.get_degree(prot) > 1 or i == 0:
            i = 1
            for node in self.get_neighbors(prot):
                if node not in path:
                    path = self.extract_CC(node, path)
        return path

    def get_neighbors(self, prot: str) -> list:
        """ Extracts the list of neighbors of a given protein from an interaction matrix

        Parameters
        ----------
        prot : str
            The given protein

        Returns
        -------
        list
            The list of the protein's neighbors
        """
        list_nodes_CC = []
        prot_index_in_matrix = self.int_mat[self.proteins.index(prot)]
        for i in range(len(self.proteins)):
            if prot_index_in_matrix[i] == 1:
                list_nodes_CC.append(self.proteins[i])
        return list_nodes_CC

    def count_CC(self) -> Tuple[int, list[int, int]]:
        """Calculates the size of each path and the total number of paths in a graph

        Parameters
        ----------

        Returns
        -------
        int 
            The total number of paths
        list[int,int] :
            A list containing a tuple for each path. Each tuple contains the label and the size of a path
        """
        dico = self.extract_all_CC()
        count_CC = max(dico.keys())
        list_size_CC = [(key, len(value)) for key, value in dico.items()]
        return count_CC, list_size_CC

    def write_CC(self, CC_file_out="CC_file_out.txt") -> None:
        """ Writes in an output file the size and the nodes contained in each path of the graph. 
        Each line in the file shows first the size of the path and then list the nodes included in the path.

        Parameters
        ----------
        CC_file_out : str, optional
            The name of the file created, by default "CC_file_out"
        """
        dico = self.extract_all_CC()
        with open(CC_file_out, 'w') as handler:
            handler.write(
                '\n'.join([f"{str(len(value))} {value}" for value in dico.values()]))

    def compute_CC(self) -> list[int, str]:
        """ Creates a list containing the path label associated to each proteins

        Returns
        -------
        list[int, str]
            A list containing tuples. Each tuple contains the path's label and the name of the protein belonging to this path
        """
        dico = self.extract_all_CC()
        return list(chain(*[[(key, i) for i in value] for key, value in dico.items()]))
