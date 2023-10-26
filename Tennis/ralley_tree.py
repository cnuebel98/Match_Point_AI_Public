import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import constants as const
import math
import numpy as np

class Ralley_Tree:
    '''In this class all the functions to generate the game tree are 
    defined'''
    def __init__(self):
        '''Initializing a tree as a NetworkX Graph'''
        self.tree = nx.DiGraph()
        self.node_index = 0
        self.tree.add_node(0, colour="red", 
                           type="init", 
                           shot="", 
                           depth=0,
                           n_visits=0,
                           n_wins=0,
                           uct_value=0)
        self.active_node = 0
        self.visited_nodes = [0]

    def add_new_edge(self, node_A, node_B, n_visits, uct_value, win_count):
        '''Adds a new edge between two given nodes'''
        self.tree.add_edge(node_A, node_B,
                           n_visits=n_visits,
                           uct_value=uct_value,
                           win_count=win_count)

    def add_new_node(self, index, colour, node_type, shot_string, depth,
                     n_visits, n_wins, uct_value):
        '''A new node is added to the tree, with an unique index, a type
        (action or state node), a shot encoding string and a depth'''
        self.tree.add_node(index,
                           colour=colour,
                           type=node_type,
                           shot=shot_string,
                           depth=depth,
                           n_visits=n_visits,
                           n_wins=n_wins,
                           uct_value=uct_value)

    def get_tree(self):
        '''Returns the current tree'''
        return self.tree

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
        '''Returns a list of the neighbor nodes of a given node'''
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
    
    def get_shots_of_neighbors(self, node_list):
        '''Return a list of shots of a given List of nodes'''
        neighbor_shots = []
        for x in range(0, len(node_list)):
            neighbor_shot = self.tree.nodes[node_list[x]]['shot']
            neighbor_shots.append(neighbor_shot)
        return neighbor_shots
    
    def get_colour_list_of_neighbors(self, node):
        '''This function returns a list of shots of the neighbor nodes
        of a given node'''
        colours_of_neighbor_nodes = []
        neighbor_nodes = list(self.tree.neighbors(node))
        colours_of_all_nodes = nx.get_node_attributes(self.tree, 'colour')
        
        for n in neighbor_nodes:
            colours_of_neighbor_nodes.append(colours_of_all_nodes[n])

        return colours_of_neighbor_nodes

    def get_shot_dict_of_neighbors(self, node):
        '''This function returns a dict of shots of the neighbor nodes
        of a given node'''
        shots_of_neighbor_nodes = {}
        neighbor_nodes = list(self.tree.neighbors(node))
        shots_of_all_nodes = nx.get_node_attributes(self.tree, 'shot')
        
        for n in neighbor_nodes:
            shots_of_neighbor_nodes[n] = shots_of_all_nodes[n]

        return shots_of_neighbor_nodes

    def get_colour_of_node(self, node):
        '''Returns the color of a given Node.'''
        color = self.tree.nodes[node]['colour']
        return color

    def get_colour_dict_of_neighbors(self, node):
        '''This function returns a dict of the colours of the neighbor
        nodes of a given node'''
        colours_of_neighbor_nodes = {}
        neighbor_nodes = list(self.tree.neighbors(node))
        colour_of_all_nodes = nx.get_node_attributes(self.tree, 'colour')
        
        for i in neighbor_nodes:
            colours_of_neighbor_nodes[i] = colour_of_all_nodes[i]

        return colours_of_neighbor_nodes

    def get_list_of_blue_neighbors(self, node):
        '''Returns the list of neighbors, where colour = "Blue", which 
        means that player is bottom player'''
        blue_neighbors = []
        neighbors = self.get_neighbors(node)

        for x in range(0, len(neighbors)):
            if self.tree.nodes[neighbors[x]]['colour'] == "blue":
                blue_neighbors.append(neighbors[x])

        return blue_neighbors
    
    def get_list_of_green_neighbors(self, node):
        '''Returns the list of neighbors, where color = "Green", which 
        means that player is top player'''
        green_neighbors = []
        neighbors = self.get_neighbors(node)

        for x in range(0, len(neighbors)):
            if self.tree.nodes[neighbors[x]]['colour'] == "green":
                green_neighbors.append(neighbors[x])

        return green_neighbors

    def add_node_visit(self, node):
        '''The given node is added to the visited_nodes list.'''
        self.visited_nodes.append(node)

    def clear_visited_nodes(self):
        '''The visited_nodes list is being cleard before each new 
        ralley'''
        self.visited_nodes.clear()
        self.visited_nodes.append(0)

    def get_visited_nodes(self):
        '''Returns the List of the visited nodes in a ralley'''
        return self.visited_nodes

    def update_edge_visit_counts(self):
        #print("Visited_nodes: " + str(self.visited_nodes))
        for x in range(0, len(self.visited_nodes)-1):
            self.tree[self.visited_nodes[x]][self.visited_nodes[x+1]][
                'n_visits'] += 1
            
    def update_node_visit_counts(self):
        '''Nodes attribute of the number of visits is updated'''
        for x in range(0, len(self.visited_nodes)):
            self.tree.nodes[self.visited_nodes[x]]['n_visits'] += 1

    def update_node_wins(self, last_char_of_last_shot, player_of_last_shot):
        '''Nodes attribute of the number of wins is updated'''
        # This if statement checks wether the bottom player made a point
        # or not  and if he did the win count on the visited edges is +1
        if (player_of_last_shot == "blue"
            and last_char_of_last_shot == const.ShotEncodings.WINNER
            or player_of_last_shot == "green"
            and last_char_of_last_shot != const.ShotEncodings.WINNER):
            #print("bottom player played a Winner or top player made an error")
            for x in range(0, len(self.visited_nodes)):
                self.tree.nodes[self.visited_nodes[x]]['n_wins'] += 1

    def update_edge_wins(self, last_char_of_last_shot, player_of_last_shot):
        '''Update win count on the visited edges'''
        # The edge wins are updated only for the bottom player
        
        # This if statement checks wether the bottom player made a point
        # or not  and if he did the win count on the visited edges is +1
        if (player_of_last_shot == "blue"
            and last_char_of_last_shot == const.ShotEncodings.WINNER
            or player_of_last_shot == "green"
            and last_char_of_last_shot != const.ShotEncodings.WINNER):
            #print("bottom player played a Winner or top player made an error")
            for x in range(0, len(self.visited_nodes)-1):
                self.tree[self.visited_nodes[x]][self.visited_nodes[x+1]][
                    'win_count'] += 1

    def update_uct_value(self):
        # the uct value is the value for the selection phase of the mcts
        # agent. The one with the largest UCT will be selected

        # UCT = (wi/si) + c * sqrt(ln(sp)/si)
        
        # (wi/si) ... exploitation term (gets larger, the better the 
        # node has performed)        
        # sqrt(ln(sp)/si) ... exploration term (gets larger, when the 
        # node is picked less and less for simulation)
        
        # c  ... exploration parameter, usually sprt(2)
        c = math.sqrt(2)
        
        for x in range(0, len(self.visited_nodes)):
            child_nodes = []
            child_nodes = self.get_neighbors(self.visited_nodes[x])

            # This UCT Values of the visited_nodes children is updated
            # for each visited node, if there is more then one, 
            # otherwise the update is covered already
            if len(child_nodes) > 1:
                #print("Child Nodes: " + str(child_nodes))
                for y in range(0, len(child_nodes)):
                    wi = self.tree.nodes[child_nodes[y]]['n_wins']
                    si = self.tree.nodes[child_nodes[y]]['n_visits']
                    sp = self.tree.nodes[self.visited_nodes[x]]['n_visits']
                    self.tree.nodes[child_nodes[y]][
                        'uct_value'] = (wi/si) + c*math.sqrt((np.log(sp))/si)
            
            # The UCT Value of the visited nodes are updated
            # wi ... current nodes number of simulations, that were won
            wi = self.tree.nodes[self.visited_nodes[x]]['n_wins']
            # si ... current nodes total number of simulations
            si = self.tree.nodes[self.visited_nodes[x]]['n_visits']
            # sp ... parent node's current number of simulations
            sp = self.tree.nodes[self.visited_nodes[x-1]]['n_visits']

            self.tree.nodes[self.visited_nodes[x]][
                'uct_value'] = (wi/si) + c*math.sqrt((np.log(sp))/si)
            
            #print("N_Wins child: " + str(wi))
            #print("N_visits child: " + str(si))
            #print("N_visits parent: " + str(sp))
            #print("UCT_value " + str((wi/si) + c*math.sqrt((np.log(sp))/si)))

    def get_uct_values(self, node_list):
        '''Return the UCT Values of a given List of nodes'''
        uct_values = []
        for x in range(0, len(node_list)):
            uct_value = self.tree.nodes[node_list[x]]['uct_value']
            uct_values.append(uct_value)

        return uct_values
    
    def get_uct_value(self, node):
        '''Returns the UCT Value of a given Node'''
        return self.tree.nodes[node]['uct_value']

    def get_n_nodes(self):
        '''Returns the number of nodes in the tree'''
        return self.tree.number_of_nodes()

    def show_tree(self):
        '''If this function is called, it will draw the created tree'''
        # This is the list of colours for all the nodes. Node Colour is
        # Blue for Bottom Bot and Green for Top Bot and Red for State 0
        colours = list(nx.get_node_attributes(self.tree,'colour').values())
        # pos = graphviz.Digraph(self.tree, prog="dot")
        # pos = nx.nx_pydot.pydot_layout(self.tree, prog="dot")
        # pos = nx.spring_layout(self.tree, k = 0.8)
        pos = graphviz_layout(self.tree, prog="dot")
        nx.draw(self.tree,
                pos,
                node_color = colours,
                node_size = 150,
                labels=nx.get_node_attributes(self.tree, 'uct_value'), 
                with_labels=True, 
                font_size=5,
                font_weight='normal')
        
        # edge_labels here are the node indices added together with "->"
        # edge_labels = dict([((n1, n2), f'{n1}->{n2}') for n1, n2 in self.tree.edges])
        
        # Edge_Labels are the number of visits
        edge_labels = dict([((n1, n2), d['n_visits'])
                            for n1, n2, d in self.tree.edges(data=True)])
        
        nx.draw_networkx_edge_labels(self.tree, 
                                     pos, 
                                     edge_labels=edge_labels, 
                                     font_size=5)

        # draw the tree
        plt.show()