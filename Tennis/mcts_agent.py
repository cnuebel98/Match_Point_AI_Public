import random
import simpler_stat_bot_djoko
import scoring

class MCTS_Agent:
    '''In this class, the MCTS Algorithm is used to find the next shot 
    in a ralley'''

    def __init__(self, name="", turn=False):
        self.name = name
        self.turn = turn
        self.active_mcts_node = 0
        self.leaf_node = 0
        self.shot = ""
        self.expansion_shot = ""
        self.expansion_path = [0]

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
        print("--------------------------------")
        print("Starting selection Phase!")
        self.selection_phase(current_ralley, score, current_tree)

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

        print("Adding MCTS Shot to ralley (not learned): " + str(self.shot))
        current_ralley.add_shot_to_ralley(self.shot)
        print("Ralley: " + str(current_ralley.get_ralley()))
        print("-------------------------------")


    def selection_phase(self, current_ralley, score, current_tree):
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
            
            print("Color of Active MCTS Node: " + 
                  str(color_of_mcts_active_node))
            
            # If the color is red, we are still at the root node
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
                    self.add_node_to_expansion_path(green_neighbors[i])
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
                        self.add_node_to_expansion_path(highest_uct_neighbor)
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
                    self.add_node_to_expansion_path(highest_uct_neighbor)
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
                    self.add_node_to_expansion_path(green_neighbors[i])
                else: print("No green neighbors to choose from, term?")

            # else: we do: get_mcts_active_node and set that one to leaf
            # node and we leave the while loop

            # Every time the While loop is left, we need to have set a
            # leaf node
            
            i += 1
            print("--------------------------")
        print("Path of Selection Phase: " + str(self.expansion_path))
        print("Starting Expansion Phase!")
        self.expansion_phase(current_ralley, score, current_tree)
        self.reset_active_mcts_node()
        self.reset_leaf_node()
        self.clear_expansion_path()

        #print(str(current_tree.get_uct_value(self.active_mcts_node)))

        # What is a leaf node in my game
        # n_neighbors with different directions = 3 (3 directions...)
        # check the shot encodings for 1 2 and 3, if there is a shot 
        # with each of those directions, we select the next,
        # if not, we expand from there
        # because Djokovic Bot also only looks at the last shots
        # direction to make a choice
    
    def expansion_phase(self, current_ralley, score, current_tree):
        # We take the leave node and check the direction, which is
        # not yet in the leaf nodes children, and that is expanded and
        # is the node we start the simulation form
        print("The Leaf Node from the Selection Phase is: " 
              + str(self.leaf_node))
        
        # Get neighbors of the leaf node
        children_of_leaf_node = current_tree.get_neighbors(self.leaf_node)
        
        # special case: we need to check if the leaf node was a first
        # serve fault and then expand a second serve from there
        shot_encoding = current_tree.get_shot_of_node(self.leaf_node)
        if any("," in s for s in shot_encoding):
            print("Leaf Node is 1st serve fault, need to expand 2nd serve")
            
            if children_of_leaf_node:
                shots_of_children = current_tree.get_shots_of_neighbors(
                    children_of_leaf_node)
                print("Leaf node is first serve fault with children")
                if (any("4" in s for s in shots_of_children) 
                    and any("5" in s for s in shots_of_children)):
                    print("4 and 5 were found in children of leaf node")
                    self.set_expansion_shot("6", score, False)
                elif (any("4" in s for s in shots_of_children)
                    and any("6" in s for s in shots_of_children)):
                    print("4 and 6 were found in children of leaf node")
                    self.set_expansion_shot("5", score, False)
                elif (any("5" in s for s in shots_of_children)
                    and any("6" in s for s in shots_of_children)):
                    print("5 and 6 were found in children of leaf node")
                    self.set_expansion_shot("4", score, False)
                elif (any("4" in s for s in shots_of_children)):
                    print("4 was found in a child")
                    i = random.randint(0, 99)
                    if i < 50:
                        self.set_expansion_shot("5", score, False)
                    else: self.set_expansion_shot("6", score, False)
                elif (any("5" in s for s in shots_of_children)):
                    print("5 was found in a child")
                    i = random.randint(0, 99)
                    if i < 50:
                        self.set_expansion_shot("4", score, False)
                    else: self.set_expansion_shot("6", score, False)
                elif (any("6" in s for s in shots_of_children)):
                    print("6 was found in a child")
                    i = random.randint(0, 99)
                    if i < 50:
                        self.set_expansion_shot("4", score, False)
                    else: self.set_expansion_shot("5", score, False)
            else:
                print("2nd Serve & No children of leaf node found.")
                i = random.randint(0, 99)
                if i < 33: 
                    self.set_expansion_shot("4", score, False)
                elif i < 66:
                    self.set_expansion_shot("5", score, False)
                else:
                    self.set_expansion_shot("6", score, False)

        # When the root is a leaf node, we expand a random direction
        elif self.leaf_node == 0:
            print("Adding a new first serve.")
            # When there are already first serves, we check to see which
            # ones were played already
            if children_of_leaf_node:
                shots_of_children = current_tree.get_shots_of_neighbors(
                    children_of_leaf_node)
                
                if (any("4" in s for s in shots_of_children) 
                    and any("5" in s for s in shots_of_children)):
                    print("4 and 5 were found in children of leaf node")
                    self.set_expansion_shot("6", score, True)
                elif (any("4" in s for s in shots_of_children)
                    and any("6" in s for s in shots_of_children)):
                    print("4 and 6 were found in children of leaf node")
                    self.set_expansion_shot("5", score, True)
                elif (any("5" in s for s in shots_of_children)
                    and any("6" in s for s in shots_of_children)):
                    print("5 and 6 were found in children of leaf node")
                    self.set_expansion_shot("4", score, True)
                elif (any("4" in s for s in shots_of_children)):
                    print("4 was found in a child")
                    i = random.randint(0, 99)
                    if i < 50:
                        self.set_expansion_shot("5", score, True)
                    else: self.set_expansion_shot("6", score, True)
                elif (any("5" in s for s in shots_of_children)):
                    print("5 was found in a child")
                    i = random.randint(0, 99)
                    if i < 50:
                        self.set_expansion_shot("4", score, True)
                    else: self.set_expansion_shot("6", score, True)
                elif (any("6" in s for s in shots_of_children)):
                    print("6 was found in a child")
                    i = random.randint(0, 99)
                    if i < 50:
                        self.set_expansion_shot("4", score, True)
                    else: self.set_expansion_shot("5", score, True)
            else:
                print("No children of leaf node found.")
                i = random.randint(0, 99)
                if i < 33: 
                    self.set_expansion_shot("4", score, True)
                elif i < 66:
                    self.set_expansion_shot("5", score, True)
                else:
                    self.set_expansion_shot("6", score, True)

        elif children_of_leaf_node:
            # When the leaf node already has children, we need to
            # check their directions and add a shot with a direction,
            # that is'nt in the tree yet
            shots_of_children = current_tree.get_shots_of_neighbors(
                children_of_leaf_node)
            
            if (any("1" in s for s in shots_of_children) 
                and any("2" in s for s in shots_of_children)):
                print("1 and 2 were found in children of leaf node")
                self.set_expansion_shot("3", score)
            elif (any("1" in s for s in shots_of_children)
                and any("3" in s for s in shots_of_children)):
                print("1 and 3 were found in children of leaf node")
                self.set_expansion_shot("2", score)
            elif (any("2" in s for s in shots_of_children)
                and any("3" in s for s in shots_of_children)):
                print("2 and 3 were found in children of leaf node")
                self.set_expansion_shot("1", score)
            elif (any("1" in s for s in shots_of_children)):
                print("1 was found in a child")
                i = random.randint(0, 99)
                if i < 50:
                    self.set_expansion_shot("2", score)
                else: self.set_expansion_shot("3", score)
            elif (any("2" in s for s in shots_of_children)):
                print("2 was found in a child")
                i = random.randint(0, 99)
                if i < 50:
                    self.set_expansion_shot("1", score)
                else: self.set_expansion_shot("3", score)
            elif (any("3" in s for s in shots_of_children)):
                print("3 was found in a child")
                i = random.randint(0, 99)
                if i < 50:
                    self.set_expansion_shot("1", score)
                else: self.set_expansion_shot("2", score)
            else:
                i = random.randint(0, 99)
                if i < 33: 
                    self.set_expansion_shot("1", score)
                elif i < 66:
                    self.set_expansion_shot("2", score)
                else:
                    self.set_expansion_shot("3", score)

        # ToDo: start Simulation Phase from that new node
    
    def simulation_phase(self, current_ralley, score, current_tree):
        # starting from that unexplored child node, simulation is done.
        # Djoko Bot and MCTS Simulation Strategy (e.g. Random,
        # MC-Evaluation, or others) take turns in adding a shot until
        # terminal state is reached
        
        # to call the add_shot function of the opponent, we need the
        # the current_ralley, score and current_tree
        #simpler_stat_bot_djoko.Simple_Stat_Bot_Djokovic.add_shot(
        #    current_ralley, score, current_tree)


        # while (active_simu_shot not terminal):
        # active_simu_shot = ""    
        # Firstly, we need to see if the expanded shot or the active 
        # simu_shot was terminal
        # if ("nwdx," or "*" in self.get_expansion_shot()):
        #   if it was terminal: backpropagation phase
        # 
        # elif (its mcts agents turn to take a shot):
        #   "4", "5", "6" add at random and the probabilites for
        #   error/winner
        # elif (its the opponents turn to take a shot):
        #   call add_shot function of top_bot

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

    def get_expansion_shot(self):
        '''Returns the expansion_shot.'''
        return self.expansion_shot
    
    def set_expansion_shot(self, shot, score, first_serve=True):
        '''Sets the value of the expansion_shot.'''
        # Adding the probabilites of errors and winners 
        # to the chosen action (One action can lead to differetn states)
        altered_shot = shot

        if (shot == "4" or shot == "5" or shot == "6" and first_serve == True):
            # If serving from deuce side
            if (score.get_point_count_per_game() % 2 == 0):
                print("Expanding first serve from the deuce side")
                if (shot == "4"):
                    i = random.randint(0, 9999)
                    if i < 3310:
                        altered_shot = altered_shot + str("nwdx,")
                    elif i < (3310 + 779):
                        altered_shot = altered_shot + str("*")
                elif (shot == "5"):
                    j = random.randint(0, 9999)
                    if j < 2548:
                        altered_shot = altered_shot + str("nwdx,")
                    elif j < (2548 + 14):
                        altered_shot = altered_shot + str("*")
                elif (shot == "6"):
                    k = random.randint(0, 9999)
                    if k < 3965:
                        altered_shot = altered_shot + str("nwdx,")
                    elif k < (3965 + 973):
                        altered_shot = altered_shot + str("*")
            # Else serving from ad side
            else: 
                print("Expanding first serve from the ad side")
                if (shot == "4"):
                    i = random.randint(0, 9999)
                    if i < 3896:
                        altered_shot = altered_shot + str("nwdx,")
                    elif i < (3896 + 664):
                        altered_shot = altered_shot + str("*")
                elif (shot == "5"):
                    j = random.randint(0, 9999)
                    if j < 2793:
                        altered_shot = altered_shot + str("nwdx,")
                    elif j < (2793 + 14):
                        altered_shot = altered_shot + str("*")
                elif (shot == "6"):
                    k = random.randint(0, 9999)
                    if k < 3527:
                        altered_shot = altered_shot + str("nwdx,")
                    elif k < (3527 + 897):
                        altered_shot = altered_shot + str("*")
        
        elif (shot == "4" or shot == "5" or shot == "6" 
              and first_serve == False):
            # Adding Winner & Error Probas to a second serve
            if (score.get_point_count_per_game() % 2 == 0):
                print("Expanding 2nd serve from the deuce side")
                if (shot == "4"):
                    i = random.randint(0, 9999)
                    if i < 1240:
                        altered_shot = altered_shot + str("nwdx,")
                    elif i < (1240 + 149):
                        altered_shot = altered_shot + str("*")
                elif (shot == "5"):
                    j = random.randint(0, 9999)
                    if j < 737:
                        altered_shot = altered_shot + str("nwdx,")
                    elif j < (737 + 2):
                        altered_shot = altered_shot + str("*")
                elif (shot == "6"):
                    k = random.randint(0, 9999)
                    if k < 1068:
                        altered_shot = altered_shot + str("nwdx,")
                    elif k < (1068 + 94):
                        altered_shot = altered_shot + str("*")
            else:
                print("Expanding 2nd serve from the ad side")
                if (shot == "4"):
                    i = random.randint(0, 9999)
                    if i < 840:
                        altered_shot = altered_shot + str("nwdx,")
                    elif i < (840 + 61):
                        altered_shot = altered_shot + str("*")
                elif (shot == "5"):
                    j = random.randint(0, 9999)
                    if j < 755:
                        altered_shot = altered_shot + str("nwdx,")
                    elif j < (755 + 4):
                        altered_shot = altered_shot + str("*")
                elif (shot == "6"):
                    k = random.randint(0, 9999)
                    if k < 1373:
                        altered_shot = altered_shot + str("nwdx,")
                    elif k < (1373 + 299):
                        altered_shot = altered_shot + str("*")

        elif (shot == "1" or shot == "2" or shot == "3"):
            print("ToDo: Adding probabilities for Winners/Errors for normal shots.")
            # we need to cover 4 cases here:
            print("First Serve? " + str(first_serve))
            print("Server: " + str(score.get_serving_player()))
            
            # MCTS Agent is serving 
            if (score.get_serving_player() == 1):
                
                # 1st was MCTS Agent serving 1st in the ralley?
                if ():
                    print("A ralley, where MCTS was serving a 1st.")
                
                # 2nd was MCTS Agent serving 2nd in the ralley?
                elif ():
                    print("A ralley, where MCTS was serving a 2nd.")
            
            # MCTS Agent is returing
            elif (score.get_serving_player() == 2):
                
                # 3rd was MCTS Agent returning 1st in the ralley?
                if ():
                    print("A ralley, where MCTS was returning a 1st.")
                
                # 4th was MCTS Agent returning 2nd in the ralley?
                elif ():
                    print("A ralley, where MCTS was returning a 2nd.")
        
        print("Altered Shot from Expansion Phase: " + str(altered_shot))
        #print("Path of Selection Phase: " + str(self.expansion_path))
        self.expansion_shot = altered_shot

    def reset_expansion_shot(self):
        '''Resets the expansion_shot.'''
        self.expansion_shot = 0

    def add_node_to_expansion_path(self, node):
        '''Adds Node to Expansion Path'''
        self.expansion_path.append(node)

    def clear_expansion_path(self):
        '''Clears all Nodes from Expansion Path'''
        self.expansion_path.clear()
        self.expansion_path = [0]