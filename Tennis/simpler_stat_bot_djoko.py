import constants as const
import random
import ralley

class Simple_Stat_Bot_Djokovic:
    '''This Bot simplifies the stat_bot_djoko by not
    differentiating between different error types anymore'''
    SERVE_DIRECTION = const.ShotEncodings.SERVE_DIRECTION
    EVERY_SHOT_TYPE = const.ShotEncodings.EVERY_SHOT_TYPE
    RETURN_SHOT_TYPES = const.ShotEncodings.RETURN_SHOT_TYPES
    RETURN_DEPTH = const.ShotEncodings.RETURN_DEPTH
    DIRECTIONS = const.ShotEncodings.DIRECTIONS
    RALLEY_ERROR = const.ShotEncodings.RALLEY_ERROR
    ERROR_TYPE = const.ShotEncodings.ERROR_TYPE
    WINNER = const.ShotEncodings.WINNER
    EXTRA_STUFF = const.ShotEncodings.EXTRA_STUFF
    Returning = False
    Serving = False

    def __init__(self, name="", turn=False):
        self.name = name
        self.turn = turn

    def add_shot(self, current_ralley, score, current_tree, simulation_phase=False):
        '''Adds the most likely shot based on djokovic data'''

        # Serve from deuce side
        if (ralley.Ralley.get_len_ralley(current_ralley) == 0):
            # Adding a first serve from deuce side
            # First we need to add the direction
            i = random.randint(0, 9999)
            self.Serving = True
            self.Returning = False
            # The real probabilities are used for 1st serve from deuce side
            if (i < 4938):
                shot = "4"
                # Error and Ace Probabilities for Serve Direction 4
                j = random.randint(0, 9999)
                if (j < (1588 + 761 + 906 + 284)):
                    shot = shot + "nwdx,"
                elif (j < (1588 + 761 + 906 + 284 + 628)):
                    shot = shot + "*"
            elif (i < (4938+572)):
                shot = "5"
                # Error and Ace Probabilities for Serve Direction 5
                j = random.randint(0, 9999)
                if (j < (766 + 1626 + 19)):
                    shot = shot + "nwdx,"
                elif (j < (766 + 1626 + 19 + 19)):
                    shot = shot + "*"
            else:
                shot = "6"
                # Error and Ace Probabilities for Serve Direction 6
                j = random.randint(0, 9999)
                if (j < (1265 + 598 + 1347 + 100)):
                    shot = shot + "nwdx,"
                elif (j < (1265 + 598 + 1347 + 100 + 848)):
                    shot = shot + "*"
        
        
        elif (ralley.Ralley.get_len_ralley(current_ralley) == 1
              and current_ralley.get_last_char_of_last_shot() == ","):
            # Add Second Serve
            self.Serving = True
            self.Returning = False
            i = random.randint(0, 9999)
            if (i < 3628):
                shot = "4"
                j = random.randint(0, 9999)
                if (j < (382 + 200 + 373 + 35)):
                    shot = shot + "nwdx"
                elif (j < (382 + 200 + 373 + 35 + 43)):
                    shot = shot + "*"
            elif (i < (3628+3291)):
                shot = "5"
                j = random.randint(0, 9999)
                if (j < (220 + 258)):
                    shot = shot + "nd"
            else:
                shot = "6"
                j = random.randint(0, 9999)
                if (j < (378 + 153 + 501 + 10)):
                    shot = shot + "nwdx"
                elif (j < (378 + 153 + 501 + 10 + 174)):
                    shot = shot + "*"

        # do we return the first or the second serve (1st if statement)
        # First Serve is returned
        elif (ralley.Ralley.get_len_ralley(current_ralley) == 1):
            # Add return to the first Serve
            print("Adding return to a first serve.")
            self.Serving = False
            self.Returning = True
            x = score.get_point_count_per_game()
            if (x % 2 == 0):
                # Returning from Deuce Side of the court
                if (current_ralley.get_last_char_of_last_shot() == "4"):
                    # First serve from deuce side was direction 4
                    i = random.randint(0, 9999)
                    if (i < 3219):
                        # Direction of the shot
                        shot = "1"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2305):
                            shot = shot + "7"
                        elif (j < (2305 + 5674)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (674 + 751 + 855 + 181)):
                            shot = shot + "nwdx"
                        elif (k < (674 + 751 + 855 + 181 + 440)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 8912):
                            shot = "f" + shot
                        elif (l < (8912 + 1062)):
                            shot = "r" + shot
                        else:
                            shot = "l" + shot
                        
                    elif (i < 3219 + 5713):
                        # Direction of the shot
                        shot = "2"

                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 1520):
                            shot = shot + "7"
                        elif (j < (1520 + 5088)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (876 + 1139)):
                            shot = shot + "nwdx"
                        elif (k < (876 + 1139 + 15)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 8321):
                            shot = "f" + shot
                        elif (l < (8321 + 15)):
                            shot = "b" + shot
                        else:
                            shot = "r" + shot

                    elif (i < 3219 + 5713 + 1068):
                        # Direction of the shot
                        shot = "3"

                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 1429):
                            shot = shot + "7"
                        elif (j < (1429 + 4935)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (1172 + 1719 + 1484)):
                            shot = shot + "nwdx"
                        elif (k < (1172 + 1719 + 1484 + 313)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 8906):
                            shot = "f" + shot
                        else:
                            shot = "r" + shot

                elif (current_ralley.get_last_char_of_last_shot() == "5"):
                    # shot = "1stS return from Deuce Side on serve 5"

                    i = random.randint(0, 9999)
                    if (i < 2248):
                        # Direction of the shot
                        shot = "1"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 1915):
                            shot = shot + "7"
                        elif (j < (1915 + 5745)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (1379 + 517 + 172)):
                            shot = shot + "nwdx"
                        elif (k < (1379 + 517 + 172 + 172)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 1897):
                            shot = "f" + shot
                        elif (l < (1897 + 7241)):
                            shot = "b" + shot
                        else:
                            shot = "r" + shot

                    elif (i < (2248 + 6279)):
                        # Direction of the shot
                        shot = "2"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 1778):
                            shot = shot + "7"
                        elif (j < (1778 + 5037)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (432 + 617)):
                            shot = shot + "nwdx"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 2840):
                            shot = "f" + shot
                        elif (l < (2840 + 5864)):
                            shot = "b" + shot
                        elif (l < (2840 + 5864 + 556)):
                            shot = "s" + shot
                        else:
                            shot = "r" + shot

                    elif (i < (2248 + 6279 + 1473)):
                        # Direction of the shot
                        shot = "3"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2903):
                            shot = shot + "7"
                        elif (j < (2903 + 4194)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (1053 + 789)):
                            shot = shot + "nwdx"
                        elif (k < (1053 + 789 + 789)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 3684):
                            shot = "f" + shot
                        elif (l < (3684 + 4474)):
                            shot = "b" + shot
                        elif (l < (3684 + 4474 + 1053)):
                            shot = "s" + shot
                        else:
                            shot = "r" + shot

                elif (current_ralley.get_last_char_of_last_shot() == "6"):
                    # shot = "1stS return from Deuce Side on serve 6"
                    i = random.randint(0, 9999)
                    if (i < 1441):
                        # Direction of the shot
                        shot = "1"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2234):
                            shot = shot + "7"
                        elif (j < (2234 + 5000)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (345 + 1172 + 1241 + 276)):
                            shot = shot + "nwdx"
                        elif (k < (345 + 1172 + 1241 + 276 + 69)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 7310):
                            shot = "b" + shot
                        elif (l < (7310 + 2621)):
                            shot = "s" + shot
                        else:
                            shot = "m" + shot

                    elif (i < (1441 + 6382)):
                        # Direction of the shot
                        shot = "2"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2101):
                            shot = shot + "7"
                        elif (j < (2101 + 5021)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (654 + 857)):
                            shot = shot + "nwdx"
                        elif (k < (654 + 857 + 16)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 62):
                            shot = "f" + shot
                        elif (l < (62 + 6495)):
                            shot = "b" + shot
                        elif (l < (62 + 6495 + 3364)):
                            shot = "s" + shot
                        else:
                            shot = "m" + shot

                    elif (i < (1441 + 6382 + 2177)):
                        # Direction of the shot
                        shot = "3"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 3795):
                            shot = shot + "7"
                        elif (j < (3795 + 4819)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (822 + 594 + 457 + 46)):
                            shot = shot + "nwdx"
                        elif (k < (822 + 594 + 457 + 46 + 91)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 5342):
                            shot = "b" + shot
                        elif (l < (5342 + 4612)):
                            shot = "s" + shot
                        else:
                            shot = "m" + shot

            elif (x % 2 == 1):
                # Returning from Ad Side of the court
                if (current_ralley.get_last_char_of_last_shot() == "4"):
                    #shot = "1stS return from Ad Side on serve 4"
                    i = random.randint(0, 9999)
                    if (i < 946):
                        # Direction of the shot
                        shot = "1"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 217):
                            shot = shot + "7"
                        elif (j < (217 + 5435)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (978 + 2065 + 1957 + 109)):
                            shot = shot + "nwdx"
                        elif (k < (978 + 2065 + 1957 + 109 + 652)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 109):
                            shot = "f" + shot
                        elif (l < (109 + 7065)):
                            shot = "b" + shot
                        elif (l < (109 + 7065 + 2609)):
                            shot = "s" + shot
                        else:
                            shot = "m" + shot

                    elif (i < (946 + 4553)):
                        # Direction of the shot
                        shot = "2"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2025):
                            shot = shot + "7"
                        elif (j < (2025 + 4268)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (519 + 1196)):
                            shot = shot + "nwdx"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 135):
                            shot = "f" + shot
                        elif (l < (135 + 6885)):
                            shot = "b" + shot
                        elif (l < (135 + 6885 + 2822)):
                            shot = "s" + shot
                        else:
                            shot = "m" + shot

                    elif (i < (946 + 4553 + 4502)):
                        # Direction of the shot
                        shot = "3"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 3275):
                            shot = shot + "7"
                        elif (j < (3275 + 5117)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (799 + 639 + 411 + 23)):
                            shot = shot + "nwdx"
                        elif (k < (799 + 639 + 411 + 23 + 46)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 23):
                            shot = "f" + shot
                        elif (l < (23 + 7922)):
                            shot = "b" + shot
                        elif (l < (23 + 7922 + 2009)):
                            shot = "s" + shot
                        else:
                            shot = "m" + shot


                elif (current_ralley.get_last_char_of_last_shot() == "5"):
                    # shot = "1stS return from Ad Side on serve 5"

                    i = random.randint(0, 9999)
                    if (i < 1215):
                        # Direction of the shot
                        shot = "1"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 3043):
                            shot = shot + "7"
                        elif (j < (3043 + 3043)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (1000 + 333 + 333)):
                            shot = shot + "nwdx"
                        elif (k < (1000 + 333 + 333 + 667)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 4667):
                            shot = "f" + shot
                        elif (l < (4667 + 3000)):
                            shot = "b" + shot
                        elif (l < (4667 + 3000 + 667)):
                            shot = "s" + shot
                        else:
                            shot = "r" + shot

                    elif (i < (1215 + 5911)):
                        # Direction of the shot
                        shot = "2"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 1667):
                            shot = shot + "7"
                        elif (j < (1667 + 5351)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (548 + 1027)):
                            shot = shot + "nwdx"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 4247):
                            shot = "f" + shot
                        elif (l < (4247 + 4110)):
                            shot = "b" + shot
                        elif (l < (4247 + 4110 + 274)):
                            shot = "s" + shot
                        else:
                            shot = "r" + shot

                    elif (i < (1215 + 5911 + 2874)):
                        # Direction of the shot
                        shot = "3"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2333):
                            shot = shot + "7"
                        elif (j < (2333 + 5000)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (423 + 845 + 423 + 141)):
                            shot = shot + "nwdx"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 4366):
                            shot = "f" + shot
                        elif (l < (4366 + 4789)):
                            shot = "b" + shot
                        elif (l < (4366 + 4789 + 423)):
                            shot = "s" + shot
                        elif (l < (4366 + 4789 + 423 + 282)):
                            shot = "r" + shot
                        else:
                            shot = "m" + shot

                elif (current_ralley.get_last_char_of_last_shot() == "6"):
                    # shot = "1stS return from Ad Side on serve 6"
                    i = random.randint(0, 9999)
                    if (i < 1292):
                        # Direction of the shot
                        shot = "1"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 4302):
                            shot = shot + "7"
                        elif (j < (4302 + 4302)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (1016 + 1094 + 781 + 78)):
                            shot = shot + "nwdx"
                        elif (k < (1016 + 1094 + 781 + 78 + 391)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 8516):
                            shot = "f" + shot
                        elif (l < (8516 + 78)):
                            shot = "b" + shot
                        else:
                            shot = "r" + shot

                    elif (i < (1292 + 5964)):
                        # Direction of the shot
                        shot = "2"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2551):
                            shot = shot + "7"
                        elif (j < (2551 + 4831)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (711 + 1015)):
                            shot = shot + "nwdx"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 7766):
                            shot = "f" + shot
                        elif (l < (7766 + 34)):
                            shot = "b" + shot
                        elif (l < (7766 + 34 + 2081)):
                            shot = "r" + shot
                        elif (l < (7766 + 34 + 2081 + 34)):
                            shot = "s" + shot
                        else:
                            shot = "l" + shot

                    elif (i < (1292 + 5964 + 2745)):
                        # Direction of the shot
                        shot = "3"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 3128):
                            shot = shot + "7"
                        elif (j < (3128 + 4667)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (662 + 993 + 588 + 404)):
                            shot = shot + "nwdx"
                        elif (k < (662 + 993 + 588 + 404 + 37)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 8493):
                            shot = "f" + shot
                        elif (l < (8493 + 37)):
                            shot = "b" + shot
                        elif (l < (8493 + 37 + 1397)):
                            shot = "r" + shot
                        else:
                            shot = "s" + shot

        elif (ralley.Ralley.get_len_ralley(current_ralley) == 2
              and "," in 
              ralley.Ralley.get_first_shot_of_ralley(current_ralley)):
            # Add return to the Second Serve
            print("Adding return to a second serve.")
            # shot = "SecondServeReturn"
            self.Serving = False
            self.Returning = True
            x = score.get_point_count_per_game()
            if (x % 2 == 0): 
                # Returning from Deuce Side of the court
                if (current_ralley.get_last_char_of_last_shot() == "4"):
                    #print("2ndS return from Deuce Side on serve 4")

                    i = random.randint(0, 9999)
                    if (i < 2271):
                        # Direction of the shot
                        shot = "1"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2667):
                            shot = shot + "7"
                        elif (j < (2667 + 6667)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (1053 + 351 + 526)):
                            shot = shot + "nwdx"
                        elif (k < (1053 + 351 + 526 + 351)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 10000):
                            shot = "f" + shot

                    elif (i < (2271 + 5657)):
                        # Direction of the shot
                        shot = "2"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 1441):
                            shot = shot + "7"
                        elif (j < (1441 + 5315)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (634 + 1127)):
                            shot = shot + "nwdx"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 9789):
                            shot = "f" + shot
                        elif (l < (9789 + 7)):
                            shot = "b" + shot
                        else:
                            shot = "r" + shot

                    elif (i < (2271 + 5657 + 2072)):
                        # Direction of the shot
                        shot = "3"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 571):
                            shot = shot + "7"
                        elif (j < (571 + 7143)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (1154 + 1154 + 962)):
                            shot = shot + "nwdx"
                        elif (k < (1154 + 1154 + 962 + 1538)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 10000):
                            shot = "f" + shot

                elif (current_ralley.get_last_char_of_last_shot() == "5"):
                    #print("2ndS return from Deuce Side on serve 5")

                    i = random.randint(0, 9999)
                    if (i < 1621):
                        # Direction of the shot
                        shot = "1"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 1961):
                            shot = shot + "7"
                        elif (j < (1961 + 5490)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (763 + 593)):
                            shot = shot + "nwdx"
                        elif (k < (763 + 593 + 339)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 4746):
                            shot = "f" + shot
                        elif (l < (4746 + 5169)):
                            shot = "b" + shot
                        else:
                            shot = "r" + shot

                    elif (i < (1621 + 6277)):
                        # Direction of the shot
                        shot = "2"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 1450):
                            shot = shot + "7"
                        elif (j < (1450 + 5776)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (263 + 547)):
                            shot = shot + "nwdx"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 3982):
                            shot = "f" + shot
                        elif (l < (3982 + 5864)):
                            shot = "b" + shot
                        elif (l < (3982 + 5864 + 88)):
                            shot = "r" + shot
                        else:
                            shot = "s" + shot

                    elif (i < (1621 + 6277 + 2102)):
                        # Direction of the shot
                        shot = "3"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2143):
                            shot = shot + "7"
                        elif (j < (2143 + 6190)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (458 + 458 + 654 + 65)):
                            shot = shot + "nwdx"
                        elif (k < (458 + 458 + 654 + 65 + 327)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 3660):
                            shot = "f" + shot
                        elif (l < (3660 + 6144)):
                            shot = "b" + shot
                        else:
                            shot = "r" + shot

                elif (current_ralley.get_last_char_of_last_shot() == "6"):
                    #print("2ndS return from Deuce Side on serve 6")

                    i = random.randint(0, 9999)
                    if (i < 976):
                        # Direction of the shot
                        shot = "1"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 625):
                            shot = shot + "7"
                        elif (j < (625 + 5313)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (612 + 1020 + 408)):
                            shot = shot + "nwdx"
                        elif (k < (612 + 1020 + 408 + 204)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 1020):
                            shot = "f" + shot
                        elif (l < (1020 + 8776)):
                            shot = "b" + shot
                        else:
                            shot = "s" + shot

                    elif (i < (976 + 6155)):
                        # Direction of the shot
                        shot = "2"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 1311):
                            shot = shot + "7"
                        elif (j < (1311 + 5820)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (194 + 647)):
                            shot = shot + "nwdx"
                        elif (k < (194 + 647 + 32)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 291):
                            shot = "f" + shot
                        elif (l < (291 + 9256)):
                            shot = "b" + shot
                        elif (l < (291 + 9256 + 421)):
                            shot = "s" + shot
                        else:
                            shot = "m" + shot

                    elif (i < (976 + 6155 + 2869)):
                        # Direction of the shot
                        shot = "3"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2143):
                            shot = shot + "7"
                        elif (j < (2143 + 5089)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (764 + 347 + 486 + 69)):
                            shot = shot + "nwdx"
                        elif (k < (764 + 347 + 486 + 69 + 69)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 139):
                            shot = "f" + shot
                        elif (l < (139 + 9375)):
                            shot = "b" + shot
                        else:
                            shot = "s" + shot

            elif (x % 2 == 1):
                # Returning from Ad Side of the court
                if (current_ralley.get_last_char_of_last_shot() == "4"):
                    #print("2ndS return from Ad Side on serve 4")

                    i = random.randint(0, 9999)
                    if (i < 399):
                        # Direction of the shot
                        shot = "1"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2857):
                            shot = shot + "7"
                        elif (j < (2857 + 5000)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (2500 + 1250 + 417)):
                            shot = shot + "nwdx"
                        elif (k < (2500 + 1250 + 417 + 833)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 1250):
                            shot = "f" + shot
                        elif (l < (1250 + 5333)):
                            shot = "b" + shot
                        else:
                            shot = "s" + shot

                    elif (i < (399 + 2795)):
                        # Direction of the shot
                        shot = "2"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 902):
                            shot = shot + "7"
                        elif (j < (902 + 5984)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (357 + 774)):
                            shot = shot + "nwdx"
                        
                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 119):
                            shot = "f" + shot
                        elif (l < (119 + 9702)):
                            shot = "b" + shot
                        else:
                            shot = "s" + shot

                    elif (i < (399 + 2795 + 6805)):
                        # Direction of the shot
                        shot = "3"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2458):
                            shot = shot + "7"
                        elif (j < (2458 + 5810)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (244 + 318 + 318 + 122)):
                            shot = shot + "nwdx"
                        elif (k < (244 + 318 + 318 + 122 + 82)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 196):
                            shot = "f" + shot
                        elif (l < (196 + 9756)):
                            shot = "b" + shot
                        else:
                            shot = "s" + shot

                elif (current_ralley.get_last_char_of_last_shot() == "5"):
                    #print("2ndS return from Ad Side on serve 5")

                    i = random.randint(0, 9999)
                    if (i < 685):
                        # Direction of the shot
                        shot = "1"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 5357):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (513 + 1026 + 513 + 513)):
                            shot = shot + "nwdx"
                        elif (k < (513 + 1026 + 513 + 513 + 2821)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 5641):
                            shot = "f" + shot
                        else:
                            shot = "b" + shot

                    elif (i < (685 + 3989)):
                        # Direction of the shot
                        shot = "2"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 1295):
                            shot = shot + "7"
                        elif (j < (1295 + 5026)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (264 + 617)):
                            shot = shot + "nwdx"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 3480):
                            shot = "f" + shot
                        elif (l < (3480 + 6432)):
                            shot = "b" + shot
                        elif (l < (3480 + 6432 + 44)):
                            shot = "s" + shot
                        else:
                            shot = "r" + shot

                    elif (i < (685 + 3989 + 5325)):
                        # Direction of the shot
                        shot = "3"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2030):
                            shot = shot + "7"
                        elif (j < (2030 + 5639)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (363 + 297 + 396 + 33)):
                            shot = shot + "nwdx"
                        elif (k < (363 + 297 + 396 + 33 + 66)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 3102):
                            shot = "f" + shot
                        elif (l < (3102 + 6832)):
                            shot = "b" + shot
                        elif (l < (3102 + 6832 + 33)):
                            shot = "s" + shot
                        else:
                            shot = "r" + shot

                elif (current_ralley.get_last_char_of_last_shot() == "6"):
                    #print("2ndS return from Ad Side on serve 6")

                    i = random.randint(0, 9999)
                    if (i < 1288):
                        # Direction of the shot
                        shot = "1"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 833):
                            shot = shot + "7"
                        elif (j < (833 + 7083)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (588 + 1471 + 588 + 294)):
                            shot = shot + "nwdx"
                        elif (k < (588 + 1471 + 588 + 294 + 1765)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 10000):
                            shot = "f" + shot

                    elif (i < (1288 + 5644)):
                        # Direction of the shot
                        shot = "2"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 1754):
                            shot = shot + "7"
                        elif (j < (1754 + 5439)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (604 + 872)):
                            shot = shot + "nwdx"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 9866):
                            shot = "f" + shot
                        else:
                            shot = "r" + shot

                    elif (i < (1288 + 5644 + 3068)):
                        # Direction of the shot
                        shot = "3"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2429):
                            shot = shot + "7"
                        elif (j < (2429 + 5571)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (617 + 494 + 988 + 123)):
                            shot = shot + "nwdx"
                        elif (k < (617 + 494 + 988 + 123 + 123)):
                            shot = shot + "*"

                        # Here the Shot type is added
                        l = random.randint(0, 9999)
                        if (l < 9753):
                            shot = "f" + shot
                        elif (l < (9753 + 123)):
                            shot = "b" + shot
                        else:
                            shot = "s" + shot

        else:
            # We need to seperate between serving and returning in the
            # ralley and also between first and second serves

            # If Djoko was starting the ralley with a first serve
            if(ralley.Ralley.get_len_ralley(current_ralley) % 2 == 1
                and self.Serving == True
                and "," in 
                ralley.Ralley.get_first_shot_of_ralley(current_ralley)):
                #print("Djoko was opening the ralley with a second serve")

                # If Opponents last shot was dir 1
                if "1" in current_ralley.get_last_shot():
                    #print("Opponents last shot was in dir 1")
                    # probabilities for Djokos Shot are added
                    
                    i = random.randint(0, 9999)
                    if (i < 4184):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 2542):
                            shot = shot + "7"
                        elif (j < (2542 + 4661)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (494 + 426 + 170 + 34)):
                            shot = shot + "nwdx"
                        elif (k < (494 + 426 + 170 + 34 + 613)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 9114):
                            shot = "f" + shot
                        elif (l < (9114 + 426)):
                            shot = "r" + shot
                        elif (l < (9114 + 426 + 17)):
                            shot = "s" + shot
                        elif (l < (9114 + 426 + 17 + 153)):
                            shot = "v" + shot
                        elif (l < (9114 + 426 + 17 + 153 + 68)):
                            shot = "o" + shot
                        elif (l < (9114 + 426 + 17 + 153 + 68 + 68)):
                            shot = "u" + shot
                        elif (l < (9114 + 426 + 17 + 153 + 68 + 68 + 68)):
                            shot = "l" + shot
                        elif (l < (9114 + 426 + 17 + 153 + 68 + 68 + 68 + 51)):
                            shot = "h" + shot
                        elif (l < (9114 + 426 + 17 + 153 + 68 + 68 + 68 + 51 
                                   + 17)):
                            shot = "j" + shot
                        elif (l < (9114 + 426 + 17 + 153 + 68 + 68 + 68 + 51 
                                   + 17 + 17)):
                            shot = "t" + shot

                    elif (i < (4184 + 2730)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1607):
                            shot = shot + "7"
                        elif (j < (1607 + 4643)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (574 + 444)):
                            shot = shot + "nwdx"
                        elif (k < (574 + 444 + 235)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 7911):
                            shot = "f" + shot
                        elif (l < (7911 + 26)):
                            shot = "b" + shot
                        elif (l < (7911 + 26 + 1227)):
                            shot = "r" + shot
                        elif (l < (7911 + 26 + 1227 + 235)):
                            shot = "v" + shot
                        elif (l < (7911 + 26 + 1227 + 235 + 78)):
                            shot = "o" + shot
                        elif (l < (7911 + 26 + 1227 + 235 + 78 + 78)):
                            shot = "u" + shot
                        elif (l < (7911 + 26 + 1227 + 235 + 78 + 78 + 392)):
                            shot = "l" + shot
                        elif (l < (7911 + 26 + 1227 + 235 + 78 + 78 + 392 
                                   + 52)):
                            shot = "h" + shot

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 563):
                            shot = shot + "7"
                        elif (j < (563 + 5915)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (577 + 577 + 485 + 69)):
                            shot = shot + "nwdx"
                        elif (k < (577 + 577 + 485 + 69 + 739)):
                            shot = shot + "*"
                        # Shot Type is added

                        l = random.randint(0, 9999)
                        if (l < 9215):
                            shot = "f" + shot
                        elif (l < (9215 + 92)):
                            shot = "b" + shot
                        elif (l < (9215 + 92 + 323)):
                            shot = "r" + shot
                        elif (l < (9215 + 92 + 323 + 46)):
                            shot = "s" + shot
                        elif (l < (9215 + 92 + 323 + 46 + 69)):
                            shot = "v" + shot
                        elif (l < (9215 + 92 + 323 + 46 + 69 + 46)):
                            shot = "o" + shot
                        elif (l < (9215 + 92 + 323 + 46 + 69 + 46 + 115)):
                            shot = "u" + shot
                        elif (l < (9215 + 92 + 323 + 46 + 69 + 46 + 115 + 46)):
                            shot = "l" + shot
                        elif (l < (9215 + 92 + 323 + 46 + 69 + 46 + 115 + 46 
                                   + 23)):
                            shot = "h" + shot
                        elif (l < (9215 + 92 + 323 + 46 + 69 + 46 + 115 + 46 
                                   + 23 + 23)):
                            shot = "j" + shot

                # ElIf Opponents last shot was dir 2
                elif "2" in current_ralley.get_last_shot():
                    #print("Opponents last shot was in dir 2")
                    # probabilities for Djokos Shot are added
                    
                    i = random.randint(0, 9999)
                    if (i < 2931):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1533):
                            shot = shot + "7"
                        elif (j < (1533 + 5733)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (475 + 356 + 211 + 53)):
                            shot = shot + "nwdx"
                        elif (k < (475 + 356 + 211 + 53 + 897)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 6979):
                            shot = "f" + shot
                        elif (l < (6979 + 2137)):
                            shot = "b" + shot
                        elif (l < (6979 + 2137 + 13)):
                            shot = "r" + shot
                        elif (l < (6979 + 2137 + 13 + 106)):
                            shot = "s" + shot
                        elif (l < (6979 + 2137 + 13 + 106 + 158)):
                            shot = "v" + shot
                        elif (l < (6979 + 2137 + 13 + 106 + 158 + 132)):
                            shot = "z" + shot
                        elif (l < (6979 + 2137 + 13 + 106 + 158 + 132 + 92)):
                            shot = "o" + shot
                        elif (l < (6979 + 2137 + 13 + 106 + 158 + 132 + 92 
                                   + 40)):
                            shot = "u" + shot
                        elif (l < (6979 + 2137 + 13 + 106 + 158 + 132 + 92 
                                   + 40 + 290)):
                            shot = "y" + shot
                        elif (l < (6979 + 2137 + 13 + 106 + 158 + 132 + 92 
                                   + 40 + 290 + 13)):
                            shot = "m" + shot
                        elif (l < (6979 + 2137 + 13 + 106 + 158 + 132 + 92 
                                   + 40 + 290 + 13 + 26)):
                            shot = "i" + shot
                        elif (l < (6979 + 2137 + 13 + 106 + 158 + 132 + 92 
                                   + 40 + 290 + 13 + 26 + 13)):
                            shot = "j" + shot

                    elif (i < (2931 + 2838)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1466):
                            shot = shot + "7"
                        elif (j < (1466 + 4914)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (286 + 463)):
                            shot = shot + "nwdx"
                        elif (k < (286 + 463 + 27)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 4605):
                            shot = "f" + shot
                        elif (l < (4605 + 4659)):
                            shot = "b" + shot
                        elif (l < (4605 + 4659 + 41)):
                            shot = "r" + shot
                        elif (l < (4605 + 4659 + 41 + 531)):
                            shot = "s" + shot
                        elif (l < (4605 + 4659 + 41 + 531 + 41)):
                            shot = "z" + shot
                        elif (l < (4605 + 4659 + 41 + 531 + 41 + 68)):
                            shot = "o" + shot
                        elif (l < (4605 + 4659 + 41 + 531 + 41 + 68 + 14)):
                            shot = "y" + shot
                        elif (l < (4605 + 4659 + 41 + 531 + 41 + 68 + 14 
                                   + 14)):
                            shot = "l" + shot
                        elif (l < (4605 + 4659 + 41 + 531 + 41 + 68 + 14 
                                   + 14 + 14)):
                            shot = "i" + shot
                        elif (l < (4605 + 4659 + 41 + 531 + 41 + 68 + 14 
                                   + 14 + 14 + 14)):
                            shot = "j" + shot

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1065):
                            shot = shot + "7"
                        elif (j < (1065 + 4907)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (320 + 448 + 302 + 18)):
                            shot = shot + "nwdx"
                        elif (k < (320 + 448 + 302 + 18 + 612)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 5238):
                            shot = "f" + shot
                        elif (l < (5238 + 3912)):
                            shot = "b" + shot
                        elif (l < (5238 + 3912 + 18)):
                            shot = "r" + shot
                        elif (l < (5238 + 3912 + 18 + 503)):
                            shot = "s" + shot
                        elif (l < (5238 + 3912 + 18 + 503 + 55)):
                            shot = "v" + shot
                        elif (l < (5238 + 3912 + 18 + 503 + 55 + 73)):
                            shot = "z" + shot
                        elif (l < (5238 + 3912 + 18 + 503 + 55 + 73 + 91)):
                            shot = "o" + shot
                        elif (l < (5238 + 3912 + 18 + 503 + 55 + 73 + 91 
                                   + 18)):
                            shot = "u" + shot
                        elif (l < (5238 + 3912 + 18 + 503 + 55 + 73 + 91 
                                   + 18 + 46)):
                            shot = "y" + shot
                        elif (l < (5238 + 3912 + 18 + 503 + 55 + 73 + 91 
                                   + 18 + 46 + 9)):
                            shot = "l" + shot
                        elif (l < (5238 + 3912 + 18 + 503 + 55 + 73 + 91 
                                   + 18 + 46 + 9 + 9)):
                            shot = "h" + shot
                        elif (l < (5238 + 3912 + 18 + 503 + 55 + 73 + 91 
                                   + 18 + 46 + 9 + 9 + 27)):
                            shot = "j" + shot

                # ElIf Opponents last shot was dir 3
                elif "3" in current_ralley.get_last_shot():
                    #print("Opponents last shot was in dir 3")
                    # probabilities for Djokos Shot are added
                    
                    i = random.randint(0, 9999)
                    if (i < 2317):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1373):
                            shot = shot + "7"
                        elif (j < (1373 + 4314)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabilities are added
                        k = random.randint(0, 9999)
                        if (k < (656 + 480 + 496 + 96)):
                            shot = shot + "nwdx"
                        elif (k < (656 + 480 + 496 + 96 + 1328)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 1792):
                            shot = "f" + shot
                        elif (l < (1792 + 6400)):
                            shot = "b" + shot
                        elif (l < (1792 + 6400 + 608)):
                            shot = "s" + shot
                        elif (l < (1792 + 6400 + 608 + 272)):
                            shot = "z" + shot
                        elif (l < (1792 + 6400 + 608 + 272 + 768)):
                            shot = "y" + shot
                        elif (l < (1792 + 6400 + 608 + 272 + 768 + 112)):
                            shot = "m" + shot
                        elif (l < (1792 + 6400 + 608 + 272 + 768 + 112 + 32)):
                            shot = "i" + shot
                        elif (l < (1792 + 6400 + 608 + 272 + 768 + 112 + 32 
                                   + 16)):
                            shot = "t" + shot

                    elif (i < (2317 + 2309)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 561):
                            shot = shot + "7"
                        elif (j < (561 + 4486)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (369 + 401)):
                            shot = shot + "nwdx"
                        elif (k < (369 + 401 + 32)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 385):
                            shot = "f" + shot
                        elif (l < (385 + 8010)):
                            shot = "b" + shot
                        elif (l < (385 + 8010 + 16)):
                            shot = "r" + shot
                        elif (l < (385 + 8010 + 16 + 1059)):
                            shot = "s" + shot
                        elif (l < (385 + 8010 + 16 + 1059 + 112)):
                            shot = "z" + shot
                        elif (l < (385 + 8010 + 16 + 1059 + 112 + 16)):
                            shot = "o" + shot
                        elif (l < (385 + 8010 + 16 + 1059 + 112 + 16 + 80)):
                            shot = "y" + shot
                        elif (l < (385 + 8010 + 16 + 1059 + 112 + 16 + 80 
                                   + 16)):
                            shot = "l" + shot
                        elif (l < (385 + 8010 + 16 + 1059 + 112 + 16 + 80 
                                   + 16 + 289)):
                            shot = "m" + shot
                        elif (l < (385 + 8010 + 16 + 1059 + 112 + 16 + 80 
                                   + 16 + 289 + 16)):
                            shot = "i" + shot

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1476):
                            shot = shot + "7"
                        elif (j < (1476 + 5000)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (372 + 269 + 193 + 21)):
                            shot = shot + "nwdx"
                        elif (k < (372 + 269 + 193 + 21 + 276)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 772):
                            shot = "f" + shot
                        elif (l < (772 + 7703)):
                            shot = "b" + shot
                        elif (l < (772 + 7703 + 1069)):
                            shot = "s" + shot
                        elif (l < (772 + 7703 + 1069 + 124)):
                            shot = "z" + shot
                        elif (l < (772 + 7703 + 1069 + 124 + 41)):
                            shot = "o" + shot
                        elif (l < (772 + 7703 + 1069 + 124 + 41 + 14)):
                            shot = "u" + shot
                        elif (l < (772 + 7703 + 1069 + 124 + 41 + 14 + 172)):
                            shot = "y" + shot
                        elif (l < (772 + 7703 + 1069 + 124 + 41 + 14 + 172 
                                   + 90)):
                            shot = "m" + shot
                        elif (l < (772 + 7703 + 1069 + 124 + 41 + 14 + 172 
                                   + 90 + 14)):
                            shot = "i" + shot
  
            # ElIf Djoko started Ralley with a first Serve
            elif(ralley.Ralley.get_len_ralley(current_ralley) % 2 == 0
                and self.Serving == True):
                #print("Djoko was opening the ralley with a first serve")        
                
                # If Opponents last shot was dir 1
                if "1" in current_ralley.get_last_shot():
                    #print("Opponents last shot was in dir 1")
                    # probabilities for Djokos Shot are added
                    i = random.randint(0, 9999)
                    if (i < 3943):
                        shot = "1"

                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 3023):
                            shot = shot + "7"
                        elif (j < (3023 + 4651)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (461 + 476 + 353)):
                            shot = shot + "nwdx"
                        elif (k < (461 + 476 + 353 + 1229)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 8694):
                            shot = "f" + shot
                        elif (l < (8694 + 15)):
                            shot = "b" + shot
                        elif (l < (8694 + 15 + 399)):
                            shot = "r" + shot
                        elif (l < (8694 + 15 + 399 + 384)):
                            shot = "v" + shot
                        elif (l < (8694 + 15 + 399 + 384 + 200)):
                            shot = "o" + shot
                        elif (l < (8694 + 15 + 399 + 384 + 200 + 123)):
                            shot = "u" + shot
                        elif (l < (8694 + 15 + 399 + 384 + 200 + 123 + 108)):
                            shot = "l" + shot
                        elif (l < (8694 + 15 + 399 + 384 + 200 + 123 + 108 
                              + 31)):
                            shot = "h" + shot
                        elif (l < (8694 + 15 + 399 + 384 + 200 + 123 + 108 
                              + 31 + 46)):
                            shot = "j" + shot

                    elif (i < (3943 + 2550)):
                        shot = "2"

                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 2000):
                            shot = shot + "7"
                        elif (j < (2000 + 4353)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (475 + 285)):
                            shot = shot + "nwdx"
                        elif (k < (475 + 285 + 238)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 8100):
                            shot = "f" + shot
                        elif (l < (8100 + 1188)):
                            shot = "r" + shot
                        elif (l < (8100 + 1188 + 261)):
                            shot = "v" + shot
                        elif (l < (8100 + 1188 + 261 + 119)):
                            shot = "o" + shot
                        elif (l < (8100 + 1188 + 261 + 119 + 95)):
                            shot = "u" + shot
                        elif (l < (8100 + 1188 + 261 + 119 + 95 + 190)):
                            shot = "l" + shot
                        elif (l < (8100 + 1188 + 261 + 119 + 95 + 190 + 48)):
                            shot = "h" + shot

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)

                        # Shot length is added
                        if (j < 1238):
                            shot = shot + "7"
                        elif (j < (1238 + 4381)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (553 + 397 + 535 + 17)):
                            shot = shot + "nwdx"
                        elif (k < (553 + 397 + 535 + 17 + 1192)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 8653):
                            shot = "f" + shot
                        elif (l < (8653 + 17)):
                            shot = "b" + shot
                        elif (l < (8653 + 17 + 363)):
                            shot = "r" + shot
                        elif (l < (8653 + 17 + 363 + 17)):
                            shot = "s" + shot
                        elif (l < (8653 + 17 + 363 + 17 + 604)):
                            shot = "v" + shot
                        elif (l < (8653 + 17 + 363 + 17 + 604 + 35)):
                            shot = "z" + shot
                        elif (l < (8653 + 17 + 363 + 17 + 604 + 35 + 69)):
                            shot = "o" + shot
                        elif (l < (8653 + 17 + 363 + 17 + 604 + 35 + 69 
                                   + 121)):
                            shot = "u" + shot
                        elif (l < (8653 + 17 + 363 + 17 + 604 + 35 + 69 + 121 
                                   + 35)):
                            shot = "l" + shot
                        elif (l < (8653 + 17 + 363 + 17 + 604 + 35 + 69 + 121 
                                   + 35 + 52)):
                            shot = "h" + shot
                        elif (l < (8653 + 17 + 363 + 17 + 604 + 35 + 69 + 121 
                                   + 35 + 52 + 17)):
                            shot = "i" + shot
                        elif (l < (8653 + 17 + 363 + 17 + 604 + 35 + 69 + 121 
                                   + 35 + 52 + 17 + 17)):
                            shot = "j" + shot

                # ElIf Opponents last shot was dir 2
                elif "2" in current_ralley.get_last_shot():
                    #print("Opponents last shot was in dir 2")
                    # probabilities for Djokos Shot are added

                    i = random.randint(0, 9999)
                    if (i < 3726):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 2383):
                            shot = shot + "7"
                        elif (j < (2383 + 4799)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (395 + 312 + 146 + 7)):
                            shot = shot + "nwdx"
                        elif (k < (395 + 312 + 146 + 7 + 1775)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 7524):
                            shot = "f" + shot
                        elif (l < (7524 + 1103)):
                            shot = "b" + shot
                        elif (l < (7524 + 1103 + 28)):
                            shot = "r" + shot
                        elif (l < (7524 + 1103 + 28 + 76)):
                            shot = "s" + shot
                        elif (l < (7524 + 1103 + 28 + 76 + 250)):
                            shot = "v" + shot
                        elif (l < (7524 + 1103 + 28 + 76 + 250 + 139)):
                            shot = "z" + shot
                        elif (l < (7524 + 1103 + 28 + 76 + 250 + 139 + 312)):
                            shot = "o" + shot
                        elif (l < (7524 + 1103 + 28 + 76 + 250 + 139 + 312 
                                   + 7)):
                            shot = "p" + shot
                        elif (l < (7524 + 1103 + 28 + 76 + 250 + 139 + 312 
                                   + 7 + 69)):
                            shot = "u" + shot
                        elif (l < (7524 + 1103 + 28 + 76 + 250 + 139 + 312 
                                   + 7 + 69 + 347)):
                            shot = "y" + shot
                        elif (l < (7524 + 1103 + 28 + 76 + 250 + 139 + 312 
                                   + 7 + 69 + 347 + 21)):
                            shot = "h" + shot
                        elif (l < (7524 + 1103 + 28 + 76 + 250 + 139 + 312 
                                   + 7 + 69 + 347 + 21 + 118)):
                            shot = "j" + shot
                        elif (l < (7524 + 1103 + 28 + 76 + 250 + 139 + 312 
                                   + 7 + 69 + 347 + 21 + 118 + 7)):
                            shot = "k" + shot

                    elif (i < (3726 + 2021)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1420):
                            shot = shot + "7"
                        elif (j < (1420 + 4438)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"
                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (384 + 256)):
                            shot = shot + "nwdx"
                        elif (k < (384 + 256 + 192)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 5243):
                            shot = "f" + shot
                        elif (l < (5243 + 3760)):
                            shot = "b" + shot
                        elif (l < (5243 + 3760 + 38)):
                            shot = "r" + shot
                        elif (l < (5243 + 3760 + 38 + 345)):
                            shot = "s" + shot
                        elif (l < (5243 + 3760 + 38 + 345 + 141)):
                            shot = "v" + shot
                        elif (l < (5243 + 3760 + 38 + 345 + 141 + 77)):
                            shot = "z" + shot
                        elif (l < (5243 + 3760 + 38 + 345 + 141 + 77 + 23)):
                            shot = "o" + shot
                        elif (l < (5243 + 3760 + 38 + 345 + 141 + 77 + 23 
                                   + 26)):
                            shot = "y" + shot
                        elif (l < (5243 + 3760 + 38 + 345 + 141 + 77 + 23 
                                   + 26 + 26)):
                            shot = "l" + shot
                        elif (l < (5243 + 3760 + 38 + 345 + 141 + 77 + 23 
                                   + 26 + 26 + 13)):
                            shot = "m" + shot
                        elif (l < (5243 + 3760 + 38 + 345 + 141 + 77 + 23 
                                   + 26 + 26 + 13 + 13)):
                            shot = "h" + shot
                        elif (l < (5243 + 3760 + 38 + 345 + 141 + 77 + 23 
                                   + 26 + 26 + 13 + 13 + 38)):
                            shot = "i" + shot
                        elif (l < (5243 + 3760 + 38 + 345 + 141 + 77 + 23 
                                   + 26 + 26 + 13 + 13 + 38 + 51)):
                            shot = "j" + shot

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1138):
                            shot = shot + "7"
                        elif (j < (1138 + 5103)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (273 + 292 + 213 + 43)):
                            shot = shot + "nwdx"
                        elif (k < (273 + 292 + 213 + 43 + 996)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 6464):
                            shot = "f" + shot
                        elif (l < (6464 + 2509)):
                            shot = "b" + shot
                        elif (l < (6464 + 2509 + 18)):
                            shot = "r" + shot
                        elif (l < (6464 + 2509 + 18 + 346)):
                            shot = "s" + shot
                        elif (l < (6464 + 2509 + 18 + 346 + 122)):
                            shot = "v" + shot
                        elif (l < (6464 + 2509 + 18 + 346 + 122 + 176)):
                            shot = "z" + shot
                        elif (l < (6464 + 2509 + 18 + 346 + 122 + 176 + 176)):
                            shot = "o" + shot
                        elif (l < (6464 + 2509 + 18 + 346 + 122 + 176 + 176 
                                   + 30)):
                            shot = "u" + shot
                        elif (l < (6464 + 2509 + 18 + 346 + 122 + 176 + 176 
                                   + 30 + 24)):
                            shot = "y" + shot
                        elif (l < (6464 + 2509 + 18 + 346 + 122 + 176 + 176 
                                   + 30 + 24 + 6)):
                            shot = "m" + shot
                        elif (l < (6464 + 2509 + 18 + 346 + 122 + 176 + 176 
                                   + 30 + 24 + 6 + 18)):
                            shot = "h" + shot
                        elif (l < (6464 + 2509 + 18 + 346 + 122 + 176 + 176 
                                   + 30 + 24 + 6 + 18 + 6)):
                            shot = "i" + shot
                        elif (l < (6464 + 2509 + 18 + 346 + 122 + 176 + 176 
                                   + 30 + 24 + 6 + 18 + 6 + 103)):
                            shot = "j" + shot

                # ElIf Opponents last shot was dir 3
                elif "3" in current_ralley.get_last_shot():
                    #print("Opponents last shot was in dir 3")
                    # probabilities for Djokos Shot are added
                    
                    i = random.randint(0, 9999)
                    if (i < 3065):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 2748):
                            shot = shot + "7"
                        elif (j < (2748 + 3664)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (835 + 503 + 396 + 43)):
                            shot = shot + "nwdx"
                        elif (k < (835 + 503 + 396 + 43 + 1713)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 2398):
                            shot = "f" + shot
                        elif (l < (2398 + 5418)):
                            shot = "b" + shot
                        elif (l < (2398 + 5418 + 343)):
                            shot =  "s" + shot
                        elif (l < (2398 + 5418 + 343 + 21)):
                            shot = "v" + shot
                        elif (l < (2398 + 5418 + 343 + 21 + 364)):
                            shot = "z" + shot
                        elif (l < (2398 + 5418 + 343 + 21 + 364 + 139)):
                            shot = "o" + shot
                        elif (l < (2398 + 5418 + 343 + 21 + 364 + 139 + 11)):
                            shot = "p" + shot
                        elif (l < (2398 + 5418 + 343 + 21 + 364 + 139 + 11 
                                   + 11)):
                            shot = "u" + shot
                        elif (l < (2398 + 5418 + 343 + 21 + 364 + 139 + 11 
                                   + 11 + 1156)):
                            shot = "y" + shot
                        elif (l < (2398 + 5418 + 343 + 21 + 364 + 139 + 11 
                                   + 11 + 1156 + 32)):
                            shot = "m" + shot
                        elif (l < (2398 + 5418 + 343 + 21 + 364 + 139 + 11 
                                   + 11 + 1156 + 32 + 32)):
                            shot = "i" + shot
                        elif (l < (2398 + 5418 + 343 + 21 + 364 + 139 + 11 
                                   + 11 + 1156 + 32 + 32 + 75)):
                            shot = "j" + shot

                    elif (i < (3065 + 1976)):
                        shot = "2"

                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 783):
                            shot = shot + "7"
                        elif (j < (783 + 4000)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (498 + 498)):
                            shot = shot + "nwdx"
                        elif (k < (498 + 498 + 249)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 681):
                            shot = "f" + shot
                        elif (l < (681 + 7442)):
                            shot = "b" + shot
                        elif (l < (681 + 7442 + 831)):
                            shot = "s" + shot
                        elif (l < (681 + 7442 + 831 + 17)):
                            shot = "v" + shot
                        elif (l < (681 + 7442 + 831 + 17 + 349)):
                            shot = "z" + shot
                        elif (l < (681 + 7442 + 831 + 17 + 349 + 183)):
                            shot = "o" + shot
                        elif (l < (681 + 7442 + 831 + 17 + 349 + 183 + 17)):
                            shot = "p" + shot
                        elif (l < (681 + 7442 + 831 + 17 + 349 + 183 + 17 
                                   + 83)):
                            shot = "y" + shot
                        elif (l < (681 + 7442 + 831 + 17 + 349 + 183 + 17 
                                   + 83 + 332)):
                            shot = "m" + shot
                        elif (l < (681 + 7442 + 831 + 17 + 349 + 183 + 17 
                                   + 83 + 332 + 33)):
                            shot = "i" + shot
                        elif (l < (681 + 7442 + 831 + 17 + 349 + 183 + 17 
                                   + 83 + 332 + 33 + 17)):
                            shot = "j" + shot
                        elif (l < (681 + 7442 + 831 + 17 + 349 + 183 + 17 
                                   + 83 + 332 + 33 + 17 + 17)):
                            shot = "t" + shot

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)

                        # Shot length is added
                        if (j < 1556):
                            shot = shot + "7"
                        elif (j < (1556 + 4553)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (457 + 185 + 146 + 20)):
                            shot = shot + "nwdx"
                        elif (k < (457 + 185 + 146 + 20 + 642)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 1635):
                            shot = "f" + shot
                        elif (l < (1635 + 6870)):
                            shot = "b" + shot
                        elif (l < (1635 + 6870 + 754)):
                            shot = "s" + shot
                        elif (l < (1635 + 6870 + 754 + 7)):
                            shot = "v" + shot
                        elif (l < (1635 + 6870 + 754 + 7 + 218)):
                            shot = "z" + shot
                        elif (l < (1635 + 6870 + 754 + 7 + 218 + 126)):
                            shot = "o" + shot
                        elif (l < (1635 + 6870 + 754 + 7 + 218 + 126 + 7)):
                            shot = "p" + shot
                        elif (l < (1635 + 6870 + 754 + 7 + 218 + 126 + 7 
                                   + 40)):
                            shot = "u" + shot
                        elif (l < (1635 + 6870 + 754 + 7 + 218 + 126 + 7 
                                   + 40 + 205)):
                            shot = "y" + shot
                        elif (l < (1635 + 6870 + 754 + 7 + 218 + 126 + 7 
                                   + 40 + 205 + 20)):
                            shot = "l" + shot
                        elif (l < (1635 + 6870 + 754 + 7 + 218 + 126 + 7 
                                   + 40 + 205 + 20 + 40)):
                            shot = "m" + shot
                        elif (l < (1635 + 6870 + 754 + 7 + 218 + 126 + 7 
                                   + 40 + 205 + 20 + 40 + 7)):
                            shot = "i" + shot
                        elif (l < (1635 + 6870 + 754 + 7 + 218 + 126 + 7 
                                   + 40 + 205 + 20 + 40 + 7 + 46)):
                            shot = "j" + shot
                        elif (l < (1635 + 6870 + 754 + 7 + 218 + 126 + 7 
                                   + 40 + 205 + 20 + 40 + 7 + 46 + 26)):
                            shot = "k" + shot
            
            # ElIf Djoko was returning a second serve in the ralley
            elif(ralley.Ralley.get_len_ralley(current_ralley) % 2 == 0
                and self.Returning == True
                and "," in 
                ralley.Ralley.get_first_shot_of_ralley(current_ralley)):
                #print("Djoko is returning a second serve in this ralley")
                
                # If Opponents last shot was dir 1
                if "1" in current_ralley.get_last_shot():
                    #print("Opponents last shot was in dir 1")
                    # probabilities for Djokos Shot are added
                    
                    i = random.randint(0, 9999)
                    if (i < 4504):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 2331):
                            shot = shot + "7"
                        elif (j < (2331 + 4737)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (452 + 347 + 226 + 90)):
                            shot = shot + "nwdx"
                        elif (k < (452 + 347 + 226 + 90 + 347)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 8824):
                            shot = "f" + shot
                        elif (l < (8824 + 709)):
                            shot = "r" + shot
                        elif (l < (8824 + 709 + 166)):
                            shot = "v" + shot
                        elif (l < (8824 + 709 + 166 + 45)):
                            shot = "o" + shot
                        elif (l < (8824 + 709 + 166 + 45 + 75)):
                            shot = "u" + shot
                        elif (l < (8824 + 709 + 166 + 45 + 75 + 181)):
                            shot = "l" + shot

                    elif (i < (4504 + 2894)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1212):
                            shot = shot + "7"
                        elif (j < (1212 + 4091)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (446 + 540)):
                            shot = shot + "nwdx"
                        elif (k < (446 + 540 + 70)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 7723):
                            shot = "f" + shot
                        elif (l < (7723 + 1667)):
                            shot = "r" + shot
                        elif (l < (7723 + 1667 + 117)):
                            shot = "v" + shot
                        elif (l < (7723 + 1667 + 117 + 47)):
                            shot = "o" + shot
                        elif (l < (7723 + 1667 + 117 + 47 + 23)):
                            shot = "u" + shot
                        elif (l < (7723 + 1667 + 117 + 47 + 23 + 399)):
                            shot = "l" + shot
                        elif (l < (7723 + 1667 + 117 + 47 + 23 + 399 + 23)):
                            shot = "h" + shot

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 465):
                            shot = shot + "7"
                        elif (j < (465 + 3256)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (574 + 444 + 444 + 52)):
                            shot = shot + "nwdx"
                        elif (k < (574 + 444 + 444 + 52 + 522)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 8799):
                            shot = "f" + shot
                        elif (l < (8799 + 783)):
                            shot = "r" + shot
                        elif (l < (8799 + 783 + 78)):
                            shot = "v" + shot
                        elif (l < (8799 + 783 + 78 + 131)):
                            shot = "u" + shot
                        elif (l < (8799 + 783 + 78 + 131 + 209)):
                            shot = "l" + shot

                # ElIf Opponents last shot was dir 2
                elif "2" in current_ralley.get_last_shot():
                    #print("Opponents last shot was in dir 2")
                    # probabilities for Djokos Shot are added
                    i = random.randint(0, 9999)
                    if (i < 3410):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1622):
                            shot = shot + "7"
                        elif (j < (1622 + 5045)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (265 + 389 + 248)):
                            shot = shot + "nwdx"
                        elif (k < (265 + 389 + 248 + 708)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 7150):
                            shot = "f" + shot
                        elif (l < (7150 + 2018)):
                            shot = "b" + shot
                        elif (l < (7150 + 2018 + 53)):
                            shot = "r" + shot
                        elif (l < (7150 + 2018 + 53 + 354)):
                            shot = "s" + shot
                        elif (l < (7150 + 2018 + 53 + 354 + 88)):
                            shot = "v" + shot
                        elif (l < (7150 + 2018 + 53 + 354 + 88 + 53)):
                            shot = "z" + shot
                        elif (l < (7150 + 2018 + 53 + 354 + 88 + 53 + 35)):
                            shot = "o" + shot
                        elif (l < (7150 + 2018 + 53 + 354 + 88 + 53 + 35 
                                   + 195)):
                            shot = "y" + shot
                        elif (l < (7150 + 2018 + 53 + 354 + 88 + 53 + 35 
                                   + 195 + 18)):
                            shot = "m" + shot
                        elif (l < (7150 + 2018 + 53 + 354 + 88 + 53 + 35 
                                   + 195 + 18 + 35)):
                            shot = "i" + shot

                    elif (i < (3410 + 2788)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1236):
                            shot = shot + "7"
                        elif (j < (1236 + 4607)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (281 + 346)):
                            shot = shot + "nwdx"
                        elif (k < (281 + 346 + 87)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 4242):
                            shot = "f" + shot
                        elif (l < (4242 + 4026)):
                            shot = "b" + shot
                        elif (l < (4242 + 4026 + 108)):
                            shot = "r" + shot
                        elif (l < (4242 + 4026 + 108 + 1320)):
                            shot = "s" + shot
                        elif (l < (4242 + 4026 + 108 + 1320 + 22)):
                            shot = "v" + shot
                        elif (l < (4242 + 4026 + 108 + 1320 + 22 + 65)):
                            shot = "z" + shot
                        elif (l < (4242 + 4026 + 108 + 1320 + 22 + 65 + 87)):
                            shot = "o" + shot
                        elif (l < (4242 + 4026 + 108 + 1320 + 22 + 65 + 87 
                                   + 22)):
                            shot = "p" + shot
                        elif (l < (4242 + 4026 + 108 + 1320 + 22 + 65 + 87 
                                   + 22 + 22)):
                            shot = "u" + shot
                        elif (l < (4242 + 4026 + 108 + 1320 + 22 + 65 + 87 
                                   + 22 + 22 + 22)):
                            shot = "y" + shot
                        elif (l < (4242 + 4026 + 108 + 1320 + 22 + 65 + 87 
                                   + 22 + 22 + 22 + 22)):
                            shot = "l" + shot
                        elif (l < (4242 + 4026 + 108 + 1320 + 22 + 65 + 87 
                                   + 22 + 22 + 22 + 22 + 43)):
                            shot = "m" + shot

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1382):
                            shot = shot + "7"
                        elif (j < (1382 + 4797)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"
                        
                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (190 + 206 + 190 + 63)):
                            shot = shot + "nwdx"
                        elif (k < (190 + 206 + 190 + 63 + 714)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 4921):
                            shot = "f" + shot
                        elif (l < (4921 + 3286)):
                            shot = "b" + shot
                        elif (l < (4921 + 3286 + 32)):
                            shot = "r" + shot
                        elif (l < (4921 + 3286 + 32 + 1397)):
                            shot = "s" + shot
                        elif (l < (4921 + 3286 + 32 + 1397 + 16)):
                            shot = "v" + shot
                        elif (l < (4921 + 3286 + 32 + 1397 + 16 + 159)):
                            shot = "z" + shot
                        elif (l < (4921 + 3286 + 32 + 1397 + 16 + 159 + 48)):
                            shot = "o" + shot
                        elif (l < (4921 + 3286 + 32 + 1397 + 16 + 159 + 48 
                                   + 16)):
                            shot = "p" + shot
                        elif (l < (4921 + 3286 + 32 + 1397 + 16 + 159 + 48 
                                   + 16 + 16)):
                            shot = "u" + shot
                        elif (l < (4921 + 3286 + 32 + 1397 + 16 + 159 + 48 
                                   + 16 + 16 + 79)):
                            shot = "y" + shot
                        elif (l < (4921 + 3286 + 32 + 1397 + 16 + 159 + 48 
                                   + 16 + 16 + 79 + 16)):
                            shot = "h" + shot
                        elif (l < (4921 + 3286 + 32 + 1397 + 16 + 159 + 48 
                                   + 16 + 16 + 79 + 16 + 16)):
                            shot = "j" + shot

                # ElIf Opponents last shot was dir 3
                elif "3" in current_ralley.get_last_shot():
                    #print("Opponents last shot was in dir 3")
                    # probabilities for Djokos Shot are added
                    i = random.randint(0, 9999)
                    if (i < 2156):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1011):
                            shot = shot + "7"
                        elif (j < (1011 + 3146)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (817 + 741 + 380 + 95)):
                            shot = shot + "nwdx"
                        elif (k < (817 + 741 + 380 + 95 + 817)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 1407):
                            shot = "f" + shot
                        elif (l < (1407 + 6654)):
                            shot = "b" + shot
                        elif (l < (1407 + 6654 + 19)):
                            shot = "r" + shot
                        elif (l < (1407 + 6654 + 19 + 951)):
                            shot = "s" + shot
                        elif (l < (1407 + 6654 + 19 + 951 + 171)):
                            shot = "z" + shot
                        elif (l < (1407 + 6654 + 19 + 951 + 171 + 19)):
                            shot = "o" + shot
                        elif (l < (1407 + 6654 + 19 + 951 + 171 + 19 + 551)):
                            shot = "y" + shot
                        elif (l < (1407 + 6654 + 19 + 951 + 171 + 19 + 551 
                                   + 209)):
                            shot = "m" + shot
                        elif (l < (1407 + 6654 + 19 + 951 + 171 + 19 + 551 
                                   + 209 + 19)):
                            shot = "t" + shot

                    elif (i < (2156 + 2320)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1136):
                            shot = shot + "7"
                        elif (j < (1136 + 4318)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (548 + 389)):
                            shot = shot + "nwdx"
                        elif (k < (548 + 389 + 71)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 177):
                            shot = "f" + shot
                        elif (l < (177 + 7420)):
                            shot = "b" + shot
                        elif (l < (177 + 7420 + 1767)):
                            shot = "s" + shot
                        elif (l < (177 + 7420 + 1767 + 53)):
                            shot = "z" + shot
                        elif (l < (177 + 7420 + 1767 + 53 + 71)):
                            shot = "o" + shot
                        elif (l < (177 + 7420 + 1767 + 53 + 71 + 18)):
                            shot = "y" + shot
                        elif (l < (177 + 7420 + 1767 + 53 + 71 + 18 + 495)):
                            shot = "m" + shot

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1673):
                            shot = shot + "7"
                        elif (j < (1673 + 4677)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (260 + 341 + 185 + 37)):
                            shot = shot + "nwdx"
                        elif (k < (260 + 341 + 185 + 37 + 334)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 653):
                            shot = "f" + shot
                        elif (l < (653 + 7270)):
                            shot = "b" + shot
                        elif (l < (653 + 7270 + 1684)):
                            shot = "s" + shot
                        elif (l < (653 + 7270 + 1684 + 104)):
                            shot = "z" + shot
                        elif (l < (653 + 7270 + 1684 + 104 + 15)):
                            shot = "o" + shot
                        elif (l < (653 + 7270 + 1684 + 104 + 15 + 7)):
                            shot = "p" + shot
                        elif (l < (653 + 7270 + 1684 + 104 + 15 + 7 + 37)):
                            shot = "u" + shot
                        elif (l < (653 + 7270 + 1684 + 104 + 15 + 7 + 37 
                                   + 126)):
                            shot = "y" + shot
                        elif (l < (653 + 7270 + 1684 + 104 + 15 + 7 + 37 
                                   + 126 + 104)):
                            shot = "m" + shot

            # ElIf Djoko was returning a first serve in the ralley
            elif(ralley.Ralley.get_len_ralley(current_ralley) % 2 == 1
                and self.Returning == True):
                #print("Djoko is returning a first serve in this ralley")
                
                # If Opponents last shot was dir 1
                if "1" in current_ralley.get_last_shot():
                    #print("Opponents last shot was in dir 1")
                    # probabilities for Djokos Shot are added
                    
                    i = random.randint(0, 9999)
                    if (i < 4379):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 2928):
                            shot = shot + "7"
                        elif (j < (2928 + 4751)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (472 + 449 + 334 + 46)):
                            shot = shot + "nwdx"
                        elif (k < (472 + 449 + 334 + 46 + 530)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 8641):
                            shot = "f" + shot
                        elif (l < (8641 + 806)):
                            shot = "r" + shot
                        elif (l < (8641 + 806 + 81)):
                            shot = "v" + shot
                        elif (l < (8641 + 806 + 81 + 12)):
                            shot = "o" + shot
                        elif (l < (8641 + 806 + 81 + 12 + 115)):
                            shot = "u" + shot
                        elif (l < (8641 + 806 + 81 + 12 + 115 + 334)):
                            shot = "l" + shot
                        elif (l < (8641 + 806 + 81 + 12 + 115 + 334 + 12)):
                            shot = "j" + shot

                    elif (i < (4379 + 2906)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 2209):
                            shot = shot + "7"
                        elif (j < (2209 + 4419)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (712 + 642)):
                            shot = shot + "nwdx"
                        elif (k < (712 + 642 + 52)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 6910):
                            shot = "f" + shot
                        elif (l < (6910 + 17)):
                            shot = "b" + shot
                        elif (l < (6910 + 17 + 1927)):
                            shot = "r" + shot
                        elif (l < (6910 + 17 + 1927 + 87)):
                            shot = "v" + shot
                        elif (l < (6910 + 17 + 1927 + 87 + 17)):
                            shot = "u" + shot
                        elif (l < (6910 + 17 + 1927 + 87 + 17 + 1024)):
                            shot = "l" + shot
                        elif (l < (6910 + 17 + 1927 + 87 + 17 + 1024 + 17)):
                            shot = "h" + shot
                        elif (l < (6910 + 17 + 1927 + 87 + 17 + 1024 + 17 + 17)):
                            shot = "t" + shot

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1250):
                            shot = shot + "7"
                        elif (j < (1250 + 5250)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (483 + 428 + 539 + 112)):
                            shot = shot + "nwdx"
                        elif (k < (483 + 428 + 539 + 112 + 799)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 8364):
                            shot = "f" + shot
                        elif (l < (8364 + 37)):
                            shot = "b" + shot
                        elif (l < (8364 + 37 + 967)):
                            shot = "r" + shot
                        elif (l < (8364 + 37 + 967 + 130)):
                            shot = "v" + shot
                        elif (l < (8364 + 37 + 967 + 130 + 74)):
                            shot = "u" + shot
                        elif (l < (8364 + 37 + 967 + 130 + 74 + 390)):
                            shot = "l" + shot
                        elif (l < (8364 + 37 + 967 + 130 + 74 + 390 + 37)):
                            shot = "h" + shot

                # ElIf Opponents last shot was dir 2
                elif "2" in current_ralley.get_last_shot():
                    #print("Opponents last shot was in dir 2")
                    # probabilities for Djokos Shot are added
                    i = random.randint(0, 9999)
                    if (i < 3177):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 2397):
                            shot = shot + "7"
                        elif (j < (2397 + 4876)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (247 + 378 + 230 + 33)):
                            shot = shot + "nwdx"
                        elif (k < (247 + 378 + 230 + 33 + 888)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 6694):
                            shot = "f" + shot
                        elif (l < (6694 + 2056)):
                            shot = "b" + shot
                        elif (l < (6694 + 2056 + 99)):
                            shot = "r" + shot
                        elif (l < (6694 + 2056 + 99 + 313)):
                            shot = "s" + shot
                        elif (l < (6694 + 2056 + 99 + 313 + 82)):
                            shot = "v" + shot
                        elif (l < (6694 + 2056 + 99 + 313 + 82 + 66)):
                            shot = "z" + shot
                        elif (l < (6694 + 2056 + 99 + 313 + 82 + 66 + 181)):
                            shot = "o" + shot
                        elif (l < (6694 + 2056 + 99 + 313 + 82 + 66 + 181 
                                   + 16)):
                            shot = "u" + shot
                        elif (l < (6694 + 2056 + 99 + 313 + 82 + 66 + 181 
                                   + 16 + 428)):
                            shot = "y" + shot
                        elif (l < (6694 + 2056 + 99 + 313 + 82 + 66 + 181 
                                   + 16 + 428 + 16)):
                            shot = "l" + shot
                        elif (l < (6694 + 2056 + 99 + 313 + 82 + 66 + 181 
                                   + 16 + 428 + 16 + 16)):
                            shot = "h" + shot
                        elif (l < (6694 + 2056 + 99 + 313 + 82 + 66 + 181 
                                   + 16 + 428 + 16 + 16 + 16)):
                            shot = "i" + shot
                        elif (l < (6694 + 2056 + 99 + 313 + 82 + 66 + 181 
                                   + 16 + 428 + 16 + 16 + 16 + 16)):
                            shot = "j" + shot

                    elif (i < (3177 + 3150)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1574):
                            shot = shot + "7"
                        elif (j < (1574 + 5000)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (182 + 481)):
                            shot = shot + "nwdx"
                        elif (k < (182 + 481 + 100)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 4080):
                            shot = "f" + shot
                        elif (l < (4080 + 3814)):
                            shot = "b" + shot
                        elif (l < (4080 + 3814 + 133)):
                            shot = "r" + shot
                        elif (l < (4080 + 3814 + 133 + 1294)):
                            shot = "s" + shot
                        elif (l < (4080 + 3814 + 133 + 1294 + 66)):
                            shot = "v" + shot
                        elif (l < (4080 + 3814 + 133 + 1294 + 66 + 17)):
                            shot = "z" + shot
                        elif (l < (4080 + 3814 + 133 + 1294 + 66 + 17 + 116)):
                            shot = "o" + shot
                        elif (l < (4080 + 3814 + 133 + 1294 + 66 + 17 + 116 
                                   + 17)):
                            shot = "u" + shot
                        elif (l < (4080 + 3814 + 133 + 1294 + 66 + 17 + 116 
                                   + 17 + 33)):
                            shot = "y" + shot
                        elif (l < (4080 + 3814 + 133 + 1294 + 66 + 17 + 116 
                                   + 17 + 33 + 216)):
                            shot = "l" + shot
                        elif (l < (4080 + 3814 + 133 + 1294 + 66 + 17 + 116 
                                   + 17 + 33 + 216 + 166)):
                            shot = "m" + shot
                        elif (l < (4080 + 3814 + 133 + 1294 + 66 + 17 + 116 
                                   + 17 + 33 + 216 + 166 + 17)):
                            shot = "h" + shot
                        elif (l < (4080 + 3814 + 133 + 1294 + 66 + 17 + 116 
                                   + 17 + 33 + 216 + 166 + 17 + 17)):
                            shot = "j" + shot
                        elif (l < (4080 + 3814 + 133 + 1294 + 66 + 17 + 116 
                                   + 17 + 33 + 216 + 166 + 17 + 17 + 17)):
                            shot = "t" + shot
                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1493):
                            shot = shot + "7"
                        elif (j < (1493 + 4328)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (341 + 384 + 128 + 14)):
                            shot = shot + "nwdx"
                        elif (k < (341 + 384 + 128 + 14 + 640)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 4196):
                            shot = "f" + shot
                        elif (l < (4196 + 3570)):
                            shot = "b" + shot
                        elif (l < (4196 + 3570 + 57)):
                            shot = "r" + shot
                        elif (l < (4196 + 3570 + 57 + 1579)):
                            shot = "s" + shot
                        elif (l < (4196 + 3570 + 57 + 1579 + 114)):
                            shot = "v" + shot
                        elif (l < (4196 + 3570 + 57 + 1579 + 114 + 128)):
                            shot = "z" + shot
                        elif (l < (4196 + 3570 + 57 + 1579 + 114 + 128 + 128)):
                            shot = "o" + shot
                        elif (l < (4196 + 3570 + 57 + 1579 + 114 + 128 + 128 
                                   + 14)):
                            shot = "p" + shot
                        elif (l < (4196 + 3570 + 57 + 1579 + 114 + 128 + 128 
                                   + 14 + 71)):
                            shot = "u" + shot
                        elif (l < (4196 + 3570 + 57 + 1579 + 114 + 128 + 128 
                                   + 14 + 71 + 71)):
                            shot = "y" + shot
                        elif (l < (4196 + 3570 + 57 + 1579 + 114 + 128 + 128 
                                   + 14 + 71 + 71 + 28)):
                            shot = "l" + shot
                        elif (l < (4196 + 3570 + 57 + 1579 + 114 + 128 + 128 
                                   + 14 + 71 + 71 + 28 + 28)):
                            shot = "m" + shot
                        elif (l < (4196 + 3570 + 57 + 1579 + 114 + 128 + 128 
                                   + 14 + 71 + 71 + 28 + 28 + 14)):
                            shot = "i" + shot

                # ElIf Opponents last shot was dir 3
                elif "3" in current_ralley.get_last_shot():
                    #print("Opponents last shot was in dir 3")
                    # probabilities for Djokos Shot are added
                    i = random.randint(0, 9999)
                    if (i < 2304):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1441):
                            shot = shot + "7"
                        elif (j < (1441 + 3475)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (748 + 906 + 504 + 43)):
                            shot = shot + "nwdx"
                        elif (k < (748 + 906 + 504 + 43 + 1007)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 878):
                            shot = "f" + shot
                        elif (l < (878 + 6590)):
                            shot = "b" + shot
                        elif (l < (878 + 6590 + 1165)):
                            shot = "s" + shot
                        elif (l < (878 + 6590 + 1165 + 14)):
                            shot = "v" + shot
                        elif (l < (878 + 6590 + 1165 + 14 + 187)):
                            shot = "z" + shot
                        elif (l < (878 + 6590 + 1165 + 14 + 187 + 43)):
                            shot = "o" + shot
                        elif (l < (878 + 6590 + 1165 + 14 + 187 + 43 + 691)):
                            shot = "y" + shot
                        elif (l < (878 + 6590 + 1165 + 14 + 187 + 43 + 691 
                                   + 14)):
                            shot = "l" + shot
                        elif (l < (878 + 6590 + 1165 + 14 + 187 + 43 + 691 
                                   + 14 + 403)):
                            shot = "m" + shot
                        elif (l < (878 + 6590 + 1165 + 14 + 187 + 43 + 691 
                                   + 14 + 403 + 14)):
                            shot = "i" + shot

                    elif (i < (2304 + 2606)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1061):
                            shot = shot + "7"
                        elif (j < (1061 + 4394)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (356 + 700)):
                            shot = shot + "nwdx"
                        elif (k < (356 + 700 + 51)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 267):
                            shot = "f" + shot
                        elif (l < (267 + 6832)):
                            shot = "b" + shot
                        elif (l < (267 + 6832 + 1832)):
                            shot = "s" + shot
                        elif (l < (267 + 6832 + 1832 + 38)):
                            shot = "z" + shot
                        elif (l < (267 + 6832 + 1832 + 38 + 64)):
                            shot = "y" + shot
                        elif (l < (267 + 6832 + 1832 + 38 + 64 + 25)):
                            shot = "l" + shot
                        elif (l < (267 + 6832 + 1832 + 38 + 64 + 25 + 916)):
                            shot = "m" + shot
                        elif (l < (267 + 6832 + 1832 + 38 + 64 + 25 + 916 
                                   + 13)):
                            shot = "k" + shot
                        elif (l < (267 + 6832 + 1832 + 38 + 64 + 25 + 916 
                                   + 13 + 13)):
                            shot = "t" + shot

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1863):
                            shot = shot + "7"
                        elif (j < (1863 + 4563)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (326 + 326 + 267 + 20)):
                            shot = shot + "nwdx"
                        elif (k < (326 + 326 + 267 + 20 + 306)):
                            shot = shot + "*"

                        # Shot Type is added
                        l = random.randint(0, 9999)
                        if (l < 508):
                            shot = "f" + shot
                        elif (l < (508 + 7251)):
                            shot = "b" + shot
                        elif (l < (508 + 7251 + 1648)):
                            shot = "s" + shot
                        elif (l < (508 + 7251 + 1648 + 91)):
                            shot = "z" + shot
                        elif (l < (508 + 7251 + 1648 + 91 + 13)):
                            shot = "o" + shot
                        elif (l < (508 + 7251 + 1648 + 91 + 13 + 13)):
                            shot = "p" + shot
                        elif (l < (508 + 7251 + 1648 + 91 + 13 + 13 + 20)):
                            shot = "u" + shot
                        elif (l < (508 + 7251 + 1648 + 91 + 13 + 13 + 20 
                                   + 176)):
                            shot = "y" + shot
                        elif (l < (508 + 7251 + 1648 + 91 + 13 + 13 + 20 
                                   + 176 + 7)):
                            shot = "l" + shot
                        elif (l < (508 + 7251 + 1648 + 91 + 13 + 13 + 20 
                                   + 176 + 7 + 274)):
                            shot = "m" + shot

            else: 
                shot = "123"
                print("Error: Szenario not covered.")
                print("Error occured whith ralley: " + str(current_ralley.get_ralley()))

        if shot == "123": print("Error occured whith ralley: " + str(current_ralley.get_ralley()))

        if simulation_phase == False:
            current_ralley.add_shot_to_ralley(shot)
        else: return shot
        shot = ""
        
        print("Ralley_after_statBotShot: " + str(current_ralley.get_ralley()))
        print("----------------------------")
        
    def set_turn(self, bool_var):
        self.turn = bool_var

    def get_turn(self):
        return self.turn