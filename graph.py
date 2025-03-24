import pandas
from nodes import Node, AdjacencyNode, insert_node, print_nodes
from algs import dfs, bfs, gbfs, dijkstra, a_star

nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", 
        "T", "U", "V", "W", "X", "Y", "Z", "T1", "T2", "CC", "FF", "Cn1", "Cn2", "Et1", "Et2", "Et3", "Et4", "Et5", "Et6"]

node_collection: dict[Node] = {}

for node in nodes:
    new_node = Node(info=node)
    # # TODO: Initialize positions here
    # new_node.xPos = X
    # new_node.yPos = Y
    
    node_collection[node] = new_node

# Save the linked list that contains all the nodes
# Used later in methods that require heuristic
head: Node = node_collection[nodes[0]]


#Adjacency's
data = pandas.read_csv("./data/weight_data.csv")
for (index, row) in data.iterrows():
    start: Node = node_collection[row["start"]]
    end: Node = node_collection[row["end"]]
    cost = float(row["cost"])
    
    start.add_adjacent(AdjacencyNode(
        cost=cost,
        adj_node=end
    ))
    end.add_adjacent(AdjacencyNode(
        cost=cost,
        adj_node=start
    ))

# for value in node_collection.values():
#     value:Node
#     print(f"{value.info} -> ", end="")
#     print_nodes(value.adj_list)
#     print()

start_node = node_collection["S"]
end_node = node_collection["M"]
# dfs_path = dfs(start_node, end_node)
# bfs_path = bfs(start_node, end_node)
# gbfs_path = gbfs(head, start_node, end_node)
# dijkstra_path = dijkstra(start_node, end_node)
a_star_path = a_star(head, start_node, end_node)
print(f"A*: {a_star_path}")
