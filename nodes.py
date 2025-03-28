from __future__ import annotations


class MasterNode:
    def __init__(self, next: MasterNode = None):
        self.next = next
        
class Node(MasterNode):
    def __init__(self, info: str = None, h_value:float = None, adj_list: AdjacencyNode = None, next: Node = None):
        super().__init__()
        self.info:str = info
        self.next:Node = next
        self.adj_list:AdjacencyNode = adj_list
        self.h_value:float = h_value
        self.xPos:int
        self.yPos:int
    
    def add_adjacent(self, new_node: AdjacencyNode):
        self.adj_list = insert_node(head=self.adj_list, new_node=new_node)
    
    # This is just so the priority queue does not break
    def __lt__(self, other):
        h1 = self.h_value if self.h_value else float("inf")
        h2 = other.h_value if other.h_value else float("inf")
        return h1 < h2
    
    def __repr__(self):
        return f"Node: {self.info}"

class AdjacencyNode(MasterNode):
    def __init__(self, cost:float, adj_node:Node, next: AdjacencyNode = None):
        super().__init__()
        self.cost: float = cost
        self.adj_node: Node = adj_node
        self.next: AdjacencyNode = next
        
        
def insert_node(head:MasterNode, new_node: MasterNode):
        if head is None:
            head = new_node
            return head
        
        temp = head
        while temp.next:
            temp = temp.next
        
        temp.next = new_node
        return head


def print_nodes(head: MasterNode):
        temp = head
        while(temp):
            if type(temp) == Node:
                temp:Node
                print(f"{temp.info} -> ", end="")
            elif type(temp) == AdjacencyNode:
                temp:AdjacencyNode
                print(f"{temp.adj_node.info}: {temp.cost} -> ", end="")
                
            temp = temp.next
