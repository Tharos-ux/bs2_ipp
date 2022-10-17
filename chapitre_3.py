import numpy as np
from itertools import chain, permutations, combinations
from typing import Callable, Tuple
from statistics import mean
from collections import Counter
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import networkx as nx


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

        key, value = list(self.int_dict.keys()), list(self.int_dict.values())
        self.proteins = sorted(set(key + list(chain(*list(value)))))

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
        with open(self.file_in, "r") as f:
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
        node_list = sorted(set(key + list(chain(*value))))
        dim = len(node_list)
        matrix = np.zeros([dim, dim], dtype=int)
        for key2, value2 in self.int_dict.items():
            col = node_list.index(key2)
            for item in value2:
                line = node_list.index(item)
                matrix[line][col] = 1
                matrix[col][line] = 1
        return np.asarray(matrix), node_list

    def count_vertices(self) -> int:
        """ Count the number of unique vertices from a dictionary,
        including the ones that are only present in the values of the dictionary.

        Returns
        -------
        int
            Number of unique vertices in the graph
        """
        key = list(self.int_dict.keys())
        value = list(self.int_dict.values())
        return len(sorted(set(key + list(chain(*value)))))

    def count_edges(self) -> int:
        """ Count the number of edges from a dictionary.

        Returns
        -------
        int
            Number of unique edges in the graph
        """
        value = list(self.int_dict.values())
        return len(list(chain(*value)))

    def get_degree(self, prot: str) -> int:
        """Count the number of interactions for a specific protein.

        Parameters
        ----------
        prot : str
            The name or ID of the protein.

        Returns
        -------
        int
            The number of edges linked to a specific protein if the protein exists, else 0.
        """
        return len(self.int_dict[prot]) if prot in self.int_dict else 0

    def get_max_degree(self) -> Tuple[str, int]:
        """Gets the protein with the highest number of interactions and the number of interactions associated.

        Returns
        -------
        Tuple[str, int]
            The name of the protein and the number of interactions associated.
        """
        max_interactions = 0
        for key, value in self.int_dict.items():
            len_val = len(value)
            if len_val > max_interactions:
                max_interactions = len_val
                return key, len_val

    def get_ave_degree(self) -> int:
        """Gives the approximate average degree

        Returns
        -------
        int
            The average degree of PPI interactions, rounded
        """
        return int(mean(list({key: len(value)
                              for key, value in self.int_dict.items()}.values())))

    def count_degree(self, deg: int) -> int:
        """Counts the number of proteins with a given degree deg

        Parameters
        ----------
        deg : int
            The given degree

        Returns
        -------
        int
            The number of proteins in the graph with the given degree
        """
        return len([k for k, v in {key: len(value) for key, value in self.int_dict.items()}.items() if v == deg])

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
        """Calculates the graph's density

        Returns:
            float: graph's density
        """
        return (2*len(self.int_list))/(len(self.proteins)*(len(self.proteins)-1))

    def clustering(self, prot: str) -> float:
        """Calculates the clustering coefficient of a node, defined as "prot"

        Parameters
        ----------
        prot : str
            The node of which we want to calculate the clustering coeficient

        Returns
        -------
        float : The clustering coeficient
        """
        if self.get_degree(prot) <= 1:
            return 0
        number_neigbors_interactions: int = len(
            [0 for x in self.int_list if x in list(
                permutations(self.__neighbors(prot), r=2))]
        )
        return number_neigbors_interactions/self.__clique(prot)

    def erdos_renyi_graph(n: int, q: float) -> list[Tuple[str, str]]:
        """Creates a random graph with n nodes and generate edges randomly between each set of nodes, with respect to the probability q.

        Parameters
        ----------
        n : int
            The number of nodes
        q : float
            The probability for the edges' creation
         Returns:
            list: list containing all the edges calculated randomly according to the probability q
        """
        nodes = [str(i) for i in range(1, n+1)]
        list_all_edges = list((combinations(nodes, 2)))
        proba_array = [np.random.choice(np.arange(0, 2), p=[1-q, q])
                       for _ in range(len(list_all_edges))]

        graph = [edge for i, edge in enumerate(
            list_all_edges) if proba_array[i]]
        return graph

    '''
    RAPPEL BARABASI ALBERT
    New nodes are more likely to create links with nodes that are the highly connected (rather than poorly connected)
    Barabasi Albert model = model of growth and preferential attachment
    Steps:
    - Starts with a small graph
    - Add a new node to the graph
    - Compute new edges between the new node and each node in the graph.
    The probability for the creation of each new edge is proportional to the number of connection the graph node has (its degree).

    => "The rich get richer", the highly connected nodes are priviledge to acquire more connections. It simulates a scale free network.
    However there is a strong biai in the simulation, the first nodes to be added will always end up being the most connected.
    Probability = (deg(i)+1)/Sum(deg(i)+1)
    '''

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
        graph = self.int_dict
        key_vertice = list(self.int_dict.keys())
        value_vertice = list(self.int_dict.values())
        count_vertices = len(
            sorted(set(key_vertice + list(chain(*value_vertice)))))
        for node in range(m):
            graph.setdefault(node, []).append(node)
        for key in graph.keys():
            probability = (self.get_degree(key)+1) / \
                (2*self.count_edges() + count_vertices)
            result = np.random.choice(
                np.arange(0, 2), p=[1-probability, probability])
            if result:
                graph.setdefault(node, []).append(key)

    def plot_random_graph(self, n: int) -> None:
        """Plot a random graph generated by the erdos renji algorithm

        Parameters
        ----------
        n : int
            The number of nodes in the graph
        """
        G = nx.Graph()
        G.add_nodes_from([str(i) for i in range(1, n+1)])
        G.add_edges_from(self.erdos_renyi_graph(n, 0.4))
        plt.figure(figsize=(8, 6))

        nx.draw_networkx(G, with_labels=True)
        plt.tick_params(axis='x', which='both', bottom=False,
                        top=False, labelbottom=False)
        plt.tick_params(axis='y', which='both', right=False,
                        left=False, labelleft=False)
        for pos in ['right', 'top', 'bottom', 'left']:
            plt.gca().spines[pos].set_visible(False)

        plt.show()

    def __str__(self):
        graph = nx.Graph()
        for prot_a, prot_b in self.int_list:
            graph.add_edge(prot_a, prot_b)

        options = {
            "font_size": 6,
            "node_size": 300,
            "node_color": "white",
            "edgecolors": "black",
            "linewidths": 1,
            "width": 1,
        }
        nx.draw_networkx(graph, None, **options)

        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        plt.show()
        return f"Displaying Interactome object with {len(self.proteins)} nodes and {len(self.int_list)} interactions."
