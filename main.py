from interactome import Interactome

if __name__ == "__main__":
    # Initialisation d'un objet Interactome
    toy_graph: Interactome = Interactome("test_files/toy_example.txt")

    # Visualisation du graphe d'interactions
    print(toy_graph)
