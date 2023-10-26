import random

class MCTS_Agent:
    '''In this class, the MCTS Algorithm is used to find the next shot 
    in a ralley'''

    def __init__(self, name="", turn=False):
        self.name = name
        self.turn = turn
        self.active_mcts_node = 0
        self.leaf_node = 0
        self.shot = ""

    def add_shot(self, current_ralley, score, current_tree):
        '''This function is calling the different phases of MCTS'''

        # Get the data to work with (current_tree, current_ralley,
        # score, and so on)
        #print("Ralley: " + str(current_ralley.get_ralley()))
        #print("Score: " + str(score.get_score()))
        #print("Number of Nodes: " + str(current_tree.get_n_nodes()))
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
        print("Starting selection Phase!")
        self.selection_phase(current_tree)

        if current_ralley.get_len_ralley() == 0:
            i = random.randint(0, 99)
            if i < 33:
                self.shot ="4"
            elif i < 66:
                self.shot = "5"
            else:
                self.shot = "6"
        elif current_ralley.get_len_ralley() > 0:
            j = random.randint(0, 99)
            if j < 33:
                self.shot ="f18"
            elif j < 66:
                self.shot = "f28"
            else:
                self.shot = "f38"
        
        print("Adding MCTS Shot to ralley: " + str(self.shot))
        current_ralley.add_shot_to_ralley(self.shot)
        print("Ralley: " + str(current_ralley.get_ralley()))
        print("-------------------------------")
        
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

        self.leaf_node = -1
        i = 0

        # we need to know if the next node to traverse to needs to be 
        # a green one or a blue one

        while self.leaf_node == -1 and i < 100:
            # The blue neighbors are the nodes, from which the next leaf
            # node could be chosen, when all 3 directions are in the
            # blue_neighbors at least once
            blue_neighbors = []
            blue_neighbors = current_tree.get_list_of_blue_neighbors(
                self.get_active_mcts_node())
            
            green_neighbors = []
            green_neighbors = current_tree.get_list_of_green_neighbors(
                self.get_active_mcts_node())
            
            # Check who is serving in the current_ralley

            # Each neighbors shot encoding is looked at
            blue_neighbor_shots = []
            blue_neighbor_shots = current_tree.get_shots_of_neighbors(
                blue_neighbors)
            
            print("Blue Neighbors from Active Node: " + str(blue_neighbors))
            print("Blue Neighbors Shot Encodings: " + str(blue_neighbor_shots))
            
            # Color of the MCTS Active node is saved
            color_of_mcts_active_node = current_tree.get_colour_of_node(
                self.get_active_mcts_node())
            
            # Booleans for finding directions of neighborshots are
            # initialized
            dir_1_found = False
            dir_2_found = False
            dir_3_found = False
            dir_4_found = False
            dir_5_found = False
            dir_6_found = False

            # Check if all three directions are in the child nodes
            if any("1" in s for s in blue_neighbor_shots):
                dir_1_found = True
                #print("1 was found in blue neighbors shots.")
            if any("2" in s for s in blue_neighbor_shots):
                dir_2_found = True
                #print("2 was found in blue neighbors shots.")
            if any("3" in s for s in blue_neighbor_shots):
                dir_3_found = True
                #print("3 was found in blue neighbors shots.")
            if any("4" in s for s in blue_neighbor_shots):
                dir_4_found = True
                #print("4 was found in blue neighbors shots.")
            if any("5" in s for s in blue_neighbor_shots):
                dir_5_found = True
                #print("5 was found in blue neighbors shots.")
            if any("6" in s for s in blue_neighbor_shots):
                dir_6_found = True
                #print("6 was found in blue neighbors shots.")
            
            print("Color of Active MCTS Node: " + str(color_of_mcts_active_node))
            
            # If the color is red, we are still at the root
            if (color_of_mcts_active_node == "red"):
                # If its the MCTS Agents turn to serve, maybe start with
                # a blue node else, start with a random green one
                
                # if root node has green children there is a 50% chance
                # that one of the green neighbors is traversed
                print("Color of active node is red")
                j = random.randint(0, 99)
                if (j < 50 and green_neighbors):
                    print("We pick random from green neighbor children")
                    i = random.randint(0, len(green_neighbors)-1)
                    self.set_active_mcts_node(green_neighbors[i])
                # If there are no green neighbors or in 50% of the cases 
                # we traverse to a blue node
                else:
                    # If all three directions are found, then we go the the 
                    # child with the highest UCT Value and go again from there
                    print("We do the UCT process with the blue children")
                    if (dir_1_found and dir_2_found and dir_3_found
                        or dir_4_found and dir_5_found and dir_6_found):
                        
                        uct_values = current_tree.get_uct_values(blue_neighbors)
                        print("UCT Values of blue neighbors: " + str(uct_values))

                        # Here the Blue neighbor with the highest UCT Value is 
                        # found and set to active
                        highest_uct_neighbor = 0
                        for x in range(0, len(blue_neighbors)):
                            if highest_uct_neighbor == 0:
                                highest_uct_neighbor = blue_neighbors[x]
                            elif (current_tree.get_uct_value(highest_uct_neighbor)
                                <= current_tree.get_uct_value(blue_neighbors[x])):
                                highest_uct_neighbor = blue_neighbors[x]
                        self.set_active_mcts_node(highest_uct_neighbor)
                        print("New MCTS Active node hast UCT = " + str(
                            current_tree.get_uct_value(highest_uct_neighbor)))
                    else:
                        print("Leaf Node was set at i = " + str(i))
                        self.leaf_node = self.get_active_mcts_node()

            # If the color is green, we need to check the blue neighbors
            # and either go to highest uct or set it as leaf
            elif (color_of_mcts_active_node == "green"):
                print("Color of active node is green")
                print("UCT process is done for the blue children")
                # If all three directions are found, then we go the the 
                # child with the highest UCT Value and go again from there
                if (dir_1_found and dir_2_found and dir_3_found
                    or dir_4_found and dir_5_found and dir_6_found):
                    
                    uct_values = current_tree.get_uct_values(blue_neighbors)
                    print("UCT Values of blue neighbors: " + str(uct_values))

                    # Here the Blue neighbor with the highest UCT Value is 
                    # found and set to active
                    highest_uct_neighbor = 0
                    for x in range(0, len(blue_neighbors)):
                        if highest_uct_neighbor == 0:
                            highest_uct_neighbor = blue_neighbors[x]
                        elif (current_tree.get_uct_value(highest_uct_neighbor)
                            <= current_tree.get_uct_value(blue_neighbors[x])):
                            highest_uct_neighbor = blue_neighbors[x]
                    self.set_active_mcts_node(highest_uct_neighbor)
                    print("New MCTS Active node hast UCT = " + str(
                        current_tree.get_uct_value(highest_uct_neighbor)))
                else:
                    print("Leaf Node was set at i = " + str(i))
                    self.leaf_node = self.get_active_mcts_node()
            
            # If the color is blue, we need to see if it has
            # green neighbors. If it does, just pick a green neighbor at
            # random, if not we should be at a terminal node
            elif (color_of_mcts_active_node == "blue"):
                print("Color of active node is blue")
                print("Green Neighbors from Active MCTS Node: " + 
                      str(green_neighbors))
                # One of the Green Neighbors is taken at random and set
                # to active
                if green_neighbors:
                    print("we have green neighbors and pick one at random.")
                    i = random.randint(0, len(green_neighbors)-1)
                    self.set_active_mcts_node(green_neighbors[i])
                else: print("No green neighbors to choose from, term?")

            # else: we do: get_mcts_active_node and set that one to leaf
            # node and we leave the while loop

            # Every time the While loop is left, we need to have set a
            # leaf node
            
            i += 1
        print("Starting Expansion Phase!")
        self.expansion_phase()
        self.reset_active_mcts_node()
        self.reset_leaf_node()

        #print(str(current_tree.get_uct_value(self.active_mcts_node)))

        # What is a leaf node in my game
        # n_neighbors with different directions = 3 (3 directions...)
        # check the shot encodings for 1 2 and 3, if there is a shot 
        # with each of those directions, we select the next,
        # if not, we expand from there
        # because Djokovic Bot also only looks at the last shots
        # direction to make a choice
    
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