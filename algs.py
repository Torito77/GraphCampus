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


def gbfs(head:Node, start:Node, end:Node):
    p_queue = PriorityQueue()
    visited = set()
    path = []
    reset_h(head)
    fill_h(end)
    
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


def aStar(head:Node, start: Node, end: Node):
    pq = PriorityQueue()
    distances = {start: 0} 
    visited = set()
    
    reset_h(head)
    fill_h(end)
    
    # f = cost + h
    pq.put((start.h_value, 0, start, [start.info]))  # (f, cost, node, path)
    
    while not pq.empty():
        f, cost, current, path = pq.get()
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


# - Heuritstic management methods - - - - - - - - - - - - - - - - - - - - - - - >
def reset_h(head: Node):
    temp = head
    while temp is not None:
        temp.h_value = None
        temp = temp.next

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
