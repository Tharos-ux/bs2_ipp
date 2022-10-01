from code import interact
from curses.ascii import isalpha
import numpy as np
from itertools import chain
from os import system  # cmd bash ou check pathlib


def read_interaction_file_dict(file):
    dico_interactions = dict()
    with open(file, "r") as f:
        next(f)
        for line in f:
            key, value = line.split()
            if value in dico_interactions.keys() and key in dico_interactions[value]:
                pass
            else:
                dico_interactions.setdefault(key, []).append(value)
    return dico_interactions

# print(read_interaction_file_dict("toy_example.txt"))


def read_interaction_file_list(file):
    list_interactions = list()
    with open(file, "r") as f:
        next(f)
        for line in f:
            if tuple(line.split())[::-1] not in list_interactions:
                list_interactions.append(tuple(line.split()))
    return list_interactions

# print(read_interaction_file_list("toy_example.txt"))


def read_interaction_file_mat(file):
    interaction = read_interaction_file_dict(file)
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

# print(read_interaction_file_mat("toy_example.txt"))


def read_interaction_file(file):
    d_int = read_interaction_file_dict(file)
    l_int = read_interaction_file_list(file)
    m_int, l_som = read_interaction_file_mat(file)
    return d_int, l_int, m_int, l_som

# Question 5 => optimiser pour lire le fichier qu'une fois


def is_interaction_file(file):
    with open(file, "r") as f:
        try:
            size_file = int(f.readline())
        except ValueError:
            return False
        # finally: s'execute forcement même si il y a une erreur
        if size_file == 0:
            return False
        for i, line in enumerate(f):
            res = line.split(" ")
            if len(res) != 2:
                return False
        if i != size_file-1:
            return False
    return True

# print(is_interaction_file("toy_example.txt"))


# if not isinstance(size_file, int):
#    return False

# Chapitre 2

def count_vertices(file):
    interaction = read_interaction_file_dict(file)
    key = list(interaction.keys())
    value = list(interaction.values())
    return len(sorted(set(key + list(chain(*value)))))

# print(count_vertices("toy_example.txt"))


def count_edges(file):
    interaction = read_interaction_file_dict(file)
    value = list(interaction.values())
    return len(list(chain(*value)))

# print(count_edges("toy_example.txt"))

#import csv
#import pandas as pd


def clean_interactome(filein):
    list_interactions = list()
    with open(filein, "r") as f:
        next(f)
        for line in f:
            line_interaction = line.split()
            if line_interaction[::-1] not in list_interactions:
                if line_interaction[0] != line_interaction[1]:
                    list_interactions.append(line_interaction)

    return list_interactions, len(list_interactions)


def write_clean_clean_interactome(filein, fileout):
    list_interactions, nb_interactions = clean_interactome(filein)
    with open(fileout, "w") as f:
        f.write(str(nb_interactions)+"\n")
        for item in list_interactions:
            f.write(f"{str(item[0])} {str(item[1])}\n")

# print(write_clean_clean_interactome("toy_example.txt", "toy_clean.txt"))


def get_degree(file, prot):
    interactions = read_interaction_file_dict(file)
    return len(interactions[prot])

# print(get_degree("toy_example.txt", "B"))


def get_max_degree(file):
    interactions = read_interaction_file_dict(file)
    max_interactions = 0
    for key, value in interactions.items():
        len_val = len(value)
        if len_val > max_interactions:
            max_interactions = len_val
            return key, len_val

# print(get_max_degree("toy_example.txt"))


def get_ave_degree(file):
    interactions = read_interaction_file_dict(file)
    somme = 0
    len_graph = len(interactions.values())
    for value in interactions.values():
        somme += len(value)
    return somme/len_graph

# print(get_ave_degree("toy_example.txt"))


def count_degree(file, deg):
    interactions = read_interaction_file_dict(file)
    i = 0
    for value in interactions.values():
        if len(value) == deg:
            i += 1
    return i

#print(count_degree("toy_example.txt", 2))


def histogram_degree(file, dmin, dmax):
    interactions = read_interaction_file_dict(file)
    dico = dict()
    for value in interactions.values():
        len_value = len(value)
        if len_value <= dmax and len_value >= dmin:
            dico[len_value] = dico.setdefault(len_value, 0) + 1
    for item in range(dmin, dmax+1):
        if item in dico.keys():
            print(str(item) + "*"*dico[item])


histogram_degree("Human_HighQuality.txt", 25, 50)


'''

                    
                    
    df = pd.read_csv(filein, sep='\s', names=['a', 'b'], engine='python')
    print(df.iat[0,0])
    display(df.drop_duplicates())
    #df.drop([row])
    print(df.iat[5,1])
'''
