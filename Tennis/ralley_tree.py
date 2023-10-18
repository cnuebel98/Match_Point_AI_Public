import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

# ToDo: track the path as a list of node indexes that were taken per ralley
# ToDo: When the server switches, there needs to be a if statement that 
# catches that (Maybe in mainloop update tree function with colors)

class Ralley_Tree:
    '''In this class all the functions to generate the game tree are defined'''
    def __init__(self):
        '''Initializing a tree as a NetworkX Graph'''
        self.tree = nx.DiGraph()
        self.node_index = 0
        self.tree.add_node(0, color="red", type="init", shot="", depth=0)
        self.active_node = 0

    def add_new_edge(self, node_A, node_B):
        '''Adds a new edge between two given nodes'''
        self.tree.add_edge(node_A, node_B)

    def add_new_node(self, index, color, node_type, shot_string, depth):
        '''A new node is added to the tree, with an unique index, a type
        (action or state node), a shot encoding string and a depth'''
        self.tree.add_node(index,
                           color=color,
                           type=node_type,
                           shot=shot_string,
                           depth=depth)

    def clear_tree(self):
        '''Deletes an existing tree'''
        self.tree.clear()

    def get_next_node_index(self):
        '''Adds +1 to current node index and returns the new index'''
        self.node_index += 1
        return self.node_index
    
    def get_active_node(self):
        '''Returns the node from which a shot is played'''
        return self.active_node
    
    def set_active_node(self, node):
        '''Makes a given Node the active Node'''
        self.active_node = node

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
    
    def get_shot_list_of_neighbors(self, node):
        '''This function returns a list of shots of the neighbor nodes
        of a given node'''
        shots_of_neighbor_nodes = []
        neighbor_nodes = list(self.tree.neighbors(node))
        shots_of_all_nodes = nx.get_node_attributes(self.tree, 'shot')
        
        for n in neighbor_nodes:
            shots_of_neighbor_nodes.append(shots_of_all_nodes[n])

        return shots_of_neighbor_nodes
    
    def get_color_list_of_neighbors(self, node):
        '''This function returns a list of shots of the neighbor nodes
        of a given node'''
        colors_of_neighbor_nodes = []
        neighbor_nodes = list(self.tree.neighbors(node))
        colors_of_all_nodes = nx.get_node_attributes(self.tree, 'color')
        
        for n in neighbor_nodes:
            colors_of_neighbor_nodes.append(colors_of_all_nodes[n])

        return colors_of_neighbor_nodes

    def get_shot_dict_of_neighbors(self, node):
        '''This function returns a dict of shots of the neighbor nodes
        of a given node'''
        shots_of_neighbor_nodes = {}
        neighbor_nodes = list(self.tree.neighbors(node))
        shots_of_all_nodes = nx.get_node_attributes(self.tree, 'shot')
        
        for n in neighbor_nodes:
            shots_of_neighbor_nodes[n] = shots_of_all_nodes[n]

        return shots_of_neighbor_nodes

    def get_color_dict_of_neighbors(self, node):
        '''This function returns a dict of the colors of the neighbor
        nodes of a given node'''
        colors_of_neighbor_nodes = {}
        neighbor_nodes = list(self.tree.neighbors(node))
        color_of_all_nodes = nx.get_node_attributes(self.tree, 'color')
        
        for i in neighbor_nodes:
            colors_of_neighbor_nodes[i] = color_of_all_nodes[i]

        return colors_of_neighbor_nodes

    def show_tree(self):
        '''If this function is called, it will draw the created tree'''
        # This is the list of colors for all the nodes. Node Color is
        # Blue for Bottom Bot and Green for Top Bot and Red for State 0
        colors = list(nx.get_node_attributes(self.tree,'color').values())
        # pos = graphviz.Digraph(self.tree, prog="dot")
        # pos = nx.nx_pydot.pydot_layout(self.tree, prog="dot")
        # pos = nx.spring_layout(self.tree, k = 0.8)
        pos = graphviz_layout(self.tree, prog="dot")
        nx.draw(self.tree,
                pos,
                node_color = colors,
                node_size = 150,
                labels=nx.get_node_attributes(self.tree, 'shot'), 
                with_labels=True, 
                font_size=5,
                font_weight='normal')
        
        plt.show()