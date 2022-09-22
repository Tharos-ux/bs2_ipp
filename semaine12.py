
from typing import Callable, Tuple
import numpy as np
from itertools import chain


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
                if len(line.replace('\n', '').split(' ')) != 2:
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
            key,value = line.replace('\n', '').split(' ')
            if value in interactions and key in interactions[value]:
                pass
            else:
                interactions[key] = [value] if key not in interactions else interactions[key]+[value]
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
                interactions+=[(key,value)]
    return interactions


def read_interaction_file_mat(filename: str) -> Tuple[np.ndarray, list[str]]:
    # TODO
    interactions: dict[str,list[str]] = read_interaction_file_dict(filename)

    edges:list[str] = sorted(list(set([key for key in chain(*interactions.values(),interactions.keys())])))
    matrix:np.ndarray = np.zeros(shape=(len(edges), len(edges)))
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


print(read_interaction_file('toy_example.txt'))
