import matplotlib.pyplot as plt
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

class Ralley_Tree:
    '''In this class all the functions to generate the game tree are defined'''
    def __init__(self):
        '''Initializing a tree as a NetworkX Graph'''
        self.tree = nx.Graph()
        self.node_index = 0
        self.tree.add_node(0, type="init", shot="", depth=0)

    def add_new_edge(self, node_A, node_B):
        '''Adds a new edge between two given nodes'''
        self.tree.add_edge(node_A, node_B)

    def add_new_node(self, index, node_type, shot_string, depth):
        '''A new node is added to the tree, with an unique index, a type
        (action or state node), a shot encoding string and a depth'''
        self.tree.add_node(index,
                           type=node_type,
                           shot=shot_string,
                           depth=depth)

    def clear_tree(self):
        '''Deletes an existing tree'''
        self.tree.clear()

    def get_next_node_index(self):
        '''Returns the new index'''
        self.node_index += 1
        return self.node_index
    
    def get_node_index(self):
        '''returns the current index'''
        return self.node_index

    def get_connections(self, n):
        '''Returns all nodes, that are connected by edges to the given 
        node n'''
        x = nx.node_connected_component(self.tree, n)
        return str(x)
    
    def get_neighbors(self, n):
        '''Returns the neighbor nodes of a given node'''
        neighbor_list = self.tree.neighbors(n)
        return list(neighbor_list)

    def show_tree(self):
        '''If this function is called, it will draw the created tree'''

        nx.draw(self.tree, with_labels=True, font_weight='bold')
        # to draw a specific attribute as label: 
        # labels = nx.get_node_attributes(self.tree, 'shot')
        plt.show()




