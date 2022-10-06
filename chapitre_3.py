from code import interact
from curses.ascii import isalpha
from xml.sax.handler import property_declaration_handler
from xmlrpc.client import Boolean
import numpy as np
from itertools import chain
from os import system


class Interactome:

    def __init__(self, file, fileout=clean_int_graph.txt):
        """ Initialisation of the attributes """
        if self.is_interaction_file(self, file):
            self.write_clean_interactome(self, file, fileout)
            self.file = fileout
            self.int_list, self.int_dict = self.read_interaction_file(
                self.file)
            value = list(self.int_dict.values())
            self.proteins = sorted(set(key + list(chain(*value))))
        else:
            raise ValueError("File is not an interaction file")

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
        if not isinstance(new_proteins, set):
            raise ValueError("Expecting a set")
        self.__proteins = new_proteins

    def is_interaction_file(self, file) -> Boolean:
        with open(file, "r") as f:
            try:
                size_file = int(f.readline())
            except ValueError:
                return False
            if size_file == 0:
                return False
            for i, line in enumerate(f):
                res = line.split(" ")
                if len(res) != 2:
                    return False
            if i != size_file-1:
                return False
        return True

    def clean_interactome(self, filein) -> list:
        list_interactions = list()
        with open(filein, "r") as f:
            next(f)
            for line in f:
                line_interaction = line.split()
                if line_interaction[::-1] not in list_interactions:
                    if line_interaction[0] != line_interaction[1]:
                        list_interactions.append(line_interaction)
        return list_interactions, len(list_interactions)

    def write_clean_interactome(self, filein, fileout) -> None:
        list_interactions, nb_interactions = clean_interactome(filein)
        with open(fileout, "w") as f:
            f.write(str(nb_interactions)+"\n")
            for item in list_interactions:
                f.write(f"{str(item[0])} {str(item[1])}\n")

    def read_interaction_file(self, file):
        list_interactions = list()
        dico_interactions = dict()
        with open(file, "r") as f:
            next(f)
            for line in f:
                list_interactions.append(tuple(line.split()))
                key, value = line.split()
                dico_interactions.setdefault(key, []).append(value)
        return list_interactions, dico_interactions

    def read_interaction_file_mat(self):
        interaction = self.int_dict
        key = list(interaction.keys())
        value = list(interaction.values())
        liste_sommets = sorted(set(key + list(chain(*value))))
        dim = len(liste_sommets)
        mat = np.zeros([dim, dim], dtype=int)
        for key2, value2 in interaction.items():
            col = liste_sommets.index(key2)
            for item in value2:
                ligne = liste_sommets.index(item)
                mat[ligne][col] = 1
                mat[col][ligne] = 1
        return mat, liste_sommets

    def count_vertices(self) -> int:
        interaction = self.int_dict
        key = list(interaction.keys())
        value = list(interaction.values())
        return len(sorted(set(key + list(chain(*value)))))

    def count_edges(self) -> int:
        interaction = self.int_dict
        value = list(interaction.values())
        return len(list(chain(*value)))

    def get_degree(self, prot: str) -> int:
        interactions = self.int_dict
        return len(interactions[prot])

    def get_max_degree(self):
        interactions = self.int_dict
        max_interactions = 0
        for key, value in interactions.items():
            len_val = len(value)
            if len_val > max_interactions:
                max_interactions = len_val
                return key, len_val

    def get_ave_degree(self) -> float:
        interactions = self.int_dict
        somme = 0
        len_graph = len(interactions.values())
        for value in interactions.values():
            somme += len(value)
        return somme/len_graph

    def count_degree(self, deg: int) -> int:
        interactions = self.int_dict
        i = 0
        for value in interactions.values():
            if len(value) == deg:
                i += 1
        return i

    def histogram_degree(self, dmin: int, dmax: int) -> str:
        interactions = self.int_dict
        dico = dict()
        for value in interactions.values():
            len_value = len(value)
            if len_value <= dmax and len_value >= dmin:
                dico[len_value] = dico.setdefault(len_value, 0) + 1
        for item in range(dmin, dmax+1):
            if item in dico.keys():
                print(str(item) + "*"*dico[item])
