from curses.ascii import isalpha
import numpy as np
from itertools import chain
from os import system #cmd bash ou check pathlib

def read_interaction_file_dict(file):
    dico_interactions = dict()
    with open(file,"r") as f:
        next(f)
        for line in f:
            key, value = line.split()
            if value in dico_interactions.keys() and key in dico_interactions[value]:  
                pass                        
            else :
                dico_interactions.setdefault(key,[]).append(value)
    return dico_interactions
        
#print(read_interaction_file_dict("toy_example.txt"))

def read_interaction_file_list(file):
    list_interactions = list()
    with open(file,"r") as f:
        next(f)
        for line in f:
            if tuple(line.split())[::-1] not in list_interactions:
                list_interactions.append(tuple(line.split())) 
    return list_interactions

#print(read_interaction_file_list("toy_example.txt"))

def read_interaction_file_mat(file):
    interaction = read_interaction_file_dict(file)
    key = list(interaction.keys())
    value = list(interaction.values())
    liste_sommets = sorted(set(key + list(chain(*value))))
    dim = len(liste_sommets)
    mat = np.zeros([dim,dim],dtype=int)
    for key2, value2 in interaction.items():
        col = liste_sommets.index(key2)
        for item in value2:
            ligne = liste_sommets.index(item)
            mat[ligne][col] = 1
            mat[col][ligne] = 1
    return mat, liste_sommets

#print(read_interaction_file_mat("toy_example.txt"))

def read_interaction_file(file):
    d_int = read_interaction_file_dict(file)
    l_int = read_interaction_file_list(file)
    m_int,l_som = read_interaction_file_mat(file)
    return d_int, l_int, m_int, l_som

# Question 5 => optimiser pour lire le fichier qu'une fois

def is_interaction_file(file):
    with open(file, "r") as f:
        try:
            size_file = int(f.readline())
        except ValueError:
            return False
        #finally: s'execute forcement même si il y a une erreur            
        if size_file == 0:
            return False
        for i,line in enumerate(f):
            res = line.split(" ")
            if len(res) != 2:
                return False
        if i != size_file-1:
            return False
    return True
    
print(is_interaction_file("toy_example.txt"))
        
            

        
#if not isinstance(size_file, int):
#    return False
    