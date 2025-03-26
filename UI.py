# Functionality Modules
import sys

# UI Modules
import tkinter as tk
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

# Local modules
from graph import head, node_collection, edges
from nodes import Node, AdjacencyNode
from algs import dfs, bfs, gbfs, dijkstra, a_star
nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", 
        "T", "U", "V", "W", "X", "Y", "Z", "T1", "T2", "CC", "FF", "Cn1", "Cn2", "Et1", "Et2", "Et3", "Et4", "Et5", "Et6"]



class UI:
    def __init__(self, master):
        # Create the main window
        self.master = master
        master.title("Recorrido del Tec")
        
        # Create NetworkX graph
        self.graph = nx.Graph()
        self.create_graph()
        
        # Selection variables
        self.start_node = None
        self.end_node = None
        self.selected_algorithm = None
        
        # Create buttons frame
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create figure and canvas
        self.figure, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Info frame
        self.info_frame = tk.Frame(master)
        self.info_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Info labels
        self.start_label = tk.Label(self.info_frame, text="Inicio: No seleccionado", fg="blue")
        self.start_label.pack(side=tk.LEFT, padx=10)
        
        self.end_label = tk.Label(self.info_frame, text="Fin: No seleccionado", fg="blue")
        self.end_label.pack(side=tk.LEFT, padx=10)
        
        # Algorithm buttons
        self.create_algorithm_buttons()
        
        # Draw initial graph
        self.draw_graph()

    
    def create_graph(self):
        self.graph.add_nodes_from(node_collection.keys())
        
        for edge in edges:
            self.graph.add_edge(edge["start"], edge["end"], weight=edge["cost"])
        
        
    def draw_graph(self):
        # Clear previous drawing
        self.ax.clear()
        self.pos = nx.spring_layout(self.graph, seed=42)
        
        # Draw nodes
        nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax, 
                                node_color=['red' if n == self.start_node else 
                                            'green' if n == self.end_node else 
                                            'lightblue' for n in self.graph.nodes()], 
                                node_size=500)
        
        # Draw edges with weights
        nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax, width=1, edge_color='gray')
        
        # Draw edge labels
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels, ax=self.ax)
        
        # Draw node labels
        nx.draw_networkx_labels(self.graph, self.pos, ax=self.ax)
        
        self.ax.set_title("Graph Visualization")
        self.ax.axis('off')
        
        # Connect click event
        self.figure.canvas.mpl_connect('button_press_event', self.on_node_click)
        
        # Redraw canvas
        self.canvas.draw()
        
        
    def on_node_click(self, event):
        pass
    
    def create_algorithm_buttons(self):
        algorithms = [
            ("DFS", self.run_dfs),
            ("BFS", self.run_bfs),
            ("Greedy BFS", self.run_gbfs),
            ("Dijkstra", self.run_dijkstra),
            ("A*", self.run_a_star)
        ]
        for name, command in algorithms:
            btn = tk.Button(self.button_frame, text=name, command=command)
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        reset_btn = tk.Button(self.button_frame, text="Reset", command=self.reset_selection)
        reset_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def run_dfs(self):
        pass
    def run_bfs(self):
        pass
    def run_gbfs(self):
        pass
    def run_dijkstra(self):
        pass
    def run_a_star(self):
        pass
    def reset_selection(self):
        self.start_node = None
        self.end_node = None
        self.selected_algorithm = None
        self.start_label.config(text="Start Node: Not Selected")
        self.end_label.config(text="End Node: Not Selected")
        self.draw_graph()

# - - - - - - - - -  Main method - - - - - - - - - - - - >
def main():
    root = tk.Tk()
    root.geometry("1400x450") # Window size
    
    # Handle window close event
    def on_closing():
        root.destroy()  
        sys.exit()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    app = UI(root)
    root.mainloop()

if __name__ == "__main__":
    main()