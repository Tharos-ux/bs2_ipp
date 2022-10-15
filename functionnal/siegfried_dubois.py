
from typing import Callable, Tuple
import numpy as np
from itertools import chain
from statistics import mean
from collections import Counter
import matplotlib as plt


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
    def wrapper(*args: list) -> object:
        """Inner part of decorator, responsible for checks

        Returns:
            object: the object returned by the Callable
        """
        if is_interaction_file(args[0]):
            return f(*args)
    return wrapper


def read_interaction_file_dict(filename: str) -> dict[str, list[str]]:
    """Reads from an interaction file a set of interactions

    Args:
        filename (str): path to file

    Returns:
        dict[str, list[str]]: interactions for each node of graph
    """
    interactions: dict[str, list[str]] = {}
    with open(filename, 'r') as handler:
        next(handler)
        for line in handler:
            key, value = line.replace('\n', '').split(' ')
            if value in interactions and key in interactions[value]:
                pass
            else:
                interactions[key] = [
                    value] if key not in interactions else interactions[key]+[value]
    return interactions


def read_interaction_file_list(filename: str) -> list[Tuple[str, str]]:
    """Reads from an interaction file a set of interactions

    Args:
        filename (str): path to file

    Returns:
        list[str]: interactions for each node of graph
    """
    interactions: list[Tuple[str, str]] = []
    with open(filename, 'r') as handler:
        next(handler)
        for line in handler:
            key, value = line.replace('\n', '').split(' ')
            if not (value, key) in interactions:
                interactions += [(key, value)]
    return interactions


def read_interaction_file_mat(filename: str) -> Tuple[np.ndarray, list[str]]:
    """Reads from an interaction file a set of interactions

    Args:
        filename (str): path to file

    Returns:
        Tuple[np.ndarray,list[str]]: distance matrix and ordered list of nodes
    """
    interactions: dict[str, list[str]] = read_interaction_file_dict(filename)
    edges: list[str] = sorted(
        list(set([key for key in chain(*interactions.values(), interactions.keys())])))
    matrix: np.ndarray = np.zeros(dtype=int, shape=(len(edges), len(edges)))
    for key, values in interactions.items():
        key_edge: int = edges.index(key)
        for value in values:
            matrix[key_edge][edges.index(value)] = 1
            matrix[edges.index(value)][key_edge] = 1
    return (np.asarray(matrix), edges)


@check_interaction_file
def read_interaction_file(filename: str) -> Tuple[dict[str, list[str]], list[Tuple[str, str]], np.ndarray, list[str]]:
    """Extracts informations from a interaction file

    Args:
        filename (str): path to file

    Returns:
        Tuple[dict[str, list[str]], list[Tuple[str, str]], np.ndarray, list[str]]: interpretation of graphs
    """
    return (read_interaction_file_dict(filename), read_interaction_file_list(filename), *read_interaction_file_mat(filename))


def count_vertices(filename: str) -> int:
    """computes the number of unique vertices 

    Args:
        filename (str): a PPI file

    Returns:
        int: the number of vertices
    """
    return len(read_interaction_file_dict(filename).keys())


def count_edges(filename: str) -> int:
    """computes the number of links between summits

    Args:
        filename (str): a PPI file

    Returns:
        int: number of edges
    """
    return len(read_interaction_file_list(filename))


def clean_interactome(filein: str, fileout: str) -> None:
    """Cleans out an interactome file

    Args:
        filein (str): path to input file
        fileout (str): path to output file
    """
    interactions: list[Tuple[str, str]] = read_interaction_file_list(filein)
    with open(fileout, 'w') as handler:
        handler.write('\n'.join(
            [len(interactions)]+[f"{key} {value}" for (key, value) in interactions]))


def get_degree(filename: str, prot: str) -> int:
    """Gives the number of proteins a specific one is linked to

    Args:
        filename (str): path to PPI file
        prot (str): name of given protein

    Returns:
        int: number of edges connected to prot, if existing, else 0
    """
    interactions: dict[str, list[str]] = read_interaction_file_dict(filename)
    return len(interactions[prot]) if prot in interactions else 0


def get_max_degree(filename: str) -> Tuple[str, int]:
    """Gives the highest degree of a PPI file

    Args:
        filename (str): PPI file to scan

    Returns:
        Tuple[str, int]: protein with max score, and max score
    """
    mapping: dict[str, int] = {key: len(value)
                               for key, value in read_interaction_file_dict(filename).items()}
    return (list(mapping.keys()).index(max(list(mapping.values()))), max(list(mapping.values())))


def get_ave_degree(filename: str) -> int:
    """Gives the approximate average degree

    Args:
        filename (str): PPI file

    Returns:
        int: average degree of PPI interactions, round at unit
    """
    return int(mean(list({key: len(value)
                          for key, value in read_interaction_file_dict(filename).items()}.values())))


def count_degree(filename: str, deg: int) -> list[str]:
    """Filters some proteins by degree

    Args:
        filename (str): PPI file
        deg (int): a degree to check

    Returns:
        list[str]: all proteins with degree equal to given score
    """
    return [k for k, v in {key: len(value) for key, value in read_interaction_file_dict(filename).items()}.items() if v == deg]


def output_histogram(data: Counter) -> None:
    """Plots histogram from counter

    Args:
        data (Counter): number of number of edges to a node
    """
    plt.bar(data.keys(), data.values())
    plt.show()


def histogram_degree(filename: str, dmin: int, dmax: int) -> None:
    """Filters some proteins by degree within range

    Args:
        filename (str): PPI file
        dmin (int): lower boundary
        dmax (int): upper boundary
    """
    output_histogram(Counter(deg for deg in [len(value) for value in read_interaction_file_dict(
        filename).values()] if deg >= dmin and deg <= dmax))


# Stratégies d'optimisation :
# > Mettre les fonctions de chargement de fichier en cache
# > Ouvrir le fichier le fichier qu'une seule fois
# > Utiliser des générateurs pour ne calculer qu'au dernier moment
# > Rassembler les fonctions en une seule
