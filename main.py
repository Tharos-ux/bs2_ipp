from argparse import ArgumentParser
from interactome import Interactome
from functools import partial
import tkinter as tk
import matplotlib.pyplot as plt

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "file", help="Path to a interactome file", type=str)
    args = parser.parse_args()
    # Initialisation d'un objet Interactome
    toy_graph: Interactome = Interactome(args.file)
    print(toy_graph.clustering("F"))

    
'''
    layout: int = 200
    button_methods: list[dict] = [
        # Visualisation du graphe d'interactions coloré par degré
        {'button_name': "Color by degree", 'function': Interactome.draw,
            'kwargs': {'method': Interactome.color_by_neighbors}},
        # Visualisation du graphe d'interactions coloré par composante connexe
        {'button_name': "Color by connectivity", 'function': Interactome.draw,
            'kwargs': {'method': Interactome.color_by_connectivity, 'colormap': plt.cm.YlOrRd}},
        # Ajout de 20 protéines selon la méthode de Barabasi-Albert
        {'button_name': "Add 20 nodes (Barabasi-Albert)", 'function': Interactome.barabasi_albert_graph,
            'kwargs': {'m': 20}},
    ]

    root = tk.Tk()
    root.geometry(f"{layout}x{(len(button_methods)*layout)//3}")
    root.title('Switcher')
    root.resizable(0, 0)
    tk.Grid.columnconfigure(root, 0, weight=1)
    for i in range(len(button_methods)):
        tk.Grid.rowconfigure(root, i, weight=1)
    button_list = [tk.Button(master=root, text=func['button_name'], bg='#2f3136', fg='white', command=partial(
        func['function'], self=toy_graph, **func['kwargs'])) for func in button_methods]
    [button.grid(sticky="nswe", column=0, row=i)
     for i, button in enumerate(button_list)]
    root.attributes("-topmost", True)
    root.mainloop()

    # Affichage de différentes propriétés de l'objet Interactome
    # print(toy_graph.int_list)
    # print(toy_graph.int_mat)

    # Affichage de différentes propriétés après modification
    # print(toy_graph.int_dict)
    # print(toy_graph.int_mat)
'''