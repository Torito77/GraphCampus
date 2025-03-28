from nodes import Node, AdjacencyNode
from collections import deque
from queue import PriorityQueue


# - Search methods - - - - - - - - - - - - - - - - - - - - - - - >
def dfs(curr: Node, end: Node, visited:set=None, path=None, cost=0):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    
    visited.add(curr)
    path.append(curr.info)
    
    if curr == end:
        return (path, cost) # Tuple (List, cost)
    
    temp:AdjacencyNode = curr.adj_list
    while temp:
        #neighbor: Node
        neighbor = temp.adj_node
        
        if neighbor not in visited:
            result = dfs(neighbor, end, visited, path, cost+temp.cost)
            
            if result is not None:
                return result
            
        temp = temp.next
        
    path.pop()
    return None


def bfs(start: Node, end: Node):
    queue = deque([(start, [start.info], 0)])  # Queue holds (node, path, cost)
    visited = set()
    path = []
    
    while queue:
        current, path, cost = queue.popleft()
        
        if current not in visited:
            
            if current == end:
                return (path, cost)
        
            visited.add(current)
            #Step 2: Append all neighbors of current to the queue
            temp = current.adj_list
            
            while temp:
                neighbor = temp.adj_node
                if neighbor not in visited:
                    queue.append(( neighbor , ( path + [neighbor.info] ), ( cost + temp.cost ) )) # (node, path, cost)
                
                temp = temp.next
    
    return None


def gbfs(start:Node, end:Node):
    p_queue = PriorityQueue()
    visited = set()
    path = []
    
    p_queue.put( (start.h_value, start, [start.info], 0) ) # (heuristic, node, path, cost)

    while not p_queue.empty():
        h, current, path, cost = p_queue.get()
        current: Node
        
        if current in visited:
            continue
        
        if current == end:
            return (path, cost)
        
        visited.add(current)
        temp = current.adj_list
        
        while temp:
            neighbor = temp.adj_node
            if neighbor not in visited:
                p_queue.put(( neighbor.h_value, neighbor, ( path + [neighbor.info] ), ( cost + temp.cost )))
            
            temp = temp.next
    return None


def dijkstra(start: Node, end: Node):
    pq = PriorityQueue()
    pq.put( (0, start, [start.info]) )  # (cost, node, path)
    distances = {start: 0}  # (node, acummulated cost)
    visited = set()

    while not pq.empty():
        cost, current, path = pq.get()
        current: Node
        
        if current in visited:
            continue
        
        if current == end:
            return (path, cost)
        
        visited.add(current)
        
        temp = current.adj_list
        while temp:
            neighbor = temp.adj_node
            new_cost = cost + temp.cost

            if (neighbor not in distances) or (new_cost < distances[neighbor]):
                distances[neighbor] = new_cost
                pq.put((new_cost, neighbor, path + [neighbor.info]))
            
            temp = temp.next
    
    return None


def a_star(start: Node, end: Node):
    pq = PriorityQueue()
    distances = {start: 0} # {node: cost}
    visited = set()
    
    # weight = cost + h
    pq.put((start.h_value, 0, start, [start.info]))  # (weight, cost, node, path)
    
    while not pq.empty():
        weight, cost, current, path = pq.get()
        current: Node
        
        if current in visited:
            continue
        
        if current == end:
            return (path, cost)
        
        visited.add(current)
        
        temp = current.adj_list
        while temp:
            neighbor = temp.adj_node
            new_cost = cost + temp.cost
            new_weight = new_cost + neighbor.h_value
            
            if (neighbor not in distances) or (new_cost < distances[neighbor]):
                distances[neighbor] = new_cost
                pq.put( ( new_weight, new_cost, neighbor, (path + [neighbor.info]) ) )
                
            temp = temp.next
    
    return None


def hill_climbing(start: Node, end: Node):
    current = start
    path = [current.info]
    cost = 0
    visited = set()
    
    while current != end:
        visited.add(current)
        best_neighbor = None
        best_h_value = float('inf')
        
        temp = current.adj_list
        while temp:
            neighbor = temp.adj_node
            if neighbor not in visited and neighbor.h_value < best_h_value:
                best_neighbor = neighbor
                best_h_value = neighbor.h_value
                best_cost = temp.cost

            temp = temp.next
        
        if best_neighbor is None or best_h_value >= current.h_value:
            break 
        
        current = best_neighbor
        cost += best_cost
        path.append(current.info)
    
    return (path, cost) if current == end else None

# - Heuritstic management methods - - - - - - - - - - - - - - - - - - - - - - - >

def set_h(all_nodes:dict[Node], end:Node):
    if end.h_value == 0:
        return
    
    for n in all_nodes.values():
        n: Node
        n.h_value = None
    
    fill_h(end)


def fill_h(end_node: Node) -> None:
    end_node.h_value = 0
    pq = PriorityQueue()
    pq.put((0, end_node))  # (h, node)
    
    while not pq.empty():
        current_h, current_node = pq.get()

        if current_node.h_value < current_h:
            continue  # Skip outdated queue entries; Dijkstra Style

        temp: AdjacencyNode = current_node.adj_list
        while temp:
            neighbor: Node = temp.adj_node
            travel_cost = temp.cost
            new_h_value = current_node.h_value + travel_cost

            if neighbor.h_value is None or new_h_value < neighbor.h_value:
                neighbor.h_value = new_h_value
                pq.put((new_h_value, neighbor)) 

            temp = temp.next # Keep the ball rolling :)
