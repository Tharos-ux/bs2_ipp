
from chapitre_3 import Interactome

if __name__ == "__main__":
    graphe: Interactome = Interactome("test_files/test_05.txt")
    print(graphe.clean_interactome())
