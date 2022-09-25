
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
        for value in values:
            matrix[edges.index(key)][edges.index(value)] = 1
            matrix[edges.index(value)][edges.index(key)] = 1
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
    return len(read_interaction_file_dict(filename).keys())


def count_edges(filename: str) -> int:
    return len(read_interaction_file_list(filename))


def clean_interactome(filein: str, fileout: str) -> None:
    interactions: list[Tuple[str, str]] = read_interaction_file_list(filein)
    with open(fileout, 'w') as handler:
        handler.write('\n'.join(
            [len(interactions)]+[f"{key} {value}" for (key, value) in interactions]))


def get_degree(filename: str, prot: str) -> int:
    interactions: dict[str, list[str]] = read_interaction_file_dict(filename)
    return len(interactions[prot]) if prot in interactions else 0


def get_max_degree(filename: str) -> Tuple[str, int]:
    mapping: dict[str, int] = {key: len(value)
                               for key, value in read_interaction_file_dict(filename).items()}
    return (list(mapping.keys()).index(max(list(mapping.values()))), max(list(mapping.values())))


def get_ave_degree(filename: str) -> int:
    return int(mean(list({key: len(value)
                          for key, value in read_interaction_file_dict(filename).items()}.values())))


def count_degree(filename: str, deg: int) -> list[str]:
    return [k for k, v in {key: len(value) for key, value in read_interaction_file_dict(filename).items()}.items() if v == deg]


def histogram_degree(filename: str, dmin: int, dmax: int) -> None:
    return Counter(deg for deg in [len(value) for value in read_interaction_file_dict(filename).values()] if deg >= dmin and deg <= dmax)


def output_histogram(data: Counter) -> None:
    plt.bar(data.keys(), data.values())
    plt.show()
