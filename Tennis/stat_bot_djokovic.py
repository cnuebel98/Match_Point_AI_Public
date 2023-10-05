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
                    shot = "1stS return from Deuce Side on serve 5"
                elif (current_ralley.get_last_char_of_last_shot() == "6"):
                    shot = "1stS return from Deuce Side on serve 6"
            elif (x % 2 == 1):
                # Returning from Ad Side of the court
                if (current_ralley.get_last_char_of_last_shot() == "4"):
                    shot = "1stS return from Ad Side on serve 4"
                elif (current_ralley.get_last_char_of_last_shot() == "5"):
                    shot = "1stS return from Ad Side on serve 5"
                elif (current_ralley.get_last_char_of_last_shot() == "6"):
                    shot = "1stS return from Ad Side on serve 6"
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