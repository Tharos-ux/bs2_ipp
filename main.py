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
    barabasi_albert_graph: Interactome = Interactome(args.file, method='barabasi-albert',kwargs={'m':15})
    erdos_renyi_graph: Interactome = Interactome(args.file, method='erdos-renyi',kwargs={'n':15,'q':0.3})

    for (interactome,name) in [(toy_graph,f'{args.file}'),(erdos_renyi_graph,'erdos_renyi'),(barabasi_albert_graph,'barabasi-albert')]:
    
        layout: int = 400
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
            # Plot de l'histogramme du degré des protéines
            {'button_name': "Plot histogram of degrees", 'function': Interactome.histogram_degree,
                'kwargs': {'dmin': 1,'dmax':20}},
        ]

        root = tk.Tk()
        root.geometry(f"{layout}x{(len(button_methods)*layout)//3}")
        root.title(f'Interactome {name}')
        root.resizable(0, 0)
        tk.Grid.columnconfigure(root, 0, weight=1)
        for i in range(len(button_methods)):
            tk.Grid.rowconfigure(root, i, weight=1)
        button_list = [tk.Button(master=root, text=func['button_name'], bg='#2f3136', fg='white', command=partial(
            func['function'], self=interactome, **func['kwargs'])) for func in button_methods]
        [button.grid(sticky="nswe", column=0, row=i)
        for i, button in enumerate(button_list)]
        #root.attributes("-topmost", True)
        root.mainloop()