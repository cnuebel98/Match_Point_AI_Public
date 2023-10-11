import constants as const
import random
import ralley

class Stat_Bot_Djokovic:
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

    def add_shot(self, current_ralley, score):
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
                if (j < 1588):
                    shot = shot + "n,"
                elif (j < (1588 + 761)):
                    shot = shot + "w,"
                elif (j < (1588 + 761 + 906)):
                    shot = shot + "d,"
                elif (j < (1588 + 761 + 906 + 284)):
                    shot = shot + "x,"
                elif (j < (1588 + 761 + 906 + 284 + 628)):
                    shot = shot + "*"
            elif (i < (4938+572)):
                shot = "5"
                # Error and Ace Probabilities for Serve Direction 5
                j = random.randint(0, 9999)
                if (j < 766):
                    shot = shot + "n,"
                elif (j < (766 + 1626)):
                    shot = shot + "d,"
                elif (j < (766 + 1626 + 19)):
                    shot = shot + "x,"
                elif (j < (766 + 1626 + 19 + 19)):
                    shot = shot + "*"
            else:
                shot = "6"
                # Error and Ace Probabilities for Serve Direction 6
                j = random.randint(0, 9999)
                if (j < 1265):
                    shot = shot + "n,"
                elif (j < (1265 + 598)):
                    shot = shot + "w,"
                elif (j < (1265 + 598 + 1347)):
                    shot = shot + "d,"
                elif (j < (1265 + 598 + 1347 + 100)):
                    shot = shot + "x,"
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
                if (j < 382):
                    shot = shot + "n"
                elif (j < (382 + 200)):
                    shot = shot + "w"
                elif (j < (382 + 200 + 373)):
                    shot = shot + "d"
                elif (j < (382 + 200 + 373 + 35)):
                    shot = shot + "x"
                elif (j < (382 + 200 + 373 + 35 + 43)):
                    shot = shot + "*"
            elif (i < (3628+3291)):
                shot = "5"
                j = random.randint(0, 9999)
                if (j < 220):
                    shot = shot + "n"
                elif (j < (220 + 258)):
                    shot = shot + "d"
            else:
                shot = "6"
                j = random.randint(0, 9999)
                if (j < 378):
                    shot = shot + "n"
                elif (j < (378 + 153)):
                    shot = shot + "w"
                elif (j < (378 + 153 + 501)):
                    shot = shot + "d"
                elif (j < (378 + 153 + 501 + 10)):
                    shot = shot + "x"
                elif (j < (378 + 153 + 501 + 10 + 174)):
                    shot = shot + "*"

        # do we return the first or the second serve (1st if statement)
        # First Serve is returned
        elif (ralley.Ralley.get_len_ralley(current_ralley) == 1):
            # Add return to the first Serve
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
                        if (k < 674):
                            shot = shot + "n"
                        elif (k < (674 + 751)):
                            shot = shot + "w"
                        elif (k < (674 + 751 + 855)):
                            shot = shot + "d"
                        elif (k < (674 + 751 + 855 + 181)):
                            shot = shot + "x"
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
                        if (k < 876):
                            shot = shot + "n"
                        elif (k < (876 + 1139)):
                            shot = shot + "d"
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
                        if (k < 1172):
                            shot = shot + "n"
                        elif (k < (1172 + 1719)):
                            shot = shot + "w"
                        elif (k < (1172 + 1719 + 1484)):
                            shot = shot + "d"
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
                        if (k < 1379):
                            shot = shot + "w"
                        elif (k < (1379 + 517)):
                            shot = shot + "d"
                        elif (k < (1379 + 517 + 172)):
                            shot = shot + "x"
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
                        if (k < 432):
                            shot = shot + "n"
                        elif (k < (432 + 617)):
                            shot = shot + "d"

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
                        if (k < 1053):
                            shot = shot + "n"
                        elif (k < (1053 + 789)):
                            shot = shot + "w"
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
                        if (k < 345):
                            shot = shot + "n"
                        elif (k < (345 + 1172)):
                            shot = shot + "w"
                        elif (k < (345 + 1172 + 1241)):
                            shot = shot + "d"
                        elif (k < (345 + 1172 + 1241 + 276)):
                            shot = shot + "x"
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
                        if (k < 654):
                            shot = shot + "n"
                        elif (k < (654 + 857)):
                            shot = shot + "d"
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
                        if (k < 822):
                            shot = shot + "n"
                        elif (k < (822 + 594)):
                            shot = shot + "w"
                        elif (k < (822 + 594 + 457)):
                            shot = shot + "d"
                        elif (k < (822 + 594 + 457 + 46)):
                            shot = shot + "x"
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
                        if (k < 978):
                            shot = shot + "n"
                        elif (k < (978 + 2065)):
                            shot = shot + "w"
                        elif (k < (978 + 2065 + 1957)):
                            shot = shot + "d"
                        elif (k < (978 + 2065 + 1957 + 109)):
                            shot = shot + "x"
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
                        if (k < 519):
                            shot = shot + "n"
                        elif (k < (519 + 1196)):
                            shot = shot + "d"

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
                        if (k < 799):
                            shot = shot + "n"
                        elif (k < (799 + 639)):
                            shot = shot + "w"
                        elif (k < (799 + 639 + 411)):
                            shot = shot + "d"
                        elif (k < (799 + 639 + 411 + 23)):
                            shot = shot + "x"
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
                        if (k < 1000):
                            shot = shot + "n"
                        elif (k < (1000 + 333)):
                            shot = shot + "w"
                        elif (k < (1000 + 333 + 333)):
                            shot = shot + "d"
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
                        if (k < 548):
                            shot = shot + "n"
                        elif (k < (548 + 1027)):
                            shot = shot + "d"

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
                        if (k < 423):
                            shot = shot + "n"
                        elif (k < (423 + 845)):
                            shot = shot + "w"
                        elif (k < (423 + 845 + 423)):
                            shot = shot + "d"
                        elif (k < (423 + 845 + 423 + 141)):
                            shot = shot + "x"

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
                        if (k < 1016):
                            shot = shot + "n"
                        elif (k < (1016 + 1094)):
                            shot = shot + "w"
                        elif (k < (1016 + 1094 + 781)):
                            shot = shot + "d"
                        elif (k < (1016 + 1094 + 781 + 78)):
                            shot = shot + "x"
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
                        if (k < 711):
                            shot = shot + "n"
                        elif (k < (711 + 1015)):
                            shot = shot + "d"

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
                        if (k < 662):
                            shot = shot + "n"
                        elif (k < (662 + 993)):
                            shot = shot + "w"
                        elif (k < (662 + 993 + 588)):
                            shot = shot + "d"
                        elif (k < (662 + 993 + 588 + 404)):
                            shot = shot + "x"
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
                        if (k < 1053):
                            shot = shot + "n"
                        elif (k < (1053 + 351)):
                            shot = shot + "w"
                        elif (k < (1053 + 351 + 526)):
                            shot = shot + "d"
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
                        if (k < 634):
                            shot = shot + "n"
                        elif (k < (634 + 1127)):
                            shot = shot + "d"

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
                        if (k < 1154):
                            shot = shot + "n"
                        elif (k < (1154 + 1154)):
                            shot = shot + "w"
                        elif (k < (1154 + 1154 + 962)):
                            shot = shot + "d"
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
                        if (k < 763):
                            shot = shot + "w"
                        elif (k < (763 + 593)):
                            shot = shot + "d"
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
                        if (k < 263):
                            shot = shot + "n"
                        elif (k < (263 + 547)):
                            shot = shot + "d"

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
                        if (k < 458):
                            shot = shot + "n"
                        elif (k < (458 + 458)):
                            shot = shot + "w"
                        elif (k < (458 + 458 + 654)):
                            shot = shot + "d"
                        elif (k < (458 + 458 + 654 + 65)):
                            shot = shot + "x"
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
                        if (k < 612):
                            shot = shot + "w"
                        elif (k < (612 + 1020)):
                            shot = shot + "d"
                        elif (k < (612 + 1020 + 408)):
                            shot = shot + "x"
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
                        if (k < 194):
                            shot = shot + "n"
                        elif (k < (194 + 647)):
                            shot = shot + "d"
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
                        if (k < 764):
                            shot = shot + "n"
                        elif (k < (764 + 347)):
                            shot = shot + "w"
                        elif (k < (764 + 347 + 486)):
                            shot = shot + "d"
                        elif (k < (764 + 347 + 486 + 69)):
                            shot = shot + "x"
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
                        if (k < 2500):
                            shot = shot + "w"
                        elif (k < (2500 + 1250)):
                            shot = shot + "d"
                        elif (k < (2500 + 1250 + 417)):
                            shot = shot + "x"
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
                        if (k < 357):
                            shot = shot + "n"
                        elif (k < (357 + 774)):
                            shot = shot + "d"

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
                        if (k < 244):
                            shot = shot + "n"
                        elif (k < (244 + 318)):
                            shot = shot + "w"
                        elif (k < (244 + 318 + 318)):
                            shot = shot + "d"
                        elif (k < (244 + 318 + 318 + 122)):
                            shot = shot + "x"
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
                        if (k < 513):
                            shot = shot + "n"
                        elif (k < (513 + 1026)):
                            shot = shot + "w"
                        elif (k < (513 + 1026 + 513)):
                            shot = shot + "d"
                        elif (k < (513 + 1026 + 513 + 513)):
                            shot = shot + "x"
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
                        if (k < 264):
                            shot = shot + "n"
                        elif (k < (264 + 617)):
                            shot = shot + "d"

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
                        if (k < 363):
                            shot = shot + "n"
                        elif (k < (363 + 297)):
                            shot = shot + "w"
                        elif (k < (363 + 297 + 396)):
                            shot = shot + "d"
                        elif (k < (363 + 297 + 396 + 33)):
                            shot = shot + "x"
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
                        if (k < 588):
                            shot = shot + "n"
                        elif (k < (588 + 1471)):
                            shot = shot + "w"
                        elif (k < (588 + 1471 + 588)):
                            shot = shot + "d"
                        elif (k < (588 + 1471 + 588 + 294)):
                            shot = shot + "x"
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
                        if (k < 604):
                            shot = shot + "n"
                        elif (k < (604 + 872)):
                            shot = shot + "d"

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
                        if (k < 617):
                            shot = shot + "n"
                        elif (k < (617 + 494)):
                            shot = shot + "w"
                        elif (k < (617 + 494 + 988)):
                            shot = shot + "d"
                        elif (k < (617 + 494 + 988 + 123)):
                            shot = shot + "x"
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
            shot = "123"
            # If Djoko was starting the ralley with a first serve
            if(ralley.Ralley.get_len_ralley(current_ralley) % 2 == 1
                and self.Serving == True
                and "," in 
                ralley.Ralley.get_first_shot_of_ralley(current_ralley)):
                print("Djoko was opening the ralley with a second serve")

                # If Opponents last shot was dir 1
                if "1" in current_ralley.get_last_shot():
                    print("Opponents last shot was in dir 1")
                    # probabilities for Djokos Shot are added

                # ElIf Opponents last shot was dir 2
                elif "2" in current_ralley.get_last_shot():
                    print("Opponents last shot was in dir 2")
                    # probabilities for Djokos Shot are added

                # ElIf Opponents last shot was dir 3
                elif "3" in current_ralley.get_last_shot():
                    print("Opponents last shot was in dir 3")
                    # probabilities for Djokos Shot are added
                
            # ElIf Djoko started Ralley with a second Serve
            elif(ralley.Ralley.get_len_ralley(current_ralley) % 2 == 0
                and self.Serving == True):
                print("Djoko was opening the ralley with a first serve")        
                
                # If Opponents last shot was dir 1
                if "1" in current_ralley.get_last_shot():
                    print("Opponents last shot was in dir 1")
                    # probabilities for Djokos Shot are added

                # ElIf Opponents last shot was dir 2
                elif "2" in current_ralley.get_last_shot():
                    print("Opponents last shot was in dir 2")
                    # probabilities for Djokos Shot are added

                # ElIf Opponents last shot was dir 3
                elif "3" in current_ralley.get_last_shot():
                    print("Opponents last shot was in dir 3")
                    # probabilities for Djokos Shot are added
            
            # ElIf Djoko was returning a second serve in the ralley
            elif(ralley.Ralley.get_len_ralley(current_ralley) % 2 == 0
                and self.Returning == True
                and "," in 
                ralley.Ralley.get_first_shot_of_ralley(current_ralley)):
                print("Djoko is returning a second serve in this ralley")
                
                # If Opponents last shot was dir 1
                if "1" in current_ralley.get_last_shot():
                    print("Opponents last shot was in dir 1")
                    # probabilities for Djokos Shot are added

                # ElIf Opponents last shot was dir 2
                elif "2" in current_ralley.get_last_shot():
                    print("Opponents last shot was in dir 2")
                    # probabilities for Djokos Shot are added

                # ElIf Opponents last shot was dir 3
                elif "3" in current_ralley.get_last_shot():
                    print("Opponents last shot was in dir 3")
                    # probabilities for Djokos Shot are added
            
            # ElIf Djoko was returning a first serve in the ralley
            elif(ralley.Ralley.get_len_ralley(current_ralley) % 2 == 1
                and self.Returning == True):
                print("Djoko is returning a first serve in this ralley")
                
                # If Opponents last shot was dir 1
                if "1" in current_ralley.get_last_shot():
                    print("Opponents last shot was in dir 1")
                        # probabilities for Djokos Shot are added

                # ElIf Opponents last shot was dir 2
                elif "2" in current_ralley.get_last_shot():
                    print("Opponents last shot was in dir 2")
                        # probabilities for Djokos Shot are added

                # ElIf Opponents last shot was dir 3
                elif "3" in current_ralley.get_last_shot():
                    print("Opponents last shot was in dir 3")
                        # probabilities for Djokos Shot are added
            else: 
                shot = "123"
                print("Szenario under development")

        current_ralley.add_shot_to_ralley(shot)
        shot = ""
        print(current_ralley.get_ralley())

    def set_turn(self, bool_var):
        self.turn = bool_var

    def get_turn(self):
        return self.turn