import random
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import simpler_stat_bot_djoko as djoko
import rally
import copy
import math
import numpy as np
import constants as const
import average_stat_bot

class MCTS_Greedy_Agent:
    '''In this class, the MCTS Algorithm with UCT Selection policy 
    is used to find the next shot in a rally'''

    def __init__(self, name="", turn=False):
        self.name = name
        self.turn = turn
        self.active_mcts_node = 0
        self.mcts_node_index = 0
        self.leaf_node = 0
        self.shot = ""
        self.x = "in_play"
        self.active_simu_node = 0
        self.first_service = True
        self.mcts_agents_turn = False
        self.expansion_node = 0
        self.expansion_shot = ""
        self.exp_shot_list = []
        self.len_of_current_rally = 0
        self.expansion_path = [0]
        self.mcts_tree = nx.DiGraph()
        self.mcts_rally = rally.Rally()
        self.simulation_rally = rally.Rally()
        self.decision_node = 0

        if const.MenuVariables.decision_strat == 'uct':
            self.decision_strategy = 'uct'
        elif const.MenuVariables.decision_strat == 'greedy':
            self.decision_strategy = 'greedy'

        if const.MenuVariables.top_bot == 3:
            self.opponent = djoko.Simple_Stat_Bot_Djokovic("Simple_Djoko")
        elif const.MenuVariables.top_bot == 4:
            self.opponent = average_stat_bot.Average_Stat_Bot("Average_Bot")
        else: print("Error: Choose other opponent for MCTS Agent")

    def add_shot(self, current_rally, score, current_tree):
        '''This function is calling the different phases of MCTS'''
        #print("Hi")
        # Here we take the actual game tree and put it on top of the 
        # mcts_game_tree and the mcts_node_index is set to the current
        # Node Index of the actual game tree
        self.mcts_tree = nx.DiGraph()
        self.mcts_node_index = current_tree.get_node_index()
        self.mcts_tree = nx.compose(self.mcts_tree, current_tree.get_tree())
        self.mcts_rally.clear_rally()
        self.decision_node = 0

        # The rally is a deepcopy (new storage loc) of the current real
        # rally
        self.mcts_rally = copy.deepcopy(current_rally)

        if (const.MenuVariables.show_tree == 'all_mcts_trees'):
            print("Initial Tree from the real game is displayed.")
            self.show_mcts_tree()

        # Here the Selection Phase is called
        self.selection_phase(current_rally, score, current_tree)
        
        #print("------------------------------------------------")
        #print("5. Making Choice and adding MCTS Shot to rally.")
        # Decission Node is root node, where we need to make the choice
        # It is set when the root node is found

        indices_of_neighbors = self.get_neighbors(self.decision_node)
        
        ucts_of_neighbors = self.get_ucts_of_neighbor_nodes(
            indices_of_neighbors)
        p_win_rate_of_neighbors = self.get_point_win_rate_of_node_list(
            indices_of_neighbors)
        
        highest_uct = 0
        highest_point_win_rate = 0
        pos = 0
        
        # Here we find the best child of decision node based on the 
        # decision strategy
        if (self.decision_strategy == 'uct'):
            #print("UCT Decision")
            for x in range(0, len(ucts_of_neighbors)):
                if highest_uct == 0:
                    pos = x
                    highest_uct = ucts_of_neighbors[x]
                elif ucts_of_neighbors[x] > highest_uct:
                    pos = x
                    highest_uct = ucts_of_neighbors[x]
        elif (self.decision_strategy == 'greedy'):
            #print("Greedy Decision")
            for x in range(0, len(p_win_rate_of_neighbors)):
                if highest_point_win_rate == 0:
                    pos = x
                    highest_point_win_rate = p_win_rate_of_neighbors[x]
                elif p_win_rate_of_neighbors[x] > highest_point_win_rate:
                    pos = x
                    highest_point_win_rate = p_win_rate_of_neighbors[x]
        else: print("Error: Decision strategie wasnt chosen correctly.")
        
        #print("Highest UCT Value of neihgbors is " 
        # + str(highest_uct) + "at position: " + str(pos))
        #print("So the Node where we need to get the direction from is: " 
        # + str(indices_of_neighbors[pos]))
        #print("And the shot in that node is: " 
        # + str(self.get_shot_of_node(indices_of_neighbors[pos])))
        #print("And the direction in that nodes shot encoding is: " 
        # + str(self.get_dir_of_shot_in_mcts_tree(indices_of_neighbors[pos])))

        dir = self.get_dir_of_shot_in_mcts_tree(indices_of_neighbors[pos])

        # Here we either add probabilities to a second serve with the 
        # corresponding function or we add them with the normal function
        if (current_rally.get_len_rally() == 1 
            and "," in current_rally.get_first_shot_of_rally()):
            new_shot = self.add_probs_to_2nd_serve(dir, score)
        else:
            new_shot = self.add_probs_to_shot(dir, score, current_tree, 
                                              expansion=False)
        
        if (current_rally.get_len_rally() == 0 and new_shot == "6nwdx"):
            print("current_rally: " + str(current_rally.get_rally()))
            print("Adding Shot: " + str(new_shot))
            print("Error: New Shot in MCTS Agent add_probs_to_shot function was done wrong!")

        current_rally.add_shot_to_rally(new_shot)
        #print("rally_after_MCTS_shot: " + str(current_rally.get_rally()))
        #print("_______________________________________________________")
        #print("-------------End of one MCTS iteration-----------------")
        #print("_______________________________________________________")

    def selection_phase(self, current_rally, score, current_tree):
        '''In the selection Phase, we traverse through the current tree,
        always taking the child node with the highest UCT Value until a
        leaf node is reached'''
        
        #print("--------------------------------")
        #print("1. Starting selection Phase!")
        #print("--------------------------------")
        #print(" 1.1 Setting the root node according to current rally.")
        
        # Blue_neighbors are only the neighbors nodes with color blue,
        # so the actions that have been taken by the MCTS Agent
        # from that node

        # The root node is always the node in the tree which represents 
        # the last shot in the current rally

        if (current_rally.get_len_rally() == 0):
            # If there is no shot in the rally yet, root node is 0
            self.set_active_mcts_node(0)
            self.decision_node = self.get_active_mcts_node()
            #print(" 1.2 Root Node is: " 
            # + str(self.get_active_mcts_node()) + " , should be 0.")
        else:
            # We have to find the rally in the current tree and go to 
            # last node/last shot of rally and find the index of that
            # node and set it to root node
            serving = score.get_serving_player()
            rally = copy.deepcopy(current_rally.get_rally())
            index = 0
            # from the Red Node, there can be 2x "6" encoding, we have 
            # to look at the current_rally, to see who is serving to 
            # take the right "6"
            if (serving == 1):
                neighbors = current_tree.get_list_of_blue_neighbors(index)
            elif (serving == 2):
                neighbors = current_tree.get_list_of_green_neighbors(index)
            
            # We look at each shot in the rally and find the enconding 
            # in the tree
            #print(" --> The rally where we get the ")
            for i in range(0, len(rally)):
                rally_shot = ""
                rally_shot = rally[i]
                neighbor_shots = current_tree.get_shots_of_neighbors(neighbors)
                neighbors_index = neighbor_shots.index(rally_shot)
                index = neighbors[neighbors_index]
                
                #self.expansion_path.append(index)
                self.add_node_to_expansion_path(index)

                neighbors = current_tree.get_neighbors(index)

            # the index in the end is the node, which represents the
            # last shot in the rally
            self.set_active_mcts_node(index)
            self.decision_node = self.get_active_mcts_node()
            self.mcts_tree.nodes[self.active_mcts_node]['colour'] = 'red'
            
            #print(" 1.2 Root Node is "
            #      + str(self.get_active_mcts_node()) 
            #      + " with shot encondging: " 
            #      + str(self.get_shot_of_node(self.get_active_mcts_node())))
        
        if (const.MenuVariables.show_tree == 'all_mcts_trees'):
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
            
            # Check who is serving in the current_rally

            # Each neighbors shot encoding is looked at
            blue_neighbor_shots = []
            blue_neighbor_shots = current_tree.get_shots_of_neighbors(
                blue_neighbors)
            
            #print("Blue Neighbors from Active Node: " 
            # + str(blue_neighbors))
            #print(" -- Blue Neighbors Shots: " + str(blue_neighbor_shots))
            
            #print("Green Neighbors from active Node: " 
            # + str(green_neighbors))
            #print("Green Neighbor Shots from acitve Node" 
            # + str(green_neighbor_shots))

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
            
            #print(" -- Color of Active MCTS Node: " 
            # + str(color_of_mcts_active_node))
            
            # If the color is red, we are still at the root node
            if (color_of_mcts_active_node == "red"):
                # If its the MCTS Agents turn to serve, maybe start with
                # a blue node else, start with a random green one
                
                # We check out all non terminal green neighbors
                if green_neighbors:
                    non_term_green_neighbors = []
                    for x in range(len(green_neighbors)):
                        if (self.shot_terminated(self.get_shot_of_node(
                            green_neighbors[x])) != "terminal"):
                            non_term_green_neighbors.append(green_neighbors[x])                 
                    
                # if root node has non term green children there is a 
                # 50% chance that one of the green neighbors is 
                # traversed
                j = random.randint(0, 99)
                if (j < 50 and green_neighbors):
                    #print("We pick random from green neighbor children")
                    
                    i = random.randint(0, len(green_neighbors)-1)
                    #print("The picked green Node is: " 
                    # + str(green_neighbors[i]))
                    self.set_active_mcts_node(green_neighbors[i])
                    self.add_node_to_expansion_path(green_neighbors[i])
                    self.add_shot_to_mcts_rally(self.get_shot_of_node(
                        green_neighbors[i]))

                # If there are no green neighbors or in 50% of the cases 
                # we traverse to a blue node
                else:
                    # If all three directions are found, then we go the
                    # child with the highest UCT Value and go again from
                    # there
                    if (dir_1_found and dir_2_found and dir_3_found
                        or dir_4_found and dir_5_found and dir_6_found):

                        # Here the Blue neighbor with the highest UCT Value is 
                        # found and set to active
                        highest_win_rate_neighbor = 0
                        for x in range(0, len(blue_neighbors)):
                            if highest_win_rate_neighbor == 0:
                                highest_win_rate_neighbor = blue_neighbors[x]
                            elif (current_tree.get_point_win_rate_of_node(
                                highest_win_rate_neighbor) <= 
                                current_tree.get_point_win_rate_of_node(blue_neighbors[x])):
                                highest_win_rate_neighbor = blue_neighbors[x]

                        self.set_active_mcts_node(highest_win_rate_neighbor)
                        self.add_node_to_expansion_path(highest_win_rate_neighbor)
                        self.add_shot_to_mcts_rally(self.get_shot_of_node(
                            highest_win_rate_neighbor))
                        
                    else:
                        self.set_leaf_node(self.get_active_mcts_node())
                        #print(" 1.4 Leaf Node was set at i = " + str(i) 
                        # + " With shot: " 
                        # + str(self.get_shot_of_node(self.leaf_node)))

            # If the color is green, we need to check the blue neighbors
            # and either go to highest uct or set it as leaf
            elif (color_of_mcts_active_node == "green"):
                # If active green node is first serve fault we check his 
                # neighbors and either pick one at random (He should 
                # always have at least 1 neighbor)
                shot_encoding_active = self.get_shot_of_node(
                    self.active_mcts_node)
                if (any("," in s for s in shot_encoding_active)):
                    #print("The current active MCTS Node is a first 
                    # serve fault of green: " + str(shot_encoding_active))
                    # When this is the case, we go to one of the second 
                    # serves at random
                    i = random.randint(0, len(green_neighbors)-1)
                    #print("The picked second serve is: " 
                    # + str(green_neighbors[i]))
                    self.set_active_mcts_node(green_neighbors[i])
                    self.add_node_to_expansion_path(green_neighbors[i])
                    self.add_shot_to_mcts_rally(self.get_shot_of_node(
                        green_neighbors[i]))

                # If all three directions are found, then we go the the 
                # child with the highest UCT Value and go again from 
                # there
                elif (dir_1_found and dir_2_found and dir_3_found
                    or dir_4_found and dir_5_found and dir_6_found):
                    
                    # Here the Blue neighbor with the highest UCT Value
                    # is found and set to active
                    highest_win_rate_neighbor = 0
                    for x in range(0, len(blue_neighbors)):
                        if highest_win_rate_neighbor == 0:
                            highest_win_rate_neighbor = blue_neighbors[x]
                        elif (current_tree.get_point_win_rate_of_node(
                            highest_win_rate_neighbor) <= 
                            current_tree.get_point_win_rate_of_node(
                                blue_neighbors[x])):
                            highest_win_rate_neighbor = blue_neighbors[x]
                    
                    self.set_active_mcts_node(highest_win_rate_neighbor)
                    self.add_node_to_expansion_path(highest_win_rate_neighbor)
                    self.add_shot_to_mcts_rally(self.get_shot_of_node(
                        highest_win_rate_neighbor))

                else:
                    self.leaf_node = self.get_active_mcts_node()    

            # If the color is blue, we need to see if it has
            # green neighbors. If it does, just pick a green neighbor at
            # random, if not we should be at a terminal node
            elif (color_of_mcts_active_node == "blue" 
                  and len(green_neighbors) != 0):
                #print("Green Neighbors from Active MCTS Node: " 
                # + str(green_neighbors))
                # One of the Green Neighbors is taken at random and set
                # to active
                if green_neighbors:
                    i = random.randint(0, len(green_neighbors)-1)

                    self.set_active_mcts_node(green_neighbors[i])
                    self.add_node_to_expansion_path(green_neighbors[i])
                    self.add_shot_to_mcts_rally(self.get_shot_of_node(
                        green_neighbors[i]))

            elif (color_of_mcts_active_node == "blue" and 
                  "," in self.get_shot_of_node(self.get_active_mcts_node())
                  and dir_4_found and dir_5_found and dir_6_found):
                # This is the scenario where a first serve fault node is 
                # active which has all three directions of the second 
                # serve in the children nodes. So we find the highest 
                # UCT neighbor and set it to active

                highest_win_rate_neighbor = 0
                for x in range(0, len(blue_neighbors)):
                    if highest_win_rate_neighbor == 0:
                        highest_win_rate_neighbor = blue_neighbors[x]
                    elif (current_tree.get_point_win_rate_of_node(
                        highest_win_rate_neighbor) <= 
                        current_tree.get_point_win_rate_of_node(
                            blue_neighbors[x])):
                        highest_win_rate_neighbor = blue_neighbors[x]
                
                self.set_active_mcts_node(highest_win_rate_neighbor)
                self.add_node_to_expansion_path(highest_win_rate_neighbor)
                self.add_shot_to_mcts_rally(self.get_shot_of_node(
                    highest_win_rate_neighbor))
                
            else:
                self.set_leaf_node(self.get_active_mcts_node())
                
            # Every time the While loop is left, we need to have set a
            # leaf node
            
            i += 1
            #print("--------------------------")
        
        #print(" 1.5 The rally that lead to leaf Node: " 
        # + str(self.mcts_rally.get_rally()))
        
        self.expansion_phase(current_rally, score, self.get_mcts_tree())
 
        self.mcts_rally.clear_rally()
        self.reset_active_mcts_node()
        self.reset_leaf_node()
        #print("Expansion_path before clearing it: " 
        # + str(self.expansion_path))
        self.clear_expansion_path()

        #self.show_mcts_tree()
    
    def expansion_phase(self, current_rally, score, current_tree):
        # We take the leave node and check the direction, which is
        # not yet in the leaf nodes children, and that is expanded and
        # is the node we start the simulation form
        #print(" 2.1 Leaf Node Shot encoding: " 
        #      + str(self.get_shot_of_node(self.leaf_node)))
        #print(" Exp Phase beginning: current_rally: " 
        # + str(current_rally.get_rally()))
        #print("2. Starting Expansion Phase!")

        #self.mcts_tree.nodes[self.leaf_node]['colour'] = 'orange'
        
        if (self.shot_terminated(self.get_shot_of_node(
            self.leaf_node)) == "terminal"):
            #print("Starting backprobagation Phase from terminal leaf node.")
            
            #print("MCTS rally that lead to backprobagation phase: " 
            #      + str(self.mcts_rally.get_rally()))
            #print("Acitve SImu Node: " 
            #      + str(self.get_active_simu_node()))
            
            self.simulation_rally = copy.deepcopy(self.mcts_rally)
            #print("Simulation rally that lead to backprobagation phase: " 
            #      + str(self.simulation_rally.get_rally()))
            self.backpropagation_phase()

        #print("exp_shot_list is cleared before each expansion phase")
        self.exp_shot_list.clear()
            
        # Get children of the leaf node
        children_of_leaf_node = self.get_blue_neighbors(self.leaf_node)
        shots_of_shildren = self.get_shots_of_neighbor_nodes(
            children_of_leaf_node)
        # Here we check which directions were found in the childrens of
        # the leaf node
        dir_1_in_children = False
        dir_2_in_children = False
        dir_3_in_children = False
        dir_4_in_children = False
        dir_5_in_children = False
        dir_6_in_children = False
        #print("Children of Leaf Node: " + str(children_of_leaf_node))
        #print("Shots of Children of Leaf node: " + str(shots_of_shildren))
        for x in range(0, len(shots_of_shildren)):
            if any("1" in s for s in str(shots_of_shildren[x])):
                dir_1_in_children = True
            if any("2" in s for s in str(shots_of_shildren[x])):
                dir_2_in_children = True
            if any("3" in s for s in str(shots_of_shildren[x])):
                dir_3_in_children = True
            if any("4" in s for s in str(shots_of_shildren[x])):
                dir_4_in_children = True
            if any("5" in s for s in str(shots_of_shildren[x])):
                dir_5_in_children = True
            if any("6" in s for s in str(shots_of_shildren[x])):
                dir_6_in_children = True

        #print("1 found: " + str(dir_1_in_children) 
        # + ", 2 found: " + str(dir_2_in_children)
        # + ", 3 found: " + str(dir_3_in_children)
        # + ", 4 found: " + str(dir_4_in_children)
        # + ", 5 found: " + str(dir_5_in_children)
        # + ", 6 found: " + str(dir_6_in_children))
        #print("Amount of children of leaf node: " + str(len(children_of_leaf_node)))

        # special case: we need to check if the leaf node was a first
        # serve fault and then expand a second serve from there
        shot_encoding = self.get_shot_of_node(self.leaf_node)

        if any("," in s for s in shot_encoding):
            #print(" 2.2 Leaf Node is 1st serve fault, need to expand 2nd serve")
            if children_of_leaf_node:
                #shots_of_children = self.get_shots_of_neighbors(children_of_leaf_node)
                #print("  2.2.1 Leaf node is first serve fault with children")
                #print("  --> We add all the directions that have not yet been found in children of the leaf node.")
                
                if dir_4_in_children and dir_5_in_children and dir_6_in_children:
                    print("Error, Leaf node has all serve directions in children")
                elif dir_4_in_children and dir_5_in_children:
                    self.add_probs_to_2nd_serve("6", score)
                elif dir_5_in_children and dir_6_in_children:
                    self.add_probs_to_2nd_serve("4", score)
                elif dir_4_in_children and dir_6_in_children:
                    self.add_probs_to_2nd_serve("5", score)
                elif dir_4_in_children:
                    self.add_probs_to_2nd_serve("5", score)
                    self.add_probs_to_2nd_serve("6", score)
                elif dir_5_in_children:
                    self.add_probs_to_2nd_serve("4", score)
                    self.add_probs_to_2nd_serve("6", score)
                elif dir_6_in_children:
                    self.add_probs_to_2nd_serve("4", score)
                    self.add_probs_to_2nd_serve("5", score)

            else:
                #print("  2.2.1 2nd Serve & No children of leaf node found.")
                #print("   2.2.1.1 -> add all the directions")
                
                self.add_probs_to_2nd_serve("4", score)
                self.add_probs_to_2nd_serve("5", score)
                self.add_probs_to_2nd_serve("6", score)

        # When the root is a leaf node, we expand a random direction
        elif self.leaf_node == 0:
            #print(" 2.2 Leaf Node is Node[0] Adding a new first serve as exp.")
            # When there are already first serves, we check to see which
            # ones were played already
            if children_of_leaf_node:
                #shots_of_children = self.get_shots_of_neighbors(children_of_leaf_node)
                
                #print("  2.2.1 Leaf Node has children. Adding dir thats not in children yet")
                #print("  -->> We have to add all the directions that are not in the children yet.")
                
                if dir_4_in_children and dir_5_in_children and dir_6_in_children:
                    print("Error: all serve directions found in children of leaf node.")
                elif dir_4_in_children and dir_5_in_children:
                    self.add_probs_to_shot("6", score, current_tree)
                elif dir_4_in_children and dir_6_in_children:
                    self.add_probs_to_shot("5", score, current_tree)
                elif dir_5_in_children and dir_6_in_children:
                    self.add_probs_to_shot("4", score, current_tree)
                elif dir_4_in_children:
                    self.add_probs_to_shot("5", score, current_tree)
                    self.add_probs_to_shot("6", score, current_tree)
                elif dir_5_in_children:
                    self.add_probs_to_shot("4", score, current_tree)
                    self.add_probs_to_shot("6", score, current_tree)
                elif dir_6_in_children:
                    self.add_probs_to_shot("4", score, current_tree)
                    self.add_probs_to_shot("5", score, current_tree)
                
            else:
                #print("  2.2.1 No children of leaf node found. Adding all dir to exp at random")
                
                self.add_probs_to_shot("4", score, current_tree)
                self.add_probs_to_shot("5", score, current_tree)
                self.add_probs_to_shot("6", score, current_tree)

        else:
            if children_of_leaf_node:
                # When the leaf node already has children, we need to
                # check their directions and add a shot with a direction,
                # that is'nt in the tree yet
                #print(" 2.2 Leaf node has children, we add dir to exp thats not in children yet")
                               
                if dir_1_in_children and dir_2_in_children and dir_3_in_children:
                    print("Error: all shot direction found in children of leaf node.")
                elif dir_1_in_children and dir_2_in_children:
                    self.add_probs_to_shot("3", score, current_tree)
                elif dir_1_in_children and dir_3_in_children:
                    self.add_probs_to_shot("2", score, current_tree)
                elif dir_2_in_children and dir_3_in_children:
                    self.add_probs_to_shot("1", score, current_tree)
                elif dir_1_in_children:
                    self.add_probs_to_shot("2", score, current_tree)
                    self.add_probs_to_shot("3", score, current_tree)
                elif dir_2_in_children:
                    self.add_probs_to_shot("1", score, current_tree)
                    self.add_probs_to_shot("3", score, current_tree)
                elif dir_3_in_children:
                    self.add_probs_to_shot("1", score, current_tree)
                    self.add_probs_to_shot("2", score, current_tree)

            else:
                #print(" 2.2 No children of leaf node found, expanding all missing directions")
                #print("  2.2.1 We expand 3 nodes (in the direction 1, 2 and 3)")
                
                self.add_probs_to_shot("1", score, current_tree)
                self.add_probs_to_shot("2", score, current_tree)
                self.add_probs_to_shot("3", score, current_tree)

        # Now we should have a shot encoding for the expansion and we
        # add it to the mcts tree.
        
        #print("Final exp_shot_list: " + str(self.exp_shot_list))

        for i in range(0, len(self.exp_shot_list)):
            exp_shot = self.exp_shot_list[i]
            exp_shot_index = self.get_next_mcts_node_index()
            exp_shot_depth = current_rally.get_len_rally() + 1
            
            # Here we add the expansion shot to the leaf node of the tree
            self.add_node_to_mcts_tree(exp_shot_index, 
                                       colour="yellow",
                                       node_type="Expansion",
                                       shot_string=exp_shot,
                                       depth=exp_shot_depth,
                                       n_visits=0,
                                       n_wins=0,
                                       uct_value=0,
                                       point_win_rate=0)
            
            exp_shot_dir = self.get_dir_of_shot_in_mcts_tree(exp_shot_index)

            self.set_expansion_node(exp_shot_index)

            self.add_edge_to_mcts_tree(node_A=self.get_leaf_node(), 
                                    node_B=exp_shot_index, 
                                    n_visits=0, uct_value=0,
                                    win_count=0, direction=exp_shot_dir)
            
            self.add_node_to_expansion_path(self.get_expansion_node())
            self.expansion_shot = exp_shot
            self.add_shot_to_mcts_rally(self.get_expansion_shot())
            #print("Get MCTS rally, when exp shot just was added: " + str(self.mcts_rally.get_rally()))
           
            self.set_active_simu_node(self.get_expansion_node())
            
            if (self.shot_terminated(self.get_expansion_shot()) == "terminal"):
                #print("Starting backpropagaton phase from terminal expansion shot.")
                self.simulation_rally = copy.deepcopy(self.mcts_rally)
                self.backpropagation_phase()
                
            else:
                #print("-----------------------------")
                #print("3. Starting Simulation Phase!")
                #print("-----------------------------")
                #print("with mcts_rally: " + str(self.mcts_rally.get_rally()))
                self.simulation_phase(current_rally, score, current_tree)
            
            self.mcts_rally.remove_last_shot()
            self.expansion_path.pop()
        
        if (const.MenuVariables.show_tree == 'all_mcts_trees'):
            print(" 2.3 Displaying MCTS Tree with yellow expansion Shots.")
            self.show_mcts_tree()

    def simulation_phase(self, current_rally, score, current_tree):
        # starting from the expansion node, simulation is done.
        # Djoko Bot and MCTS Simulation Strategy (e.g. Random,
        # MC-Evaluation, or others) take turns in adding a shot until
        # terminal state is reached

        # We start with the expansion shot.
        #print("Current rally is: " + str(current_rally.get_rally()))
        #print("beginning of simulation phase: MCTS rally is: " + str(self.mcts_rally.get_rally()))
        #print(" 3.1 Expanded shot: " + str(self.expansion_shot))
        
        # Range(x) x is number of simulations we do from the expanded 
        # Node

        #print(" 3.1.1 MCTS rally before simu loop starts: " + str(self.mcts_rally.get_rally()))

        #self.simulation_rally = self.mcts_rally
        self.simulation_rally = copy.deepcopy(self.mcts_rally)
        #print(" 3.1 Simulation_rally: " + str(self.simulation_rally.get_rally()))
        
        n_simus = const.MenuVariables.simu_rallys
        for _ in range(n_simus):
            #print("----------------------------------")
            # for each simualtion we set thon "ongoing" bool to true and
            # the mcts agents turn to false

            #print("Simu rally in the beginning of new simulation rally: " + str(self.simulation_rally.get_rally()))
            
            # init failsafe for while loop and bool for rally termination
            rally_ongoing = True
            i = 0

            # first we check if the Expansion Shot is terminal or not or
            # wether its a first serve fault.
            self.x = self.shot_terminated(self.expansion_shot)
            if (self.x == "second_serve"):
                # If exp shot was first serve fault, its mcts Agents
                # turn for adding a second serve
                self.mcts_agents_turn = True

            # This while loop runs until the rally is over, by checking if
            # a terminal shot was played
            while (rally_ongoing == True): 
                
                # in the while loop we always have an active simu node
                # from that simunode we get the shots and colors of the
                # neighbor nodes and safe them here
                #shot_dict = self.get_shot_dict_of_neighbors(
                #    self.get_active_simu_node())
                #colour_dict = self.get_colour_dict_of_neighbors(
                #    self.get_active_simu_node())

                # In the beginning we assume that the next node will not
                # be in mcts tree yet
                shot_in_tree = False

                # We go through 3 if statements here: 
                if (self.x == "in_play" and self.mcts_agents_turn == False):
                    #print(" 3.2 The expanded shot is in play and MCTS Agents turn is False.")
                    # The Expansion shot is always a Shot of the 
                    # MCTS agent, so we need to add a shot of the 
                    # opponent first unless exp shot is 1st serve fault

                    # here we get the next simulated shot encoding of 
                    # the opponents shot
                    #print("Getting Bots shot when we give him simu_rally, when its his turn: " + str(self.simulation_rally.get_rally()))
                    #print("Getting Bots shot count simu_rally before he adds a shot: " + str(self.simulation_rally.get_shot_count()))

                    bot_shot = self.opponent.add_shot(
                        current_rally=self.simulation_rally,
                        score=score,
                        current_tree=self.mcts_tree,
                        simulation_phase=True)
                    
                    # Then we set the next index, but only if shot not 
                    # in children of current node

                    # We check the shot encodings of the neighbors of 
                    # the active simu node and see if one matches the 
                    # bot_shot

                    #print(" ----->>> Bot_shot: " + str(bot_shot))
                    neighbor_lst = self.get_shot_list_of_simu_neighbors_new(
                        self.get_active_simu_node())
                    
                    if bot_shot in neighbor_lst:

                        shot_dict = self.get_shot_dict_of_neighbors_new(
                            self.get_active_simu_node())
                        colour_dict = self.get_colour_dict_of_neighbors_new(
                            self.get_active_simu_node())
                        
                        index_lst = []
                        for x in neighbor_lst:
                            if (x == bot_shot):
                                matching_shot = x
                                index_lst = [k for k,v in shot_dict.items()
                                             if v == matching_shot]
                                for h in range(len(index_lst)):
                                    if (colour_dict[index_lst[h]] ==
                                        "springgreen"):
                                        shot_in_tree = True
                                        self.set_active_simu_node(index_lst[h])
                                        self.switch_simu_turns()

                    if (shot_in_tree == False):
                        simu_bot_node_index = self.get_next_mcts_node_index()
                        simu_bot_shot_depth = current_rally.get_len_rally()+1
                        
                        #print("The simulated shot of Djoko: " + str(bot_shot))

                        self.add_node_to_mcts_tree(index=simu_bot_node_index,
                                                   colour="springgreen",
                                                   node_type="Simu_Djoko",
                                                   shot_string=bot_shot,
                                                   depth=simu_bot_shot_depth,
                                                   n_visits=0, 
                                                   n_wins=0, 
                                                   uct_value=0,
                                                   point_win_rate=0)
                        
                        direction = self.get_dir_of_shot_in_mcts_tree(simu_bot_node_index)

                        self.add_edge_to_mcts_tree(node_A=self.get_active_simu_node(),
                                                   node_B=simu_bot_node_index,
                                                   n_visits=0,
                                                   uct_value=0,
                                                   win_count=0,
                                                   direction=direction)
                        
                        self.set_active_simu_node(simu_bot_node_index)
                        self.switch_simu_turns()
                    
                    self.add_shot_to_simu_rally(bot_shot)
                    
                    #if (const.MenuVariables.show_tree == 'all_mcts_trees'):
                    #    print("The MCTS_Tree with the first simu shot from expanded node is displayed.")
                    #    self.show_mcts_tree()
                        
                elif (self.x == "second_serve" and self.mcts_agents_turn == True):
                    #print(" 3.2 The expanded shot is a first serve fault and its the mcts agents turn = True.")
                    # Here we need to start simulation with a second serve of 
                    # the mcts agent

                    # Therefore we check if there are children in the mcts tree 
                    # of the expanded first serve fault
                    children = self.mcts_tree.neighbors(
                        self.get_expansion_node())
                    children_lst = list(children)
                    # print(children_lst)

                    if (len(children_lst) != 0):
                        #print("  3.2.1 and it has children.")
                        # If expansion node has children, we need to look at the
                        # directions, that already have been explored and add
                        # a new one
                        shots_of_children = self.get_shots_of_neighbor_nodes(
                            children_lst)
                        
                        dir_4_found = False
                        dir_5_found = False
                        dir_6_found = False

                        for i in range(0, len(shots_of_children)):
                            if (any("4" in s for s in shots_of_children[i])):
                                dir_4_found = True
                            if (any("5" in s for s in shots_of_children[i])):
                                dir_5_found = True
                            if (any("6" in s for s in shots_of_children[i])):
                                dir_6_found = True

                        if dir_4_found and dir_5_found:
                            second_simu_serve = "6"
                        elif dir_4_found and dir_6_found:
                            second_simu_serve = "5"
                        elif dir_5_found and dir_6_found:
                            second_simu_serve = "4"
                        elif dir_4_found:
                            i = random.randint(0, 99)
                            if i < 50:
                                second_simu_serve = "5"
                            else: second_simu_serve = "6"
                        elif dir_5_found:
                            i = random.randint(0, 99)
                            if i < 50:
                                second_simu_serve = "4"
                            else: second_simu_serve = "6"
                        elif dir_6_found:
                            i = random.randint(0, 99)
                            if i < 50:
                                second_simu_serve = "4"
                            else: second_simu_serve = "5"

                        if dir_4_found and dir_5_found and dir_6_found:
                            i = random.randint(0, 99)
                            if i < 33:
                                second_simu_serve = "4"
                            elif i < 66:
                                second_simu_serve = "5"
                            else: 
                                second_simu_serve = "6"

                    else:
                        # Add a second serve direction from mcts bot to the
                        # simulation at random
                        #print("  3.2.1 and it has no children.")
                        i = random.randint(0, 99)
                        if i < 33:
                            second_simu_serve = "4"
                        elif i < 66:
                            second_simu_serve = "5"
                        else: 
                            second_simu_serve = "6"
                    
                    sec_serve_sim = self.add_probs_to_2nd_serve(
                        shot=second_simu_serve, score=score)

                    #print(" 3.3 2nd serve shot enconding for simu phase is: " + str(sec_serve_sim))
                    
                    neighbor_lst = self.get_shot_list_of_simu_neighbors_new(
                        self.get_active_simu_node())
                    
                    if sec_serve_sim in neighbor_lst:
                        
                        shot_dict = self.get_shot_dict_of_neighbors_new(
                            self.get_active_simu_node())
                        colour_dict = self.get_colour_dict_of_neighbors_new(
                            self.get_active_simu_node())
                        
                        index_lst = []
                        for x in neighbor_lst:
                            if (x == sec_serve_sim):
                                matching_shot = x
                                index_lst = [k for k,v in shot_dict.items()
                                             if v == matching_shot]
                                for h in range(len(index_lst)):
                                    if (colour_dict[index_lst[h]] 
                                        == "lightskyblue"):
                                        shot_in_tree = True
                                        self.set_active_simu_node(index_lst[h])
                                        self.switch_simu_turns()
                    
                    if (shot_in_tree == False):
                    
                        sec_serve_index = self.get_next_mcts_node_index()
                        depth = current_rally.get_len_rally() + 1

                        self.add_node_to_mcts_tree(index=sec_serve_index,
                                                   colour="lightskyblue",
                                                   node_type="MCTS_2nd",
                                                   shot_string=sec_serve_sim,
                                                   depth=depth,
                                                   n_visits=0, 
                                                   n_wins=0, 
                                                   uct_value=0,
                                                   point_win_rate=0)
                        
                        direction = self.get_dir_of_shot_in_mcts_tree(
                            sec_serve_index)

                        self.add_edge_to_mcts_tree(node_A=self.get_active_simu_node(),
                                                   node_B=sec_serve_index,
                                                   n_visits=0,
                                                   uct_value=0,
                                                   win_count=0,
                                                   direction=direction)
                        self.set_active_simu_node(sec_serve_index)
                        self.switch_simu_turns()
                    
                    self.add_shot_to_simu_rally(sec_serve_sim)
                    
                    self.x = "in_play"

                elif (self.x == "in_play" and self.mcts_agents_turn == True):
                    # we need to add a normal shot from mcts agent to the 
                    # simulation phase
                    #print(" 3.2 Add a simulation shot from the mcts agent to the rally. MCTS Agents Turn = True")
                    
                    i = random.randint(0, 99)
                    if i < 33:
                        simu_shot = "1"
                    elif i < 66:
                        simu_shot = "2"
                    else: 
                        simu_shot = "3"

                    altered_simu_shot = self.add_probs_to_shot(shot=simu_shot,
                                                               score=score,
                                                               current_tree=self.mcts_tree,
                                                               expansion=False)

                    #print("children_shot_list: " + str(self.get_shot_list_of_simu_neighbors(self.get_active_simu_node())))
                    #print("simu shot MCTS Shot: " + str(altered_simu_shot))

                    neighbor_lst = self.get_shot_list_of_simu_neighbors_new(self.get_active_simu_node())

                    if altered_simu_shot in neighbor_lst:
                        
                        shot_dict = self.get_shot_dict_of_neighbors_new(
                            self.get_active_simu_node())
                        colour_dict = self.get_colour_dict_of_neighbors_new(
                            self.get_active_simu_node())


                        index_lst = []
                        for x in neighbor_lst:
                            if (x == altered_simu_shot):
                                matching_shot = x
                                index_lst = [k for k,v in shot_dict.items()
                                            if v == matching_shot]
                                for h in range(len(index_lst)):
                                    if (colour_dict[index_lst[h]] 
                                        == "lightskyblue"):
                                        shot_in_tree = True
                                        self.set_active_simu_node(index_lst[h])
                                        self.switch_simu_turns()

                    if (shot_in_tree == False):
                        altered_simu_shot_index = self.get_next_mcts_node_index()
                        depth_mcts_simu = current_rally.get_len_rally() + 1

                        self.add_node_to_mcts_tree(index=altered_simu_shot_index,
                                                   colour="lightskyblue",
                                                   node_type="MCTS_Simu_Shot",
                                                   shot_string=altered_simu_shot,
                                                   depth=depth_mcts_simu,
                                                   n_visits=0,
                                                   n_wins=0,
                                                   uct_value=0,
                                                   point_win_rate=0)

                        dir_simu_shot = self.get_dir_of_shot_in_mcts_tree(
                            altered_simu_shot_index)

                        self.add_edge_to_mcts_tree(node_A=self.get_active_simu_node(), 
                                            node_B=altered_simu_shot_index, 
                                            n_visits=0, uct_value=0, win_count=0,
                                            direction=dir_simu_shot)

                        self.set_active_simu_node(altered_simu_shot_index)
                        self.switch_simu_turns()

                    self.add_shot_to_simu_rally(altered_simu_shot)
                
                else: print("Error: Scenario in three if statements in simulation not covered!")

                # Testing wether the last added shot was terminal or not:
                if ("nwdx" in self.get_shot_of_node(
                    self.get_active_simu_node())
                    and "nwdx," not in self.get_shot_of_node(
                        self.get_active_simu_node())
                    or "*" in self.get_shot_of_node(
                        self.get_active_simu_node())
                    or self.x == "terminal"):
                    
                    #if self.x == "terminal": print(" 3.3 Exp Shot was terminal.")
                    #else: print(" 3.3 Last shot was terminal.")
                    
                    #print("Starting backpropagation from normal terminal shot in rally.")
                    self.backpropagation_phase()
                    
                    self.simulation_rally.remove_last_n_elements_of_rally(
                        len(self.expansion_path)-1)

                    self.set_active_simu_node(self.get_expansion_node())
                    self.mcts_agents_turn = False
                    rally_ongoing = False
                i += 1
            
    def backpropagation_phase(self, from_leaf_node=False):
        '''During backprobagation the 'n_wins' and 'n_visits' node 
        attributes are updated for the expansion path nodes'''

        #print("----------------------------")
        #print("4. Start of Backpropagation Phase!")
        #print("The expansion path that we possibly need to backprobagate through: " + str(self.expansion_path))
        #print("The simulation rally, that lead to the backprobagation: " + str(self.simulation_rally.get_rally()))
        #print("The last shot that was taken and that was terminal: " + str(self.simulation_rally.get_last_shot()))
        
        #print("Shot of active simu Node when backproba was started: " + str(self.get_shot_of_node(self.get_active_simu_node())))
        
        self.set_active_simu_node(self.expansion_path[-1])
        
        #print("The colour of last shot that was taken and that was terminal: " + str(self.mcts_tree.nodes[self.active_simu_node]['colour']))

        # We need to update the visit counts of all nodes in the 
        # expansion path, regardless of who won the point

        #print("Expansion Path: " + str(self.expansion_path))

        col_term_node = self.mcts_tree.nodes[self.mcts_node_index]['colour']

        if (col_term_node == "lightskyblue" or col_term_node == "yellow" 
            or col_term_node == "blue"):
            if ("*" in self.simulation_rally.get_last_shot()):
                # We update n_wins. MCTS shot was a winner.
                for x in range(1, len(self.expansion_path)):
                    self.mcts_tree.nodes[self.expansion_path[x]]['n_wins'] += 1      
        elif (col_term_node == "springgreen" or col_term_node == "green"):
            if ("nwdx" in self.simulation_rally.get_last_shot()):
                # We update n_wins. Bot shot was a error.
                for x in range(1, len(self.expansion_path)):
                    self.mcts_tree.nodes[self.expansion_path[x]]['n_wins'] += 1
        else: print("Error: Color was'nt matched Color: " + str(col_term_node))

        #Here we update the visit counts for the whole expansion path."
        for x in range(0, len(self.expansion_path)):
            self.mcts_tree.nodes[self.expansion_path[x]]['n_visits'] += 1
            
            wi = self.mcts_tree.nodes[self.expansion_path[x]]['n_wins']
            si = self.mcts_tree.nodes[self.expansion_path[x]]['n_visits']
            
            self.mcts_tree.nodes[self.expansion_path[x]][
                'point_win_rate'] = wi/si
            
        # Here we update the 'n_visits' attribute on the edges
        for x in range(0, len(self.expansion_path)-1):
            self.mcts_tree[self.expansion_path[x]][
                self.expansion_path[x+1]]['n_visits'] += 1
        
        # Here we update the 'uct_value' attribute of the nodes in 
        # the expansion path
        c = const.Config.c_value

        for x in range(0, len(self.expansion_path)):
            # first we need to get the predecessors n_visits
            # then we need the n_visits of the node in exp_path
            # and the n_wins of the node in the exp_path
            
            # wi ... current nodes number of simulations, that were won
            wi = self.mcts_tree.nodes[self.expansion_path[x]]['n_wins']
            # si ... current nodes total number of simulations
            si = self.mcts_tree.nodes[self.expansion_path[x]]['n_visits']
            # sp ... parent node's current number of simulations
            sp = self.mcts_tree.nodes[self.expansion_path[x-1]]['n_visits']
            
            self.mcts_tree.nodes[self.expansion_path[x]][
                'uct_value'] = (wi/si) + c*math.sqrt((np.log(sp))/si)
            
        #print("Node from where we need to choose: " + str(self.expansion_path[-2]))
        #print("Get the Node with the highest UCT Value from ")

    def get_shots_of_neighbor_nodes(self, node_list):
        '''Return a list of shots of a given List of nodes'''
        neighbor_shots = []
        for x in range(0, len(node_list)):
            neighbor_shot = self.mcts_tree.nodes[node_list[x]]['shot']
            neighbor_shots.append(neighbor_shot)
        return neighbor_shots
    
    def get_ucts_of_neighbor_nodes(self, node_list):
        '''Return a list of uct values of a given List of nodes'''
        neighbor_ucts = []
        for x in range(0, len(node_list)):
            neighbor_uct = self.mcts_tree.nodes[node_list[x]]['uct_value']
            neighbor_ucts.append(neighbor_uct)
        return neighbor_ucts
    
    def get_point_win_rate_of_node_list(self, node_list):
        '''Return a list of point_win_rate values of a given 
        List of nodes'''
        node_win_rates = []
        for x in range(0, len(node_list)):
            node_win_rate = self.mcts_tree.nodes[node_list[x]]['point_win_rate']
            node_win_rates.append(node_win_rate)
        return node_win_rates
    
    def get_point_win_rate_of_node(self, node):
        '''Returns the point win rate of a given Node.'''
        return self.mcts_tree.nodes[node]['point_win_rate']

    def get_active_simu_node(self):
        '''Returns the active simu Node'''
        return self.active_simu_node

    def set_active_simu_node(self, node):
        '''Sets the active Simu node to the given node'''
        self.active_simu_node = node

    def reset_active_simu_node(self):
        '''Resets the active Simu Node to Expansion Node'''
        self.active_simu_node = self.get_expansion_node()

    def get_expansion_node(self):
        '''Returns teh current Expansion Node'''
        return self.expansion_node
    
    def set_expansion_node(self, node):
        '''Sets the expansion Node to the given Node'''
        self.expansion_node = node

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
    
    def add_probs_to_shot(self, shot, score, current_tree, first_serve=True, expansion=True):
        '''Sets the value of the expansion_shot. Called during the 
        Expansion Phase to alter the shot direction with the 
        corresponding probabilities'''
        # Adding the probabilites of errors and winners 
        # to the chosen action (One action can lead to different states)
        
        #print("Expansion Path in the beginning of adding probs to shot: " + str(self.expansion_path))

        self.first_service = True
        if self.simulation_rally.get_shot_count() != 0:
            first_serve_encoding = self.simulation_rally.get_first_shot_of_rally()
            if "," in first_serve_encoding:
                #print("First serve is set to false because: , :was found")
                self.first_service = False

        # if we add probas to an expansion shot, the shot of parent node
        # is the shot encoding of the leaf node 
        if expansion == True:
            parent_node_shot = self.get_shot_of_node(self.leaf_node)
            parent_node_depth = self.get_depth(self.leaf_node)
        elif expansion == False:
            parent_node_shot = self.get_shot_of_node(self.get_active_simu_node())
            parent_node_depth = self.get_depth(self.get_active_simu_node())

        #print("Parent_Node_Shot = " + str(parent_node_shot))
        #print("First shot of Simurally, before adding probs to a shot: " + str(self.simulation_rally.get_rally()))
        #print("First serve: " + str(self.first_service))
        #print("shot encoding expansion node before alterations: " + str(shot))
        #print("Self.MCTS rally: " + str(self.mcts_rally.get_rally()))
        #print("Len of mcts_rally: " + str(self.mcts_rally.get_len_rally()))
        #print("Self.first_servince: " + str(self.first_service))
        #print("first_serve: " + str(first_serve))

        if self.mcts_rally.get_len_rally() == 0:
            self.first_service = True

        if (shot == "4" or shot == "5" or shot == "6" and self.first_service == True):
            # If serving from deuce side
            if (score.get_point_count_per_game() % 2 == 0):
                #print("Expanding/simulation first serve from the deuce side")
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
                #print("Expanding first serve from the ad side")
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
        
        elif (shot == "4" or shot == "5" or shot == "6" and self.first_service == False):
            # Adding Winner & Error Probas to a second serve
            if (score.get_point_count_per_game() % 2 == 0):
                #print("Expanding/simulating 2nd serve from the deuce side")
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
                #print("Expanding/Simulation 2nd serve from the ad side")
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
            
            #print("Serving (1 for bottom, 2 for top): " + str(score.get_serving_player()))
            #print("Path till expanded shot: " + str(self.expansion_path))
            #print("Shot of first serve in selected rally: " + str(self.get_shot_of_node(self.expansion_path[1])))
            #print("Shot of Leaf Node: " + str(self.get_shot_of_node(self.leaf_node)))
            
            # Are we expanding/simulation a return?
            if (parent_node_shot == "4" 
                or parent_node_shot == "5" 
                or parent_node_shot == "6"):
                #print("We are expanding a return.")
                # How to figure out if its a first or second serve??
                # Look at depth of leaf node. If it is 1 then it was a 
                # first serve and if its two it was a second serve

                if (parent_node_depth == 1):
                    #print("Depth of leaf Node: 1, so we add the return Probas for return on first serve")
                    # Depending on the direction of the first serve, we 
                    # take different Probabilities for the return
                    if (parent_node_shot == "4"):
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

                    elif(parent_node_shot == "5"):
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

                elif (parent_node_depth == 2):
                    #print("Depth of leaf Node: 2, so we add the return Probas for return on second serve")

                    if (parent_node_shot == "4"):
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

                    elif(parent_node_shot == "5"):
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
                #print("We are expanding/simulating a normal shot.")
                if (score.get_serving_player() == 1):

                    # firstly was MCTS Agent serving 2nd in the rally?
                    if (self.first_service == False):
                        #print("In a rally, where MCTS was serving a 2nd.")
                        if ("1" in parent_node_shot):
                            #print("(0) Leaf Nodes shot was in direction 1.")
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
                        elif ("2" in parent_node_shot):
                            #print("(0) 2 found in Leaf Node when leaf node was: " + str(self.get_shot_of_node(self.leaf_node)))
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
                        elif ("3" in parent_node_shot): 
                            #print("(1) 3 found in Leaf Node. When Leaf Node was: " + str(self.get_shot_of_node(self.leaf_node)))
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

                    # Was MCTS Agent serving 1st in the rally?
                    elif (self.first_service == True):
                        #print("In a rally, where MCTS was serving a 1st.")
                        if ("1" in parent_node_shot):
                            #print("1 found in Parent Node")
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
                        elif ("2" in parent_node_shot):
                            #print("2 found in Parent Node")
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
                        elif ("3" in parent_node_shot): 
                            #print("3 found in parent node")
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

                # MCTS Agent is returning
                elif (score.get_serving_player() == 2):
                    # 3rd was MCTS Agent returning 2nd in the rally?
                    # any("," in s for s in self.get_shot_of_node(self.expansion_path[1]))
                    if (self.first_service == False):
                        #print("In a rally, where MCTS was returning a 2nd.")
                        if ("1" in parent_node_shot):
                            #print("1 found in Parent Node")
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
                        elif ("2" in parent_node_shot):
                            #print("2 fount in Leaf Node")
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
                        elif ("3" in parent_node_shot): 
                            #print("3 found in parent Node.")
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

                    # 4th was MCTS Agent returning 1st in the rally?
                    else:
                        #print("In a rally, where MCTS was returning a 1st.")
                        if ("1" in parent_node_shot):
                            #print("1 found in parent Node")
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
                        elif ("2" in parent_node_shot):
                            #print("2 fount in Leaf Node")
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
                        elif ("3" in parent_node_shot): 
                            #print("3 found in Parent Node.")
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

        #print(" ----->>> Altered Shot: " + str(shot))
        if expansion == True:
            self.exp_shot_list.append(shot)
            #print("New exp_shot_list: " + str(self.exp_shot_list))
            #self.expansion_shot = shot
        else: 
            return shot
    
    def add_probs_to_2nd_serve(self, shot, score, simulation=False):
        if (shot == "4" or shot == "5" or shot == "6"):
            # Adding Winner & Error Probas to a second serve
            if (score.get_point_count_per_game() % 2 == 0):
                #print("Expanding/simulating 2nd serve from the deuce side")
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
                #print("Expanding/Simulation 2nd serve from the ad side")
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
        #print("------------>> Altered 2nd Serve encoding: " + str(shot))
        self.x = "in_play"
        self.exp_shot_list.append(shot)
        return shot

    def reset_expansion_shot(self):
        '''Resets the expansion_shot.'''
        self.expansion_shot = 0

    def get_neighbors(self, n):
        '''Returns a list of the neighbor nodes of a given node'''
        neighbor_list = self.mcts_tree.neighbors(n)
        return list(neighbor_list)

    def get_shot_of_node(self, node):
        '''Returns the shot of a given Node.'''
        shot = self.mcts_tree.nodes[node]['shot']
        return shot

    def get_next_mcts_node_index(self):
        '''Adds +1 to current node index and returns the new index'''
        self.mcts_node_index += 1
        return self.mcts_node_index

    def add_node_to_expansion_path(self, node):
        '''Adds Node to Expansion Path'''
        self.expansion_path.append(node)

    def get_depth(self, node):
        '''Returns the Depth of a given Node'''
        return self.mcts_tree.nodes[node]['depth']

    def clear_expansion_path(self):
        '''Clears all Nodes from Expansion Path'''
        self.expansion_path.clear()
        self.expansion_path = [0]

    def get_mcts_tree(self):
        return self.mcts_tree
    
    def get_shot_list_of_simu_neighbors_new(self, node):
        '''This function returns a list of shots of the neighbor nodes
        of a given node'''
        shots_of_neighbor_nodes = []
        neighbor_nodes = list(self.mcts_tree.neighbors(node))
        
        #shots_of_all_nodes = nx.get_node_attributes(self.mcts_tree, 'shot')
        
        for n in range(0, len(neighbor_nodes)):
            neighbor_shot = self.mcts_tree.nodes[neighbor_nodes[n]]['shot']
            shots_of_neighbor_nodes.append(neighbor_shot)

        return shots_of_neighbor_nodes

    def get_shot_list_of_simu_neighbors(self, node):
        '''This function returns a list of shots of the neighbor nodes
        of a given node'''
        shots_of_neighbor_nodes = []
        neighbor_nodes = list(self.mcts_tree.neighbors(node))
        shots_of_all_nodes = nx.get_node_attributes(self.mcts_tree, 'shot')
        
        for n in neighbor_nodes:
            shots_of_neighbor_nodes.append(shots_of_all_nodes[n])

        return shots_of_neighbor_nodes

    def get_shots_of_neighbors(self, node_list):
        '''Return a list of shots of a given List of nodes'''
        neighbor_shots = []
        for x in range(0, len(node_list)):
            neighbor_shot = self.mcts_tree.nodes[node_list[x]]['shot']
            neighbor_shots.append(neighbor_shot)
        return neighbor_shots
    
    def get_shot_dict_of_neighbors(self, node):
        '''This function returns a dict of shots of the neighbor nodes
        of a given node'''
        shots_of_neighbor_nodes = {}
        neighbor_nodes = list(self.mcts_tree.neighbors(node))
        shots_of_all_nodes = nx.get_node_attributes(self.mcts_tree, 'shot')
        
        for n in neighbor_nodes:
            shots_of_neighbor_nodes[n] = shots_of_all_nodes[n]

        return shots_of_neighbor_nodes
    
    def get_shot_dict_of_neighbors_new(self, node):
        '''This function returns a dict of shots of the neighbor nodes
        of a given node'''
        shots_of_neighbor_nodes = {}
        neighbor_nodes = list(self.mcts_tree.neighbors(node))
        #shots_of_all_nodes = nx.get_node_attributes(self.mcts_tree, 'shot')
        #print("Neighbor Node list: " + str(neighbor_nodes))
        for n in range(0, len(neighbor_nodes)):
            neighbor_shot = self.mcts_tree.nodes[neighbor_nodes[n]]['shot']
            shots_of_neighbor_nodes[neighbor_nodes[n]] = neighbor_shot

        return shots_of_neighbor_nodes
    
    def get_colour_dict_of_neighbors(self, node):
        '''This function returns a dict of the colours of the neighbor
        nodes of a given node'''
        colours_of_neighbor_nodes = {}
        neighbor_nodes = list(self.mcts_tree.neighbors(node))
        colour_of_all_nodes = nx.get_node_attributes(self.mcts_tree, 'colour')
        
        for i in neighbor_nodes:
            colours_of_neighbor_nodes[i] = colour_of_all_nodes[i]

        return colours_of_neighbor_nodes
    
    def get_colour_dict_of_neighbors_new(self, node):
        '''This function returns a dict of the colours of the neighbor
        nodes of a given node'''
        colours_of_neighbor_nodes = {}
        neighbor_nodes = list(self.mcts_tree.neighbors(node))
        
        for i in range(0, len(neighbor_nodes)):
            neighbor_color = self.mcts_tree.nodes[neighbor_nodes[i]]['colour']
            colours_of_neighbor_nodes[neighbor_nodes[i]] = neighbor_color

        return colours_of_neighbor_nodes

    def add_node_to_mcts_tree(self, index, colour, node_type, shot_string,
                              depth, n_visits, n_wins, uct_value,
                              point_win_rate):
        '''A new node is added to the mcts tree.'''
        self.mcts_tree.add_node(node_for_adding=index,
                           colour=colour,
                           type=node_type,
                           shot=shot_string,
                           depth=depth,
                           n_visits=n_visits,
                           n_wins=n_wins,
                           uct_value=uct_value,
                           point_win_rate=point_win_rate)
        
    def add_edge_to_mcts_tree(self, node_A, node_B, n_visits, uct_value,
                              win_count, direction):
        '''Adds a new edge between two given nodes'''
        self.mcts_tree.add_edge(node_A, node_B,
                           n_visits=n_visits,
                           uct_value=uct_value,
                           win_count=win_count,
                           direction=direction)
        
    def get_dir_of_shot_in_mcts_tree(self, node):
        '''Returns the direction of a shot of a given Node'''
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

    def copy_rally_to_mcts_rally(self, current_rally):
        '''Copys current_rally to the mcts rally'''
        for i in range(0, current_rally.get_len_rally()):
            x = current_rally.return_shot_at_pos(i)
            self.mcts_rally.add_shot_to_rally(x)

    def copy_rally_to_simu_rally(self, current_rally):
        '''Copys current_rally to the mcts rally'''
        for i in range(0, current_rally.get_len_rally()):
            x = current_rally.return_shot_at_pos(i)
            self.simulation_rally.add_shot_to_rally(x)

    def get_mcts_rally(self):
        '''Returns the MCTS rally.'''
        return self.mcts_rally

    def add_shot_to_simu_rally(self, shot):
        '''Adds a given shot to the Simulation rally'''
        self.simulation_rally.add_shot_to_rally(shot)

    def switch_simu_turns(self):
        '''Switches the turn variable from true to false and vice versa 
        for turns taken during the simulation phase'''
        if self.mcts_agents_turn == False:
            self.mcts_agents_turn = True
        elif self.mcts_agents_turn == True:
            self.mcts_agents_turn = False

    def add_shot_to_mcts_rally(self, shot):
        '''Adds a shot (Expansion shot&Simu shots) to the mcts rally'''
        self.mcts_rally.add_shot_to_rally(shot)

    def get_blue_neighbors(self, node):
        '''Returns a List of the Blue neighbor Node indexes of a given Node'''
        blue_neighbors = []
        neighbors = self.get_neighbors(node)

        for x in range(0, len(neighbors)):
            if self.mcts_tree.nodes[neighbors[x]]['colour'] == "blue":
                blue_neighbors.append(neighbors[x])

        return blue_neighbors

    def show_mcts_tree(self):
        '''When this function is called, it will draw the mcts tree.'''
        colours = list(nx.get_node_attributes(
            self.mcts_tree,'colour').values())
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