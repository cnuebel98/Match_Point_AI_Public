import random
import ralley_tree

class MCTS_Agent:
    '''In this class, the MCTS Algorithm is used to find the next shot 
    in a ralley'''

    def __init__(self, name="", turn=False):
        self.name = name
        self.turn = turn
        self.active_mcts_node = 0
        self.leaf_node = 0

    def add_shot(self, current_ralley, score, current_tree):
        '''This function is calling the different phases of MCTS'''

        # Get the data to work with (current_tree, current_ralley,
        # score, and so on)
        #print("Ralley: " + str(current_ralley.get_ralley()))
        #print("Score: " + str(score.get_score()))
        print("Number of Nodes: " + str(current_tree.get_n_nodes()))
        print("Active Node: " + str(current_tree.get_active_node()))
        
        #print("Active Node: " + str(current_tree.get_active_node()))

        # 1. Tree selection phase with UCT Formular:
        
        # The one with the largest UCT will be selected
        # UCT = (wi/si) + c * sqrt(ln(sp)/si)
        
        # wi ... current nodes number of simulations, that were won
        # si ... current nodes total number of simulations
        # sp ... parent node's current number of simulations
        # c  ... exploration parameter, usually sprt(2)

        # (wi/si) ... exploitation term (gets larger, the better the 
        # node has performed)
        
        # sqrt(ln(sp)/si) ... exploration term (gets larger, when the 
        # node is picked less and less for simulation)
        
        # My plan: 
        # - gets the current tree and the active node in that tree

        # - here we start the selection phase: from that active node we 
        # look at the next possible actions. If there is any action, 
        # that has not yet been played, the selection phase is stopped 
        # and one or more of them is expanded 
        
        # - when its a serve, the Agent can choose the hit in directions 4, 5, 6
        # - when its in the ralley, the Agent can choose to hit in directions 1, 2, 3
        
        for _ in range(0, 10):
            # repeat the 4 phases x times
            # Selection phase:
            #selected_node = self.selection_phase(current_tree)
            ...
        self.selection_phase(current_tree)

        if current_ralley.get_len_ralley() == 0:
            i = random.randint(0, 99)
            if i < 33:
                shot ="4"
            elif i < 66:
                shot = "5"
            else:
                shot = "6"
        elif current_ralley.get_len_ralley() > 0:
            shot = "f18"

        current_ralley.add_shot_to_ralley(shot)

        # 2. Expansion phase


    def selection_phase(self, current_tree):
        '''In the selection Phase, we traverse through the current tree,
        always taking the child node with the highest UCT Value until a
        leaf node is reached'''
        
        
        # Then get the UCT Values of the neighboring nodes 
        # Then pick the neighbor with the highest uct value and go there
        # Do that until a leaf node is found
        # Get the list of neighbors from the root/active node

        # Blue_neighbors are only the neighbors nodes with color blue,
        # so the actions that have been taken by the MCTS Agent
        # from that node

        self.leaf_node = 0
        i = 0

        while self.leaf_node == 0 or i == 10:
            blue_neighbors = []
            blue_neighbors = current_tree.get_list_of_blue_neighbors(
                self.get_active_mcts_node())
            # print("Blue Neighbors from Active Node: " + str(blue_neighbors))

            # Idea:
            # if: blue_neighbors have shots in all directions, then we
            # set the highest UTC node to mcts_active_node 

            # else: we do: get_mcts_active_node and set that one to leaf
            # node and we leave the while loop

            # Every time the While loop is left, we need to have set a
            # leaf node

            if blue_neighbors:
                uct_values = current_tree.get_uct_values(blue_neighbors)
                print("UCT Values of blue neighbors: " + str(uct_values))

            # Here the Blue neighbor with the highest UCT Value is found
            highest_uct_neighbor = 0
            for x in range(0, len(blue_neighbors)):
                if highest_uct_neighbor == 0:
                    highest_uct_neighbor = blue_neighbors[x]
                elif (current_tree.get_uct_value(highest_uct_neighbor)
                    <= current_tree.get_uct_value(blue_neighbors[x])):
                    highest_uct_neighbor = blue_neighbors[x]

            #print("Highest UCT Value of any blue neighbor: " + 
            #    str(current_tree.get_uct_value(highest_uct_neighbor)))
            
            # The Blue neighbornode with the highest UTC Value is set to
            # active and then the loop is repeated
            self.set_active_mcts_node(highest_uct_neighbor)
            
            i += 1

        self.expansion_phase()
            

        #print(str(current_tree.get_uct_value(self.active_mcts_node)))

        # What is a leaf node in my game????
        # n_neighbors with different directions = 3 (3 directions...)
        # check the shot encodings for 1 2 and 3, if there is a shot 
        # with each of those directions, we select the next,
        # if not, we expand from there
        # because Djokovic Bot also only looks at the last shots
        # direction to make a choice

        # Exception for 1st & 2nd Serve, there we have the 3 other
        # direction for each serve
        #self.set_leaf_node()
        #return self.get_leaf_node()
        
    
    def expansion_phase(self):
        # We take the leave node and check the direction, which is
        # not yet in the leaf nodes children, and that is expanded and
        # is the node we start the simulation form
        print("The Leaf Node from the Selection Phase is: " 
              + str(self.leaf_node))
        
        # ToDo: check directions in the children of the leaf node
        # ToDo: choose a direction and add that as a new node/shot
        # ToDo: start Simulation Phase from that new node
    
    def simulation_phase(self):
        # starting from that unexplored child node, simulation is done.
        # Djoko Bot and MCTS Simulation Strategy (e.g. Random,
        # MC-Evaluation, or others) take turns in adding a shot until
        # terminal state is reached
        ...
    
    def backpropagation_phase(self):
        # Either only update the values between root node and unexplored
        # expanded child node, or all of the simulated stuff
        ...

    def get_active_mcts_node(self):
        '''Returns the node, that is active during the MCTS process.'''
        return self.active_mcts_node
    
    def set_active_mcts_node(self, node):
        '''Sets the value of the mcts-active node to a given Node.'''
        self.active_mcts_node = node

    def reset_active_mcts_node(self):
        '''Resets the node, that was active during the MCTS process.'''
        self.active_mcts_node = 0

    def get_leaf_node(self):
        '''Returns the node, that is active during the MCTS process.'''
        return self.leaf_node
    
    def set_leaf_node(self, node):
        '''Sets the value of the mcts-active node to a given Node.'''
        self.leaf_node = node

    def reset_leaf_node(self):
        '''Resets the node, that was active during the MCTS process.'''
        self.leaf_node = 0