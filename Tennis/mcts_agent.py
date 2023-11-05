import random
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import simpler_stat_bot_djoko as djoko
import ralley
import copy
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
        self.mcts_tree = nx.DiGraph()
        self.mcts_ralley = ralley.Ralley()
        self.opponent = djoko.Simple_Stat_Bot_Djokovic("Simple_Djoko")

    def add_shot(self, current_ralley, score, current_tree):
        '''This function is calling the different phases of MCTS'''

        # We save a deep copy of the current_tree from the actual game
        self.mcts_tree = nx.compose(self.mcts_tree, current_tree.get_tree())
        print(type(self.mcts_ralley))
        # We safe a copy of the current_ralley from the actual game
        self.copy_ralley_to_mcts_ralley(current_ralley)
        print(type(self.mcts_ralley))
        print("Initial Tree from the real game is displayed.")
        self.show_mcts_tree()

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
        print("-> Starting selection Phase!")
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
                self.shot = "f28*"
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
        print("Current_ralley in start of selection Phase: " + str(current_ralley.get_ralley()))

        # The root node is always the node in the tree which represents 
        # the last shot in the current Ralley

        print("-> Setting the root node according to current ralley.")
        if (current_ralley.get_len_ralley() == 0):
            # If there is no shot in the ralley, root node is 0
            self.set_active_mcts_node(0)
            print("Root Node is: " + str(self.get_active_mcts_node()) + " , should be 0.")
        else:
            # We have to find the ralley in the current tree and go to 
            # last node/last shot of ralley and find the index of that
            # node and set it to root node
            serving = score.get_serving_player()
            ralley = current_ralley.get_ralley()
            index = 0
            # from the Red Node, there can be 2x "6" encoding, we have 
            # to look at the current_ralley, to see who is serving to 
            # take the right "6"
            if (serving == 1):
                neighbors = current_tree.get_list_of_blue_neighbors(index)
            elif (serving == 2):
                neighbors = current_tree.get_list_of_green_neighbors(index)
            
            # We look at each shot in the ralley and find the enconding 
            # in the tree
            for i in range(0, len(ralley)):
                ralley_shot = ""
                ralley_shot = ralley[i]

                neighbor_shots = current_tree.get_shots_of_neighbors(neighbors)
                neighbors_index = neighbor_shots.index(ralley_shot)
                index = neighbors[neighbors_index]
                self.expansion_path.append(index)
                neighbors = current_tree.get_neighbors(index)
                        
            # the index in the end is the node, which represetns the
            # last shot in the ralley
            self.set_active_mcts_node(index)     

            
            self.mcts_tree.nodes[self.active_mcts_node]['colour'] = 'red'
            
            print("Root Node is " 
                  + str(self.get_active_mcts_node()) 
                  + " with shot encondging: " 
                  + str(current_tree.get_shot_of_node(self.
                                                      get_active_mcts_node())))
        
        print("MCTS_tree with new root node is displayed.")
        self.show_mcts_tree()
        # Now that we have the root node we can look for the leaf node 
        # from there
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
            
            green_neighbor_shots = []
            green_neighbor_shots = current_tree.get_shots_of_neighbors(
                green_neighbors)

            # Check who is serving in the current_ralley

            # Each neighbors shot encoding is looked at
            blue_neighbor_shots = []
            blue_neighbor_shots = current_tree.get_shots_of_neighbors(
                blue_neighbors)
            
            print("Blue Neighbors from Active Node: " + str(blue_neighbors))
            print("Blue Neighbors Shot Encodings: " + str(blue_neighbor_shots))
            
            print("Green Neighbors from active Node: " + str(green_neighbors))
            print("Green Neighbor Shots from acitve Node" + str(green_neighbor_shots))

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
                j = random.randint(0, 99)
                if (j < 50 and green_neighbors):
                    print("We pick random from green neighbor children")
                    
                    i = random.randint(0, len(green_neighbors)-1)
                    print("The picked green Node is: " + str(green_neighbors[i]))
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
                # If active green node is first serve fault we check his 
                # neighbors and either pick one at random (He should 
                # always have at least 1 neighbor)
                shot_encoding_active = current_tree.get_shot_of_node(
                    self.active_mcts_node)
                if (any("," in s for s in shot_encoding_active)):
                    print("The current active MCTS Node is a first serve fault of green: " + str(shot_encoding_active))
                    # When this is the case, we go to one of the second serves at random
                    i = random.randint(0, len(green_neighbors)-1)
                    print("The picked second serve is: " + str(green_neighbors[i]))
                    self.set_active_mcts_node(green_neighbors[i])
                    self.add_node_to_expansion_path(green_neighbors[i])

                # If all three directions are found, then we go the the 
                # child with the highest UCT Value and go again from there
                elif (dir_1_found and dir_2_found and dir_3_found
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
                    print("New MCTS Active node has UCT = " + str(
                        current_tree.get_uct_value(highest_uct_neighbor)))
                else:
                    print("Leaf Node was set at i = " + str(i))
                    self.leaf_node = self.get_active_mcts_node()
            
            # If the color is blue, we need to see if it has
            # green neighbors. If it does, just pick a green neighbor at
            # random, if not we should be at a terminal node
            elif (color_of_mcts_active_node == "blue"):
                print("Green Neighbors from Active MCTS Node: " + 
                      str(green_neighbors))
                # One of the Green Neighbors is taken at random and set
                # to active
                if green_neighbors:
                    print("There are green neighbors and we pick one at random.")
                    print("ToDo: make sure that no terminal nodes are picked")
                    i = random.randint(0, len(green_neighbors)-1)
                    print("Green neighbor that was picked: " + str(green_neighbors[i]))
                    self.set_active_mcts_node(green_neighbors[i])
                    self.add_node_to_expansion_path(green_neighbors[i])
                else: print("No green neighbors to choose from, term?")

            # else: we do: get_mcts_active_node and set that one to leaf
            # node and we leave the while loop

            # Every time the While loop is left, we need to have set a
            # leaf node
            
            i += 1
            print("--------------------------")
        #print("Path of Selection Phase: " + str(self.expansion_path))
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
        print("Leaf Node Shot encoding: " + str(current_tree.get_shot_of_node(self.leaf_node)))
        
        self.mcts_tree.nodes[self.leaf_node]['colour'] = 'orange'
        print("Displaying the MCTS_Tree with orange Leaf Node.")
        self.show_mcts_tree()

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
                    self.set_expansion_shot("6", score, current_tree, False)
                elif (any("4" in s for s in shots_of_children)
                    and any("6" in s for s in shots_of_children)):
                    print("4 and 6 were found in children of leaf node")
                    self.set_expansion_shot("5", score, current_tree, False)
                elif (any("5" in s for s in shots_of_children)
                    and any("6" in s for s in shots_of_children)):
                    print("5 and 6 were found in children of leaf node")
                    self.set_expansion_shot("4", score, current_tree, False)
                elif (any("4" in s for s in shots_of_children)):
                    print("4 was found in a child")
                    i = random.randint(0, 99)
                    if i < 50:
                        self.set_expansion_shot("5", score, current_tree, False)
                    else: self.set_expansion_shot("6", score, current_tree, False)
                elif (any("5" in s for s in shots_of_children)):
                    print("5 was found in a child")
                    i = random.randint(0, 99)
                    if i < 50:
                        self.set_expansion_shot("4", score, current_tree, False)
                    else: self.set_expansion_shot("6", score, current_tree, False)
                elif (any("6" in s for s in shots_of_children)):
                    print("6 was found in a child")
                    i = random.randint(0, 99)
                    if i < 50:
                        self.set_expansion_shot("4", score, current_tree, False)
                    else: self.set_expansion_shot("5", score, current_tree, False)
            else:
                print("2nd Serve & No children of leaf node found.")
                i = random.randint(0, 99)
                if i < 33: 
                    self.set_expansion_shot("4", score, current_tree, False)
                elif i < 66:
                    self.set_expansion_shot("5", score, current_tree, False)
                else:
                    self.set_expansion_shot("6", score, current_tree, False)

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
                    self.set_expansion_shot("6", score, current_tree)
                elif (any("4" in s for s in shots_of_children)
                    and any("6" in s for s in shots_of_children)):
                    print("4 and 6 were found in children of leaf node")
                    self.set_expansion_shot("5", score, current_tree)
                elif (any("5" in s for s in shots_of_children)
                    and any("6" in s for s in shots_of_children)):
                    print("5 and 6 were found in children of leaf node")
                    self.set_expansion_shot("4", score, current_tree)
                elif (any("4" in s for s in shots_of_children)):
                    print("4 was found in a child")
                    i = random.randint(0, 99)
                    if i < 50:
                        self.set_expansion_shot("5", score, current_tree)
                    else: self.set_expansion_shot("6", score, current_tree)
                elif (any("5" in s for s in shots_of_children)):
                    print("5 was found in a child")
                    i = random.randint(0, 99)
                    if i < 50:
                        self.set_expansion_shot("4", score, current_tree)
                    else: self.set_expansion_shot("6", score, current_tree)
                elif (any("6" in s for s in shots_of_children)):
                    print("6 was found in a child")
                    i = random.randint(0, 99)
                    if i < 50:
                        self.set_expansion_shot("4", score, current_tree)
                    else: self.set_expansion_shot("5", score, current_tree)
            else:
                print("No children of leaf node found.")
                i = random.randint(0, 99)
                if i < 33: 
                    self.set_expansion_shot("4", score, current_tree)
                elif i < 66:
                    self.set_expansion_shot("5", score, current_tree)
                else:
                    self.set_expansion_shot("6", score, current_tree)

        elif children_of_leaf_node:
            # When the leaf node already has children, we need to
            # check their directions and add a shot with a direction,
            # that is'nt in the tree yet
            shots_of_children = current_tree.get_shots_of_neighbors(
                children_of_leaf_node)
            
            if (any("1" in s for s in shots_of_children) 
                and any("2" in s for s in shots_of_children)):
                print("1 and 2 were found in children of leaf node")
                self.set_expansion_shot("3", score, current_tree)
            elif (any("1" in s for s in shots_of_children)
                and any("3" in s for s in shots_of_children)):
                print("1 and 3 were found in children of leaf node")
                self.set_expansion_shot("2", score, current_tree)
            elif (any("2" in s for s in shots_of_children)
                and any("3" in s for s in shots_of_children)):
                print("2 and 3 were found in children of leaf node")
                self.set_expansion_shot("1", score, current_tree)
            elif (any("1" in s for s in shots_of_children)):
                print("1 was found in a child")
                i = random.randint(0, 99)
                if i < 50:
                    self.set_expansion_shot("2", score, current_tree)
                else: self.set_expansion_shot("3", score, current_tree)
            elif (any("2" in s for s in shots_of_children)):
                print("2 was found in a child")
                i = random.randint(0, 99)
                if i < 50:
                    self.set_expansion_shot("1", score, current_tree)
                else: self.set_expansion_shot("3", score, current_tree)
            elif (any("3" in s for s in shots_of_children)):
                print("3 was found in a child")
                i = random.randint(0, 99)
                if i < 50:
                    self.set_expansion_shot("1", score, current_tree)
                else: self.set_expansion_shot("2", score, current_tree)
            else:
                i = random.randint(0, 99)
                if i < 33: 
                    self.set_expansion_shot("1", score, current_tree)
                elif i < 66:
                    self.set_expansion_shot("2", score, current_tree)
                else:
                    self.set_expansion_shot("3", score, current_tree)

        else: 
            #print("ToDo: No children of leaf node found, expanding a random direction")
            i = random.randint(0, 99)
            if i < 33: 
                self.set_expansion_shot("1", score, current_tree)
            elif i < 66:
                self.set_expansion_shot("2", score, current_tree)
            else:
                self.set_expansion_shot("3", score, current_tree)

        # Now we should have a shot encoding for the expansion and we
        # add it to the mcts tree.
        
        exp_shot = self.get_expansion_shot()
        exp_shot_index = current_tree.get_next_node_index()
        exp_shot_depth = current_ralley.get_len_ralley() + 1
        
        # Here we add the expansion shot to the leaf node of the tree
        self.add_node_to_mcts_tree(exp_shot_index, colour="yellow", 
                                   node_type="Expansion", shot_string=exp_shot,
                                   depth=exp_shot_depth, n_visits=0, n_wins=0, 
                                   uct_value=0)
        
        exp_shot_dir = self.get_dir_of_shot_in_mcts_tree(exp_shot_index)

        self.add_edge_to_mcts_tree(node_A=self.get_leaf_node(), 
                                   node_B=exp_shot_index, 
                                   n_visits=0, uct_value=0,
                                   win_count=0, direction=exp_shot_dir)


        self.add_shot_to_mcts_ralley(self.get_expansion_shot())
        print("Displaying MCTS Tree with yellow expansion Shot.")
        self.show_mcts_tree()

        print("-----------------------------")
        print("Starting Simulation Phase!")
        self.simulation_phase(current_ralley, score, current_tree)


        # ToDo: start Simulation Phase from that new node
    
    def simulation_phase(self, current_ralley, score, current_tree):
        # starting from the expansion node, simulation is done.
        # Djoko Bot and MCTS Simulation Strategy (e.g. Random,
        # MC-Evaluation, or others) take turns in adding a shot until
        # terminal state is reached

        # We start with the expansion shot.

        # first we check if the Expansion Shot is terminal or not or
        # wether its a first serve fault.
        
        x = self.shot_terminated(self.expansion_shot)
        if (x == "in_play"):
            print("The expanded shot is in play.")
            # The Expansion shot is always a Shot of the MCTS agent, so we 
            # need to add a shot of the opponent first
            print("the problem mcts ralley: " + str(self.mcts_ralley))
            

            bot_shot = self.opponent.add_shot(
                current_ralley=self.mcts_ralley,
                score=score,
                current_tree=current_tree,
                simulation_phase=True)
            
            print("The simulated shot of Djoko: " + str(bot_shot))


        elif (x == "terminal"):
            print("The expanded shot is terminal.")
            print("ToDo: start backpropagation from here")

        elif (x == "second_serve"):
            print("The expanded serve is a first serve fault.")



        
        # to call the add_shot function of the opponent, we need the
        # the current_ralley, score and current_tree
        


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

    def shot_terminated(self, shot):
        '''Checks wether a given shot encoding is a terminal shot or 
        not, or if it's a first serve fault.'''
        x = "in_play"
        
        if ('nwdx,' in shot):
            x = "second_serve"
        elif ('nwdx' in shot or '*' in shot):
            x = 'terminal'
        return x

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
    
    def set_expansion_shot(self, shot, score, current_tree, first_serve=True):
        '''Sets the value of the expansion_shot. Called during the 
        Expansion Phase to alter the shot direction with the 
        corresponding probabilities'''
        # Adding the probabilites of errors and winners 
        # to the chosen action (One action can lead to different states)
        #shot = shot
        
        if (shot == "4" or shot == "5" or shot == "6" and first_serve == True):
            # If serving from deuce side
            if (score.get_point_count_per_game() % 2 == 0):
                print("Expanding first serve from the deuce side")
                if (shot == "4"):
                    i = random.randint(0, 9999)
                    if i < 3310:
                        shot = shot + str("nwdx,")
                    elif i < (3310 + 779):
                        shot = shot + str("*")
                elif (shot == "5"):
                    j = random.randint(0, 9999)
                    if j < 2548:
                        shot = shot + str("nwdx,")
                    elif j < (2548 + 14):
                        shot = shot + str("*")
                elif (shot == "6"):
                    k = random.randint(0, 9999)
                    if k < 3965:
                        shot = shot + str("nwdx,")
                    elif k < (3965 + 973):
                        shot = shot + str("*")
            # Else serving from ad side
            else: 
                print("Expanding first serve from the ad side")
                if (shot == "4"):
                    i = random.randint(0, 9999)
                    if i < 3896:
                        shot = shot + str("nwdx,")
                    elif i < (3896 + 664):
                        shot = shot + str("*")
                elif (shot == "5"):
                    j = random.randint(0, 9999)
                    if j < 2793:
                        shot = shot + str("nwdx,")
                    elif j < (2793 + 14):
                        shot = shot + str("*")
                elif (shot == "6"):
                    k = random.randint(0, 9999)
                    if k < 3527:
                        shot = shot + str("nwdx,")
                    elif k < (3527 + 897):
                        shot = shot + str("*")
        
        elif (shot == "4" or shot == "5" or shot == "6" 
              and first_serve == False):
            # Adding Winner & Error Probas to a second serve
            if (score.get_point_count_per_game() % 2 == 0):
                print("Expanding 2nd serve from the deuce side")
                if (shot == "4"):
                    i = random.randint(0, 9999)
                    if i < 1240:
                        shot = shot + str("nwdx")
                    elif i < (1240 + 149):
                        shot = shot + str("*")
                elif (shot == "5"):
                    j = random.randint(0, 9999)
                    if j < 737:
                        shot = shot + str("nwdx")
                    elif j < (737 + 2):
                        shot = shot + str("*")
                elif (shot == "6"):
                    k = random.randint(0, 9999)
                    if k < 1068:
                        shot = shot + str("nwdx")
                    elif k < (1068 + 94):
                        shot = shot + str("*")
            else:
                print("Expanding 2nd serve from the ad side")
                if (shot == "4"):
                    i = random.randint(0, 9999)
                    if i < 840:
                        shot = shot + str("nwdx")
                    elif i < (840 + 61):
                        shot = shot + str("*")
                elif (shot == "5"):
                    j = random.randint(0, 9999)
                    if j < 755:
                        shot = shot + str("nwdx")
                    elif j < (755 + 4):
                        shot = shot + str("*")
                elif (shot == "6"):
                    k = random.randint(0, 9999)
                    if k < 1373:
                        shot = shot + str("nwdx")
                    elif k < (1373 + 299):
                        shot = shot + str("*")

        elif (shot == "1" or shot == "2" or shot == "3"):
            
            print("Serving (1 for bottom, 2 for top): " + str(score.get_serving_player()))
            print("Path till expanded shot: " + str(self.expansion_path))
            print("Shot of first serve in selected Ralley: " + str(current_tree.get_shot_of_node(self.expansion_path[1])))
            print("Shot of Parent Node (Leaf Node): " + str(current_tree.get_shot_of_node(self.leaf_node)))
            
            # Are we expanding a return?
            if (current_tree.get_shot_of_node(self.leaf_node) == "4" 
                or current_tree.get_shot_of_node(self.leaf_node) == "5" 
                or current_tree.get_shot_of_node(self.leaf_node) == "6"):
                print("We are expanding a return.")
                # How to figure out if its a first or second serve??
                # Look at depth of leaf node. If it is 1 then it was a 
                # first serve and if its two it was a second serve

                if (current_tree.get_depth(self.leaf_node) == 1):
                    print("Depth of leaf Node: 1, so we add the return Probas for return on first serve")
                    # Depending on the direction of the first serve, we 
                    # take different Probabilities for the return
                    if (current_tree.get_shot_of_node(self.leaf_node) == "4"):
                        if (shot == "1"):
                            i = random.randint(0, 9999)
                            if i < 2737:
                                shot = shot + "7"
                            elif (i < 2737 + 4565):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 3005:
                                shot = shot + "nwdx"
                            elif (j < 3005 + 390):
                                shot = shot + "*"
                            
                        elif (shot == "2"):
                            i = random.randint(0, 9999)
                            if i < 2137:
                                shot = shot + "7"
                            elif (i < 4406 + 4406):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 1942:
                                shot = shot + "nwdx"
                            elif (j < 1942 + 21):
                                shot = shot + "*"
                        else:
                            i = random.randint(0, 9999)
                            if i < 3165:
                                shot = shot + "7"
                            elif (i < 3165 + 4354):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 2574:
                                shot = shot + "nwdx"
                            elif (j < 2574 + 147):
                                shot = shot + "*"

                    elif(current_tree.get_shot_of_node(self.leaf_node) == "5"):
                        if (shot == "1"):
                            i = random.randint(0, 9999)
                            if i < 2682:
                                shot = shot + "7"
                            elif (i < 2682 + 4506):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 2604:
                                shot = shot + "nwdx"
                            elif (j < 2604 + 317):
                                shot = shot + "*"

                        elif (shot == "2"):
                            i = random.randint(0, 9999)
                            if i < 2222:
                                shot = shot + "7"
                            elif (i < 2222 + 4521):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 1443:
                                shot = shot + "nwdx"
                            elif (j < 1443 + 14):
                                shot = shot + "*"

                        else:
                            i = random.randint(0, 9999)
                            if i < 2770:
                                shot = shot + "7"
                            elif (i < 2770 + 4693):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 2230:
                                shot = shot + "nwdx"
                            elif (j < 2230 + 95):
                                shot = shot + "*"

                    else:
                        if (shot == "1"):
                            i = random.randint(0, 9999)
                            if i < 3042:
                                shot = shot + "7"
                            elif (i < 3042 + 4132):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 3089:
                                shot = shot + "nwdx"
                            elif (j < 3089 + 238):
                                shot = shot + "*"

                        elif (shot == "2"):
                            i = random.randint(0, 9999)
                            if i < 2724:
                                shot = shot + "7"
                            elif (i < 2724 + 4427):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 1675:
                                shot = shot + "nwdx"
                            elif (j < 1675 + 10):
                                shot = shot + "*"

                        else:
                            i = random.randint(0, 9999)
                            if i < 3158:
                                shot = shot + "7"
                            elif (i < 3158 + 4320):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 2507:
                                shot = shot + "nwdx"
                            elif (j < 2507 + 46):
                                shot = shot + "*"

                elif (current_tree.get_depth(self.leaf_node) == 2):
                    print("Depth of leaf Node: 2, so we add the return Probas for return on second serve")

                    if (current_tree.get_shot_of_node(self.leaf_node) == "4"):
                        if (shot == "1"):
                            i = random.randint(0, 9999)
                            if i < 2237:
                                shot = shot + "7"
                            elif (i < 2237 + 4899):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 2641:
                                shot = shot + "nwdx"
                            elif (j < 2641 + 899):
                                shot = shot + "*"
                            
                        elif (shot == "2"):
                            i = random.randint(0, 9999)
                            if i < 1519:
                                shot = shot + "7"
                            elif (i < 1519 + 4903):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 1510:
                                shot = shot + "nwdx"
                            elif (j < 1510 + 21):
                                shot = shot + "*"

                        else:
                            i = random.randint(0, 9999)
                            if i < 2601:
                                shot = shot + "7"
                            elif (i < 2601 + 5046):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 1513:
                                shot = shot + "nwdx"
                            elif (j < 1513 + 195):
                                shot = shot + "*"

                    elif(current_tree.get_shot_of_node(self.leaf_node) == "5"):
                        if (shot == "1"):
                            i = random.randint(0, 9999)
                            if i < 2107:
                                shot = shot + "7"
                            elif (i < 2107 + 5037):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 2223:
                                shot = shot + "nwdx"
                            elif (j < 2223 + 744):
                                shot = shot + "*"

                        elif (shot == "2"):
                            i = random.randint(0, 9999)
                            if i < 1823:
                                shot = shot + "7"
                            elif (i < 1823 + 4877):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 1114:
                                shot = shot + "nwdx"
                            elif (j < 1114 + 16):
                                shot = shot + "*"

                        else:
                            i = random.randint(0, 9999)
                            if i < 2452:
                                shot = shot + "7"
                            elif (i < 2452 + 5109):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 1481:
                                shot = shot + "nwdx"
                            elif (j < 1481 + 232):
                                shot = shot + "*"

                    else:
                        if (shot == "1"):
                            i = random.randint(0, 9999)
                            if i < 2077:
                                shot = shot + "7"
                            elif (i < 2077 + 5096):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 2316:
                                shot = shot + "nwdx"
                            elif (j < 2316 + 787):
                                shot = shot + "*"

                        elif (shot == "2"):
                            i = random.randint(0, 9999)
                            if i < 2037:
                                shot = shot + "7"
                            elif (i < 2037 + 4912):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 1164:
                                shot = shot + "nwdx"
                            elif (j < 1164 + 14):
                                shot = shot + "*"

                        else:
                            i = random.randint(0, 9999)
                            if i < 2277:
                                shot = shot + "7"
                            elif (i < 2277 + 5185):
                                shot = shot + "8"
                            else:
                                shot = shot + "9" 

                            j = random.randint(0, 9999)
                            if j < 1685:
                                shot = shot + "nwdx"
                            elif (j < 1685 + 219):
                                shot = shot + "*"

            # We are not expanding a return
            else:
                print("We are expanding a normal shot.")
                if (score.get_serving_player() == 1):

                    # 1st was MCTS Agent serving 2nd in the ralley?
                    if (any("," in s for s in current_tree.get_shot_of_node(
                        self.expansion_path[1]))):
                        print("In a ralley, where MCTS was serving a 2nd.")
                        if (any("1" in s for s in current_tree.
                                get_shot_of_node(self.leaf_node))):
                            print("Opponents shot was in direction 1.")
                            if (shot == "1"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 2395:
                                    shot = shot + "7"
                                elif (i < 2395 + 4580):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"

                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1509:
                                    shot = shot + "nwdx"
                                elif j < (1509 + 577):
                                    shot = shot + "*"

                            elif (shot == "2"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1728:
                                    shot = shot + "7"
                                elif (i < 1728 + 4390):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1411:
                                    shot = shot + "nwdx"
                                elif j < (1411 + 114):
                                    shot = shot + "*"
                            else: 
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1449:
                                    shot = shot + "7"
                                elif (i < 1449 + 4448):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 2271:
                                    shot = shot + "nwdx"
                                elif j < (2271 + 1025):
                                    shot = shot + "*"

                        elif (any("2" in s for s in current_tree.
                                  get_shot_of_node(self.leaf_node))):
                            print("2 fount in Leaf Node")
                            if (shot == "1"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1734:
                                    shot = shot + "7"
                                elif (i < 1734 + 4789):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1500:
                                    shot = shot + "nwdx"
                                elif j < (1500 + 1126):
                                    shot = shot + "*"

                            elif (shot == "2"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1487:
                                    shot = shot + "7"
                                elif (i < 1487 + 4702):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1046:
                                    shot = shot + "nwdx"
                                elif j < (1046 + 102):
                                    shot = shot + "*"
                            else: 
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1570:
                                    shot = shot + "7"
                                elif (i < 1570 + 5010):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1334:
                                    shot = shot + "nwdx"
                                elif j < (1334 + 733):
                                    shot = shot + "*"
                        else: 
                            print("3 found in Leaf Node.")
                            if (shot == "1"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1478:
                                    shot = shot + "7"
                                elif (i < 1478 + 4324):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 2399:
                                    shot = shot + "nwdx"
                                elif j < (2399 + 1451):
                                    shot = shot + "*"

                            elif (shot == "2"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1332:
                                    shot = shot + "7"
                                elif (i < 1332 + 4481):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1233:
                                    shot = shot + "nwdx"
                                elif j < (1233 + 74):
                                    shot = shot + "*"
                            else: 
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1830:
                                    shot = shot + "7"
                                elif (i < 1830 + 4784):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1167:
                                    shot = shot + "nwdx"
                                elif j < (1167 + 317):
                                    shot = shot + "*"

                    # Was MCTS Agent serving 1st in the ralley?
                    else:
                        print("In a ralley, where MCTS was serving a 1st.")
                        if (any("1" in s for s in current_tree.
                                get_shot_of_node(self.leaf_node))):
                            print("1 found in Leaf Node")
                            if (shot == "1"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 2697:
                                    shot = shot + "7"
                                elif (i < 2697 + 4507):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1425:
                                    shot = shot + "nwdx"
                                elif j < (1425 + 1094):
                                    shot = shot + "*"

                            elif (shot == "2"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1882:
                                    shot = shot + "7"
                                elif (i < 1882 + 4457):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1323:
                                    shot = shot + "nwdx"
                                elif j < (1323 + 233):
                                    shot = shot + "*"
                            else: 
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1616:
                                    shot = shot + "7"
                                elif (i < 1616 + 4478):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1979:
                                    shot = shot + "nwdx"
                                elif j < (1979 + 1501):
                                    shot = shot + "*"

                        elif (any("2" in s for s in current_tree.
                                  get_shot_of_node(self.leaf_node))):
                            print("2 fount in Leaf Node")
                            if (shot == "1"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1834:
                                    shot = shot + "7"
                                elif (i < 1834 + 4817):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1263:
                                    shot = shot + "nwdx"
                                elif j < (1263 + 1758):
                                    shot = shot + "*"

                            elif (shot == "2"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1604:
                                    shot = shot + "7"
                                elif (i < 1604 + 4689):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 975:
                                    shot = shot + "nwdx"
                                elif j < (975 + 291):
                                    shot = shot + "*"
                            else: 
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1701:
                                    shot = shot + "7"
                                elif (i < 1701 + 4970):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1229:
                                    shot = shot + "nwdx"
                                elif j < (1229 + 1320):
                                    shot = shot + "*"
                        else: 
                            print("3 found in Leaf Node.")
                            if (shot == "1"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1705:
                                    shot = shot + "7"
                                elif (i < 1705 + 4102):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 2043:
                                    shot = shot + "nwdx"
                                elif j < (2043 + 1985):
                                    shot = shot + "*"

                            elif (shot == "2"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1440:
                                    shot = shot + "7"
                                elif (i < 1440 + 4439):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1175:
                                    shot = shot + "nwdx"
                                elif j < (1175 + 217):
                                    shot = shot + "*"

                            else: 
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 2046:
                                    shot = shot + "7"
                                elif (i < 2046 + 4818):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1114:
                                    shot = shot + "nwdx"
                                elif j < (1114 + 660):
                                    shot = shot + "*"

                # MCTS Agent is returing
                elif (score.get_serving_player() == 2):
                    
                    # 3rd was MCTS Agent returning 2nd in the ralley?
                    if (any("," in s for s in current_tree.get_shot_of_node(
                        self.expansion_path[1]))):
                        print("In a ralley, where MCTS was returning a 2nd.")
                        if (any("1" in s for s in current_tree.
                                get_shot_of_node(self.leaf_node))):
                            print("1 found in Leaf Node")
                            if (shot == "1"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 2347:
                                    shot = shot + "7"
                                elif (i < 2347 + 4746):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1516:
                                    shot = shot + "nwdx"
                                elif j < (1516 + 506):
                                    shot = shot + "*"

                            elif (shot == "2"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1856:
                                    shot = shot + "7"
                                elif (i < 1856 + 4224):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1420:
                                    shot = shot + "nwdx"
                                elif j < (1420 + 80):
                                    shot = shot + "*"
                            else: 
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1447:
                                    shot = shot + "7"
                                elif (i < 1447 + 4398):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 2375:
                                    shot = shot + "nwdx"
                                elif j < (2375 + 892):
                                    shot = shot + "*"

                        elif (any("2" in s for s in current_tree.
                                  get_shot_of_node(self.leaf_node))):
                            print("2 fount in Leaf Node")
                            if (shot == "1"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1713:
                                    shot = shot + "7"
                                elif (i < 1713 + 4879):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1531:
                                    shot = shot + "nwdx"
                                elif j < (1531 + 1123):
                                    shot = shot + "*"

                            elif (shot == "2"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1373:
                                    shot = shot + "7"
                                elif (i < 1373 + 4816):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 936:
                                    shot = shot + "nwdx"
                                elif j < (936 + 99):
                                    shot = shot + "*"

                            else: 
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1528:
                                    shot = shot + "7"
                                elif (i < 1528 + 5039):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1258:
                                    shot = shot + "nwdx"
                                elif j < (1258 + 734):
                                    shot = shot + "*"
                        else: 
                            print("3 found in Leaf Node.")
                            if (shot == "1"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1277:
                                    shot = shot + "7"
                                elif (i < 1277 + 4271):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 2493:
                                    shot = shot + "nwdx"
                                elif j < (2493 + 1221):
                                    shot = shot + "*"

                            elif (shot == "2"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1355:
                                    shot = shot + "7"
                                elif (i < 1355 + 4429):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1171:
                                    shot = shot + "nwdx"
                                elif j < (1171 + 67):
                                    shot = shot + "*"
                            else: 
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1837:
                                    shot = shot + "7"
                                elif (i < 1837 + 4803):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1155:
                                    shot = shot + "nwdx"
                                elif j < (1155 + 271):
                                    shot = shot + "*"

                    # 4th was MCTS Agent returning 1st in the ralley?
                    else:
                        print("In a ralley, where MCTS was returning a 1st.")
                        if (any("1" in s for s in current_tree.
                                get_shot_of_node(self.leaf_node))):
                            print("1 found in Leaf Node")
                            if (shot == "1"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 2587:
                                    shot = shot + "7"
                                elif (i < 2587 + 4533):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1780:
                                    shot = shot + "nwdx"
                                elif j < (1780 + 598):
                                    shot = shot + "*"

                            elif (shot == "2"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1915:
                                    shot = shot + "7"
                                elif (i < 1915 + 4308):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1568:
                                    shot = shot + "nwdx"
                                elif j < (1568 + 91):
                                    shot = shot + "*"
                            else: 
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1632:
                                    shot = shot + "7"
                                elif (i < 1632 + 4177):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 2566:
                                    shot = shot + "nwdx"
                                elif j < (2566 + 976):
                                    shot = shot + "*"

                        elif (any("2" in s for s in current_tree.
                                  get_shot_of_node(self.leaf_node))):
                            print("2 fount in Leaf Node")
                            if (shot == "1"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1710:
                                    shot = shot + "7"
                                elif (i < 1710 + 4779):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1613:
                                    shot = shot + "nwdx"
                                elif j < (1613 + 1142):
                                    shot = shot + "*"

                            elif (shot == "2"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1363:
                                    shot = shot + "7"
                                elif (i < 1363 + 4751):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1047:
                                    shot = shot + "nwdx"
                                elif j < (1047 + 114):
                                    shot = shot + "*"
                            else: 
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1489:
                                    shot = shot + "7"
                                elif (i < 1489 + 4974):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1309:
                                    shot = shot + "nwdx"
                                elif j < (1309 + 824):
                                    shot = shot + "*"
                        else: 
                            print("3 found in Leaf Node.")
                            if (shot == "1"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1404:
                                    shot = shot + "7"
                                elif (i < 1404 + 4112):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 2780:
                                    shot = shot + "nwdx"
                                elif j < (2780 + 1314):
                                    shot = shot + "*"

                            elif (shot == "2"):
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1556:
                                    shot = shot + "7"
                                elif (i < 1556 + 4265):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1366:
                                    shot = shot + "nwdx"
                                elif j < (1366 + 71):
                                    shot = shot + "*"
                            else: 
                                # Adding Depth encoding
                                i = random.randint(0, 9999)
                                if i < 1978:
                                    shot = shot + "7"
                                elif (i < 1978 + 4724):
                                    shot = shot + "8"
                                else: 
                                    shot = shot + "9"
                                    
                                # Adding Winner/Error encoding
                                j = random.randint(0, 9999)
                                if j < 1325:
                                    shot = shot + "nwdx"
                                elif j < (1325 + 349):
                                    shot = shot + "*"

        print("Altered Shot from Expansion Phase: " + str(shot))
        #print("Path of Selection Phase: " + str(self.expansion_path))
        self.expansion_shot = shot

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

    def add_node_to_mcts_tree(self, index, colour, node_type, shot_string, depth,
                     n_visits, n_wins, uct_value):
        '''A new node is added to the mcts tree.'''
        self.mcts_tree.add_node(node_for_adding=index,
                           colour=colour,
                           type=node_type,
                           shot=shot_string,
                           depth=depth,
                           n_visits=n_visits,
                           n_wins=n_wins,
                           uct_value=uct_value)
        
    def add_edge_to_mcts_tree(self, node_A, node_B, n_visits, uct_value,
                              win_count, direction):
        '''Adds a new edge between two given nodes'''
        self.mcts_tree.add_edge(node_A, node_B,
                           n_visits=n_visits,
                           uct_value=uct_value,
                           win_count=win_count,
                           direction=direction)
        
    def get_dir_of_shot_in_mcts_tree(self, node):
        '''Returns the direction of a shot od a given Node'''
        direction = ""
        node_shot = self.mcts_tree.nodes[node]['shot']

        if any('1' in s for s in node_shot):
            direction = '1'
        elif any('2' in s for s in node_shot):
            direction = '2'
        elif any('3' in s for s in node_shot):
            direction = '3'
        elif any('4' in s for s in node_shot):
            direction = '4'
        elif any('5' in s for s in node_shot):
            direction = '5'
        elif any('6' in s for s in node_shot):
            direction = '6'

        return direction

    def copy_ralley_to_mcts_ralley(self, current_ralley):
        '''Copys current_ralley to the mcts ralley'''
        for i in range(0, current_ralley.get_len_ralley()):
            self.mcts_ralley.add_shot_to_ralley(current_ralley[i])

    def add_shot_to_mcts_ralley(self, shot):
        '''Adds a shot (Expansion shot&Simu shots) to the mcts ralley'''
        self.mcts_ralley.add_shot_to_ralley(shot)

    def show_mcts_tree(self):
        '''When this function is called, it will draw the mcts tree.'''
        colours = list(nx.get_node_attributes(self.mcts_tree,'colour').values())
        pos = graphviz_layout(self.mcts_tree, prog="dot")
        nx.draw(self.mcts_tree,
                pos,
                node_color = colours,
                node_size = 170,
                labels=nx.get_node_attributes(self.mcts_tree, 'shot'), 
                with_labels=True, 
                font_size=6,
                font_weight='bold')
        edge_labels = dict([((n1, n2), d['n_visits'])
                            for n1, n2, d in self.mcts_tree.edges(data=True)])
        nx.draw_networkx_edge_labels(self.mcts_tree, 
                                     pos, 
                                     edge_labels=edge_labels, 
                                     font_size=6)

        # draw the tree
        plt.show()