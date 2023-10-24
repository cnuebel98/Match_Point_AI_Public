
import ralley_tree

class MCTS_Agent:
    '''In this class, the MCTS Algorithm is used to find the next shot 
    in a ralley'''

    def __init__(self, name="", turn=False):
        self.name = name
        self.turn = turn

    def add_shot(self, current_ralley, score, current_tree):
        '''This function is calling the different phases of MCTS'''

        # Get the data to work with (current_tree, current_ralley,
        # score, and so on)
        #print("Ralley: " + str(current_ralley.get_ralley()))
        #print("Score: " + str(score.get_score()))
        
        ralley_tree.Ralley_Tree.show_tree(current_tree)
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
        
        # 2. Expansion phase

        shot ="123n"
        current_ralley.add_shot_to_ralley(shot)


    def get_uct_value(self, node_1, node_2):
        '''Returns the current UCT Value between two nodes'''
        ...

    

    def selection_phase(self):
        ...
    
    def expansion_phase(self):
        ...
    
    def simulation_phase(self):
        ...
    
    def backpropagation_phase(self):
        ...