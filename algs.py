from nodes import Node, AdjacencyNode
from collections import deque
from queue import PriorityQueue


def dfs(curr: Node, end: Node, visited:set=None, path=None, weight=0):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    
    visited.add(curr)
    path.append(curr.info)
    
    if curr == end:
        return (path, weight) # Tuple (List, Weight)
    
    temp:AdjacencyNode = curr.adj_list
    while temp:
        #neighbor: Node
        neighbor = temp.adj_node
        
        if neighbor not in visited:
            result = dfs(neighbor, end, visited, path, weight+temp.weight)
            
            if result is not None:
                return result
            
        temp = temp.next
        
    path.pop()
    return None


def bfs(start: Node, end: Node):
    queue = deque([(start, [start.info], 0)])  # Queue holds (node, path, weight)
    visited = set()
    path = []
    
    while queue:
        current, path, weight = queue.popleft()
        
        if current not in visited:
            
            if current == end:
                return (path, weight)
        
            visited.add(current)
            #Step 2: Append all neighbors of current to the queue
            temp = current.adj_list
            
            while temp:
                neighbor = temp.adj_node
                if neighbor not in visited:
                    queue.append(( neighbor , ( path + [neighbor.info] ), ( weight + temp.weight ) )) # (node, path, weight)
                
                temp = temp.next
    
    return None


def gbfs(head:Node, start:Node, end:Node):
    p_queue = PriorityQueue()
    visited = set()
    path = []
    reset_h(head)
    fill_h(end)
    
    p_queue.put( (start.h_value, start, [start.info], 0) ) # (heuristic, node, path, weight)

    while not p_queue.empty():
        h, current, path, weight = p_queue.get()
        current: Node
        
        if current in visited:
            continue
        
        if current == end:
            return (path, weight)
        
        visited.add(current)
        temp = current.adj_list
        
        while temp:
            neighbor = temp.adj_node
            if neighbor not in visited:
                p_queue.put(( neighbor.h_value, neighbor, ( path + [neighbor.info] ), ( weight + temp.weight )))
            
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
            continue  # Skip outdated queue entries

        temp: AdjacencyNode = current_node.adj_list
        while temp:
            neighbor: Node = temp.adj_node
            travel_weight = temp.weight
            new_h_value = current_node.h_value + travel_weight

            if neighbor.h_value is None or new_h_value < neighbor.h_value:
                neighbor.h_value = new_h_value
                pq.put((new_h_value, neighbor))  # Prioritize lower heuristic values

            temp = temp.next # Keep the ball rolling :)
