from random import choice, choices
from string import ascii_uppercase
import numpy as np
from itertools import chain, permutations, combinations
from typing import Callable, Tuple
from statistics import mean
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx


def is_interaction_file(filename: str) -> bool:
    ############
    #ATTENTION, NE CAPTURE PAS L'ERREUR SI LE NOMBRE D'INTERACTION EN DEBUT DE FICHIER EST MAUVAIS.
    # CHERCHE A INIT self.__proteins qui n'existe pas :
    # AttributeError: 'Interactome' object has no attribute '_Interactome__proteins'. Did you mean: '_Interactome__neighbors'?
    ############
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
        with open(filename, 'r') as handler:
            first_line: int = int(handler.readline().replace('\n', ''))
            for i, line in enumerate(handler):
                if len(line.replace('\n', '').split()) != 2:
                    raise ValueError
            if i+1 != first_line:
                raise AssertionError
        status = True
    except AssertionError:
        raise AssertionError(
            f"File {filename} has incorrect number of lines. Described : {i}, awaited {first_line}")
    except TypeError:
        raise TypeError(f"File {filename} has incorrect first line.")
    except ValueError:
        raise ValueError(f"File contains error on line {i}.")
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} does not exists.")
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
            object: the object returned by the Callable
        """
        if is_interaction_file(args[1]):
            return f(*args, **kwargs)
    return wrapper


class Interactome:

    @check_interaction_file
    def __init__(self, file: str, fileout="clean_int_graph.txt"):
        """Creates a list and a dictionary from the interactome file as well as the list of ordered proteins.

        Parameters
        ----------
        file : str
            a path to an interactome file in txt format
        fileout : str, optional
            output path for a cleaned interactome txt file
        """
        self.file_in = file
        self.file_out = fileout
        self.write_clean_interactome()
        self.int_list, self.int_dict = self.read_interaction_file()
        self.int_mat, self.proteins = self.read_interaction_file_mat()
        self.flat_list = list(chain(*self.int_list))

        #key, value = list(self.int_dict.keys()), list(self.int_dict.values())
        #sorted(set(key + list(chain(*list(value)))))

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
        # "node_color": "white",
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
                # TODO fix cette fonction
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
        dico_interactions = dict()
        with open(self.file_out, "r") as f:
            next(f)
            for line in f:
                list_interactions.append(tuple(line.split()))
                key, value = line.split()
                dico_interactions.setdefault(key, []).append(value)
        return list_interactions, dico_interactions

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
        liste_sommets = sorted(set(key + list(chain(*value))))
        dim = len(liste_sommets)
        matrix = np.zeros([dim, dim], dtype=int)
        for key2, value2 in self.int_dict.items():
            col = liste_sommets.index(key2)
            for item in value2:
                ligne = liste_sommets.index(item)
                matrix[ligne][col] = 1
                matrix[col][ligne] = 1
        return np.asarray(matrix), liste_sommets

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
        
        # return len(self.int_dict[prot]) if prot in self.int_dict else 0

    def get_max_degree(self) -> Tuple[int, list]:
        """Gets the protein with the highest number of interactions and the number of interactions associated.

        Returns
        -------
        Tuple[int, list]
            The number of interaction max and the names of the proteins associated.
        """
        list_degrees = [self.get_degree(prot) for prot in self.proteins]
        max_degree = max(list_degrees)
        prot_max_degree = [self.proteins[i] for i, degree in enumerate(list_degrees) if degree == max_degree]
        return max_degree, prot_max_degree

        #max_interactions = 0
        #for key, value in self.int_dict.items():
        #    len_val = len(value)
        #    if len_val > max_interactions:
        #        max_interactions = len_val
        #        return key, len_val


    def get_ave_degree(self) -> float:
        """Gives the approximate average degree

        Returns
        -------
        float
            The average degree of PPI interactions
        """
        return mean([self.get_degree(prot) for prot in self.proteins])
        #return int(mean(list({key: len(value)
        #                      for key, value in self.int_dict.items()}.values())))

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
        # return len([k for k, v in {key: len(value) for key, value in self.int_dict.items()}.items() if v == deg])

    def __output_histogram(self, data: Counter) -> None:
        """Plots histogram from counter

        Parameters
        ----------
        data : Counter
            Number of number of edges to a node
        """
        plt.bar(data.keys(), data.values())
        plt.savefig(f"{self.file.split('.')[0]}.png")

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
        # get neighbors of prot
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
        #########
        #FONCTIONNE MAIS A OPTIMISER (très long avec de gros graphes)
        #########
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
        """
        nodes = [str(i) for i in range(1, n+1)]
        list_all_edges = list((combinations(nodes, 2)))
        proba_array = [choices([0, 1], weights=[1-q, q])[0]
                       for _ in range(len(list_all_edges))]

        graph = [edge for i, edge in enumerate(
            list_all_edges) if proba_array[i]]
        return graph

    def barabasi_albert_graph(self, m: int) -> list[Tuple[str, str]]:
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
            for key in self.int_dict.keys():
                probability = (self.get_degree(key)+1) / \
                    (2*self.count_edges() + self.count_vertices())
                if choices([0, 1], weights=[1-probability, probability])[0]:
                    self.int_list.append((node, key))
                    self.int_dict[key].append(node)
        self.int_mat, self.proteins = self.read_interaction_file_mat()
