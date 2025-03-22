import pandas
from nodes import Node, AdjacencyNode, insert_node, print_nodes
from algs import dfs, bfs, gbfs
# from algs import fill_h

nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", 
        "T", "U", "V", "W", "X", "Y", "Z", "T1", "T2", "CC", "FF", "Cn1", "Cn2", "Et1", "Et2", "Et3", "Et4", "Et5", "Et6"]

node_collection: dict[Node] = {}

for node in nodes:
    new_node = Node(info=node)
    # # TODO: Initialize positions here
    # new_node.xPos = X
    # new_node.yPos = Y
    
    node_collection[node] = new_node
    
head: Node = node_collection[nodes[0]]


#Adjacency's
data = pandas.read_csv("./data/weight_data.csv")
for (index, row) in data.iterrows():
    start: Node = node_collection[row["start"]]
    end: Node = node_collection[row["end"]]
    weight = float(row["weight"])
    
    start.add_adjacent(AdjacencyNode(
        weight=weight,
        adj_node=end
    ))
    end.add_adjacent(AdjacencyNode(
        weight=weight,
        adj_node=start
    ))

# for value in node_collection.values():
#     value:Node
#     print(f"{value.info} -> ", end="")
#     print_nodes(value.adj_list)
#     print()

start_node = node_collection["W"]
end_node = node_collection["Cn1"]
#dfs_path = dfs(start_node, end_node)
#bfs_path = bfs(start_node, end_node)
gbfs_path = gbfs(head, start_node, end_node)
print(f"GBFS path: {gbfs_path}")

# fill_h(node_collection["Z"])
# print("Heuristic: ")
# for value in node_collection.values():
#     value:Node
#     print(f"{value.info}: {value.h_value}")