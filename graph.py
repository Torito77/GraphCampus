import pandas
from nodes import Node, AdjacencyNode, insert_node, print_nodes
from algs import dfs, bfs, gbfs, dijkstra, a_star


positions_df = pandas.read_csv('./data/positions.csv')
node_collection: dict[Node] = {}

max_x_pos = positions_df['x'].max()
max_y_pos = positions_df['y'].max()

for _, row in positions_df.iterrows():
    new_node = Node(info=row['nodes'])
    new_node.xPos = row['x']
    new_node.yPos = row['y']
    
    node_collection[row['nodes']] = new_node


edges = []
# Adjacency's
data = pandas.read_csv("./data/weight_data.csv")
for (index, row) in data.iterrows():
    start: Node = node_collection[row["start"]]
    end: Node = node_collection[row["end"]]
    cost = float(row["cost"])
    
    edges.append( {"start":start.info, "end":end.info, "cost":cost} )
    
    start.add_adjacent(AdjacencyNode(
        cost=cost,
        adj_node=end
    ))
    end.add_adjacent(AdjacencyNode(
        cost=cost,
        adj_node=start
    ))

