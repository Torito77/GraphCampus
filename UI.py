# Functionality Modules
import sys

# UI Modules
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Local modules
from graph import node_collection, edges, max_x_pos, max_y_pos
from nodes import Node
from algs import set_h, dfs, bfs, gbfs, dijkstra, a_star, hill_climbing


bg_color = "#F0F5F9"  # Lightest
frame_color = "#C9D6DF"  # Light grey-blue
button_color = "#52616B"  # Dark grey-blue
text_color = "#F0F5F9"  # Light text
hover_color = "#1E2022"  # Darkest for hover effect

class UI:
    def __init__(self, master):
        
        # Create the main window
        self.master = master
        master.title("Recorrido del Tec")
        master.configure(bg=bg_color)
        
        # Create NetworkX graph
        self.graph = nx.Graph()
        self.create_graph()
        
        # Selection variables
        self.start_node: str = None
        self.end_node: str = None
        
        # Result variables
        self.path_found = None
        self.weight_found = None
        
        # Button frame
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.button_frame.configure(bg="#52616B")
        
        # Info frame
        self.info_frame = tk.Frame(master)
        self.info_frame.pack(side=tk.TOP, fill=tk.X)
        self.info_frame.configure(bg="#52616B")
        
        # Create figure and canvas
        self.figure, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Info labels
        self.start_label = tk.Label(self.info_frame, text="Nodo inicial:", fg=text_color, bg="#52616B")
        self.start_label.pack(side=tk.LEFT, padx=10)
        
        self.end_label = tk.Label(self.info_frame, text="Nodo final:", fg=text_color, bg="#52616B")
        self.end_label.pack(side=tk.LEFT, padx=10)
        
        self.cost_label = tk.Label(self.info_frame, text="", fg=text_color, bg="#52616B")
        self.cost_label.pack(side=tk.LEFT, padx=10)
        
        # Algorithm buttons
        self.create_algorithm_buttons()
        
        # Draw initial graph
        self.draw_graph()

    # - - - - - - - - - - - - - - Graph design and drawing - - - - - - - - - - - - - - - - - - - - - >
    def create_graph(self):
        self.graph.add_nodes_from(node_collection.keys())
        
        for edge in edges:
            self.graph.add_edge(edge["start"], edge["end"], weight=edge["cost"])
        
        
    def draw_graph(self):
        # Clear previous drawing
        self.ax.clear()
        
        self.pos = {}
        for key, value in node_collection.items():
            
            value:Node
            # Normalize coordinates to be between 0 and 1 for NetworkX layout
            self.pos[key] =  ( value.xPos / max_x_pos, 
                            self.master.winfo_height() - value.yPos / max_y_pos ) # TODO: Make the graph stay the same when window gets resized
            

        # Draw nodes
        nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax, 
                                node_color=['#5376A3' if n == self.start_node else 
                                            '#4B8A6E' if n == self.end_node else 
                                            '#D9EAFD' for n in self.graph.nodes()], 
                                node_size=500)
        
        # Determine edge colors depending the path found
        if self.path_found:
            path_connections = set()
            for i in range( len(self.path_found)-1 ):
                path_connections.add((self.path_found[i], self.path_found[i+1]))
            
            edge_colors = []
            edge_widths = []
            for (u, v) in self.graph.edges():
                if (u, v) in path_connections or (v, u) in path_connections:
                    edge_colors.append('#3F72AF')  
                    edge_widths.append(2)  
                else: 
                    # Normal edge
                    edge_colors.append('gray')  
                    edge_widths.append(1)  
        else:
            edge_colors = "gray"
            edge_widths = 1
        
        # Draw edges
        nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax, width=edge_widths, edge_color=edge_colors)
        
        # Draw node labels
        nx.draw_networkx_labels(self.graph, self.pos, ax=self.ax)
        
        self.ax.set_title("Grafo-Tec")
        self.ax.axis('off')
        
        # Click event
        self.figure.canvas.mpl_connect('button_press_event', self.on_node_click)
        
        # Redraw canvas
        self.canvas.draw()
        
    def is_edge_in_path(self, u, v):
        # Check if the edge exists in consecutive nodes of the path
        for i in range(len(self.path_found) - 1):
            if (self.path_found[i] == u and self.path_found[i+1] == v) or (self.path_found[i] == v and self.path_found[i+1] == u):
                return True
        
        return False
    
    # - - - - Graph clicking & node selection - - - - - >
    def on_node_click(self, event):
        # Check if click is on a node
        if event.inaxes != self.ax:
            return
        
        # Find the closest node to the click
        node = self.find_closest_node(event)
        
        if node:
            # If no start node, set start node
            if not self.start_node:
                self.start_node = node
                self.start_label.config(text=f"Nodo inicial: {node}")
                
            # If start node is set but no end node, set end node
            elif not self.end_node and node != self.start_node:
                self.end_node = node
                self.end_label.config(text=f"Nodo final: {node}")
                
            # If both nodes are set, reset selection
            else:
                self.start_node = node
                self.end_node = None
                self.path_found = None
                self.weight_found = None
                self.start_label.config(text=f"Nodo inicial: {node}")
                self.end_label.config(text="Nodo final:")
            
            # Redraw graph to update node colors
            self.draw_graph()
    
    def find_closest_node(self, event):
        # Find the node closest to the click 
        closest_node = None
        min_dist = float('inf')
        for node, (x, y) in self.pos.items():
            # Convert node to position
            node_x, node_y = self.ax.transData.transform((x, y))
            
            # Calculate distance
            dist = ((event.x - node_x)**2 + (event.y - node_y)**2)**0.5
            
            # If close enough (20 pixels)
            if (dist < 20) and (dist < min_dist):
                closest_node = node
                min_dist = dist
                
        return closest_node
    
    # - - - - - - - - Algorithm buttons - - - - - - - - >
    def create_algorithm_buttons(self):
        algorithms = [
            ("DFS", dfs),
            ("BFS", bfs),
            ("GBFS", gbfs),
            ("Dijkstra", dijkstra),
            ("A*", a_star),
            ("Hill Climbing", hill_climbing)
        ]
        for name, algorithm in algorithms:
            btn = tk.Button(self.button_frame, 
                            text=name, 
                            bg=button_color, 
                            fg=text_color, 
                            activebackground=hover_color, 
                            activeforeground=text_color,
                            command=lambda alg=algorithm: self.run_algorithm(alg))
            btn.pack(side=tk.LEFT, padx=5, pady=7)
        
        reset_btn = tk.Button(
            self.button_frame, 
            text="Reiniciar", 
            bg=button_color, 
            fg=text_color, 
            activebackground=hover_color, 
            activeforeground=text_color,
            command=self.reset_selection)
        
        reset_btn.pack(side=tk.LEFT, padx=5, pady=7)
    
    def run_algorithm(self, algorithm):
        if self.start_node and self.end_node:
            start = node_collection[self.start_node]
            end = node_collection[self.end_node]
            
            if algorithm in [gbfs, a_star, hill_climbing]:
                set_h(node_collection, end)
            
            result = algorithm(start, end)
            if result:
                self.path_found, self.weight_found = result
                self.cost_label.config(text=f"Coste: {round(self.weight_found,1)} segundos")
                self.draw_graph()
            
    
    def reset_selection(self):
        self.start_node = None
        self.end_node = None
        self.path_found = None
        
        self.start_label.config(text="Nodo inicial: ")
        self.end_label.config(text="Nodo final: ")
        self.cost_label.config(text="")
        
        self.draw_graph()
    
# - - - - - - - - -  Main method - - - - - - - - - - - - >
def main():
    root = tk.Tk()
    root.geometry("1400x450") # Window size
    
    # Handle window close event
    def on_closing():
        plt.close('all')
        root.destroy()  
        sys.exit()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    app = UI(root)
    root.mainloop()

if __name__ == "__main__":
    main()