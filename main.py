from interactome import Interactome

if __name__ == "__main__":
    # Initialisation d'un objet Interactome
    toy_graph: Interactome = Interactome("test_files/toy_example.txt")

    # Affichage de différentes propriétés de l'objet Interactome
    print(toy_graph.int_list)
    print(toy_graph.int_mat)

    # Visualisation du graphe d'interactions
    print(toy_graph)

    # Ajout de 100 protéines selon la méthode de Barabasi-Albert
    toy_graph.barabasi_albert_graph(100)

    # Affichage de différentes propriétés après modification
    print(toy_graph.int_dict)
    print(toy_graph.int_mat)

    # Visualisation du graphe d'interactions modifié
    print(toy_graph)
