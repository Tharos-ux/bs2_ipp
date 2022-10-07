
from ast import In
from chapitre_3 import Interactome

if __name__ == "__main__":
    graphe: Interactome = Interactome("test_files/Human_HighQuality.txt")
    print(graphe.read_interaction_file_mat())
