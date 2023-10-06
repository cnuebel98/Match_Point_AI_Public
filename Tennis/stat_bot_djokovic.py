import constants as const
import scoring
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
            shot = "SecondServeReturn"

            x = score.get_point_count_per_game()
            if (x % 2 == 0): 
                # Returning from Deuce Side of the court
                if (current_ralley.get_last_char_of_last_shot() == "4"):
                    print("2ndS return from Deuce Side on serve 4")
                elif (current_ralley.get_last_char_of_last_shot() == "5"):
                    print("2ndS return from Deuce Side on serve 5")
                elif (current_ralley.get_last_char_of_last_shot() == "6"):
                    print("2ndS return from Deuce Side on serve 6")
            elif (x % 2 == 1):
                # Returning from Ad Side of the court
                if (current_ralley.get_last_char_of_last_shot() == "4"):
                    print("2ndS return from Ad Side on serve 4")
                elif (current_ralley.get_last_char_of_last_shot() == "5"):
                    print("2ndS return from Ad Side on serve 5")
                elif (current_ralley.get_last_char_of_last_shot() == "6"):
                    print("2ndS return from Ad Side on serve 6")


        else:
            print("Error: Szenario was not covered")
            shot = "123"
        
        

        current_ralley.add_shot_to_ralley(shot)
        shot = ""
        print(current_ralley.get_ralley())

    def set_turn(self, bool_var):
        self.turn = bool_var

    def get_turn(self):
        return self.turn