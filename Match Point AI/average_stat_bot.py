import constants as const
import random
import rally

class Average_Stat_Bot:
    '''This Bot uses a fixed strategy based on the Average Probabilities
    of all matches in the Dataset. It is the Average Player'''
    SERVE_DIRECTION = const.ShotEncodings.SERVE_DIRECTION
    EVERY_SHOT_TYPE = const.ShotEncodings.EVERY_SHOT_TYPE
    RETURN_SHOT_TYPES = const.ShotEncodings.RETURN_SHOT_TYPES
    RETURN_DEPTH = const.ShotEncodings.RETURN_DEPTH
    DIRECTIONS = const.ShotEncodings.DIRECTIONS
    RALLY_ERROR = const.ShotEncodings.RALLY_ERROR
    ERROR_TYPE = const.ShotEncodings.ERROR_TYPE
    WINNER = const.ShotEncodings.WINNER
    EXTRA_STUFF = const.ShotEncodings.EXTRA_STUFF
    Returning = False
    Serving = False

    def __init__(self, name="", turn=False):
        self.name = name
        self.turn = turn

    def add_shot(self, current_rally, score, current_tree, simulation_phase=False):
        '''Adds the most likely shot based on average player data'''
        
        # Adding first Serve
        if (rally.Rally.get_len_rally(current_rally) == 0):
            if (score.get_point_count_per_game() % 2 == 0):
                # Adding a first serve from deuce side
                # First we need to add the direction
                i = random.randint(0, 9999)
                self.Serving = True
                self.Returning = False
                # The real probabilities are used for 1st serve from deuce side
                if (i < 4975):
                    shot = "4"
                    # Error and Ace Probabilities for Serve Direction 4
                    j = random.randint(0, 9999)
                    if (j < (3896)):
                        shot = shot + "nwdx,"
                    elif (j < (3896 + 664)):
                        shot = shot + "*"
                elif (i < (4975 + 1017)):
                    shot = "5"
                    # Error and Ace Probabilities for Serve Direction 5
                    j = random.randint(0, 9999)
                    if (j < (2793)):
                        shot = shot + "nwdx,"
                    elif (j < (2793 + 14)):
                        shot = shot + "*"
                else:
                    shot = "6"
                    # Error and Ace Probabilities for Serve Direction 6
                    j = random.randint(0, 9999)
                    if (j < (3527)):
                        shot = shot + "nwdx,"
                    elif (j < (3527 + 897)):
                        shot = shot + "*"
            
            # Adding a first serve from ad side
            elif (score.get_point_count_per_game() % 2 == 1):
                #print("Adding first serve from ad side!")
                i = random.randint(0, 9999)
                self.Serving = True
                self.Returning = False
                # The real probabilities are used for 1st serve from deuce side
                if (i < 4369):
                    shot = "4"
                    # Error and Ace Probabilities for Serve Direction 4
                    j = random.randint(0, 9999)
                    if (j < (3310)):
                        shot = shot + "nwdx,"
                    elif (j < (3310 + 779)):
                        shot = shot + "*"
                elif (i < (4369 + 1045)):
                    shot = "5"
                    # Error and Ace Probabilities for Serve Direction 5
                    j = random.randint(0, 9999)
                    if (j < (2548)):
                        shot = shot + "nwdx,"
                    elif (j < (2548 + 14)):
                        shot = shot + "*"
                else:
                    shot = "6"
                    # Error and Ace Probabilities for Serve Direction 6
                    j = random.randint(0, 9999)
                    if (j < (3965)):
                        shot = shot + "nwdx,"
                    elif (j < (3965 + 973)):
                        shot = shot + "*"

        # Adding second Serve
        elif (rally.Rally.get_len_rally(current_rally) == 1
              and current_rally.get_last_char_of_last_shot() == ","):
            # Add Second Serve from deuce side
            if (score.get_point_count_per_game() % 2 == 0):
                self.Serving = True
                self.Returning = False
                i = random.randint(0, 9999)
                if (i < 2346):
                    shot = "4"
                    j = random.randint(0, 9999)
                    if (j < (1240)):
                        shot = shot + "nwdx"
                    elif (j < (1240 + 149)):
                        shot = shot + "*"
                elif (i < (2346 + 4103)):
                    shot = "5"
                    j = random.randint(0, 9999)
                    if (j < (737)):
                        shot = shot + "nwdx"
                    elif (j < (737 + 2)):
                        shot = shot + "*"
                else:
                    shot = "6"
                    j = random.randint(0, 9999)
                    if (j < (1068)):
                        shot = shot + "nwdx"
                    elif (j < (1068 + 94)):
                        shot = shot + "*"

            # Add Second Serve from ad side
            elif (score.get_point_count_per_game() % 2 == 1):
                self.Serving = True
                self.Returning = False
                i = random.randint(0, 9999)
                if (i < 4384):
                    shot = "4"
                    j = random.randint(0, 9999)
                    if (j < (840)):
                        shot = shot + "nwdx"
                    elif (j < (840 + 61)):
                        shot = shot + "*"
                elif (i < (4384 + 3713)):
                    shot = "5"
                    j = random.randint(0, 9999)
                    if (j < (755)):
                        shot = shot + "nwdx"
                    elif (j < (755 + 4)):
                        shot = shot + "*"
                else:
                    shot = "6"
                    j = random.randint(0, 9999)
                    if (j < (1373)):
                        shot = shot + "nwdx"
                    elif (j < (1373 + 299)):
                        shot = shot + "*"

        # Adding Return on first serve
        elif (rally.Rally.get_len_rally(current_rally) == 1):
            # Add return to the first Serve
            #print("Adding return to a first serve.")
            self.Serving = False
            self.Returning = True
            x = score.get_point_count_per_game()
            
            if (current_rally.get_last_char_of_last_shot() == "4"):
                # First serve was direction 4
                i = random.randint(0, 9999)
                if (i < 2015):
                    # Direction of the shot
                    shot = "1"
                    
                    # Lenght encoding of the shot has to be added
                    j = random.randint(0, 9999)
                    if (j < 2737):
                        shot = shot + "7"
                    elif (j < (2737 + 4565)):
                        shot = shot + "8"
                    else:
                        shot = shot + "9"

                    # Here the Error/Winner Probabilitites are added
                    k = random.randint(0, 9999)
                    if (k < (3005)):
                        shot = shot + "nwdx"
                    elif (k < (3005 + 390)):
                        shot = shot + "*"
                    
                elif (i < (2015 + 5124)):
                    # Direction of the shot
                    shot = "2"

                    # Lenght encoding of the shot has to be added
                    j = random.randint(0, 9999)
                    if (j < 2137):
                        shot = shot + "7"
                    elif (j < (2137 + 4406)):
                        shot = shot + "8"
                    else:
                        shot = shot + "9"

                    # Here the Error/Winner Probabilitites are added
                    k = random.randint(0, 9999)
                    if (k < (1942)):
                        shot = shot + "nwdx"
                    elif (k < (1942 + 21)):
                        shot = shot + "*"

                else:
                    # Direction of the shot
                    shot = "3"

                    # Lenght encoding of the shot has to be added
                    j = random.randint(0, 9999)
                    if (j < 3165):
                        shot = shot + "7"
                    elif (j < (3165 + 4354)):
                        shot = shot + "8"
                    else:
                        shot = shot + "9"

                    # Here the Error/Winner Probabilitites are added
                    k = random.randint(0, 9999)
                    if (k < (2574)):
                        shot = shot + "nwdx"
                    elif (k < (2574 + 147)):
                        shot = shot + "*"

            elif (current_rally.get_last_char_of_last_shot() == "5"):
                # shot = "1stS return on serve 5"

                i = random.randint(0, 9999)
                if (i < 1616):
                    # Direction of the shot
                    shot = "1"
                    
                    # Lenght encoding of the shot has to be added
                    j = random.randint(0, 9999)
                    if (j < 2682):
                        shot = shot + "7"
                    elif (j < (2682 + 4506)):
                        shot = shot + "8"
                    else:
                        shot = shot + "9"

                    # Here the Error/Winner Probabilitites are added
                    k = random.randint(0, 9999)
                    if (k < (2604)):
                        shot = shot + "nwdx"
                    elif (k < (2604 + 317)):
                        shot = shot + "*"

                elif (i < (1616 + 6106)):
                    # Direction of the shot
                    shot = "2"
                    
                    # Lenght encoding of the shot has to be added
                    j = random.randint(0, 9999)
                    if (j < 2222):
                        shot = shot + "7"
                    elif (j < (2222 + 4521)):
                        shot = shot + "8"
                    else:
                        shot = shot + "9"

                    # Here the Error/Winner Probabilitites are added
                    k = random.randint(0, 9999)
                    if (k < (1443)):
                        shot = shot + "nwdx"
                    elif (k < (1443 + 14)):
                        shot = shot + "*"

                else:
                    # Direction of the shot
                    shot = "3"
                    
                    # Lenght encoding of the shot has to be added
                    j = random.randint(0, 9999)
                    if (j < 2770):
                        shot = shot + "7"
                    elif (j < (2770 + 4693)):
                        shot = shot + "8"
                    else:
                        shot = shot + "9"

                    # Here the Error/Winner Probabilitites are added
                    k = random.randint(0, 9999)
                    if (k < (2230)):
                        shot = shot + "nwdx"
                    elif (k < (2230 + 95)):
                        shot = shot + "*"

            elif (current_rally.get_last_char_of_last_shot() == "6"):
                    # shot = "1stS return from Deuce Side on serve 6"
                    i = random.randint(0, 9999)
                    if (i < 1474):
                        # Direction of the shot
                        shot = "1"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 3042):
                            shot = shot + "7"
                        elif (j < (3042 + 4132)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (3089)):
                            shot = shot + "nwdx"
                        elif (k < (3089 + 238)):
                            shot = shot + "*"

                    elif (i < (1474 + 6346)):
                        # Direction of the shot
                        shot = "2"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2724):
                            shot = shot + "7"
                        elif (j < (2724 + 4427)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (1675)):
                            shot = shot + "nwdx"
                        elif (k < (1675 + 10)):
                            shot = shot + "*"

                    else:
                        # Direction of the shot
                        shot = "3"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 3158):
                            shot = shot + "7"
                        elif (j < (3158 + 4320)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (2507)):
                            shot = shot + "nwdx"
                        elif (k < (2507 + 46)):
                            shot = shot + "*"

        # Adding Return on second serve
        elif (rally.Rally.get_len_rally(current_rally) == 2
              and "," in 
              rally.Rally.get_first_shot_of_rally(current_rally)):
            # Add return to the Second Serve
            
            self.Serving = False
            self.Returning = True
            
            if (current_rally.get_last_char_of_last_shot() == "4"):
                i = random.randint(0, 9999)
                if (i < 1903):
                    # Direction of the shot
                    shot = "1"
                    
                    # Lenght encoding of the shot has to be added
                    j = random.randint(0, 9999)
                    if (j < 2237):
                        shot = shot + "7"
                    elif (j < (2237 + 4899)):
                        shot = shot + "8"
                    else:
                        shot = shot + "9"

                    # Here the Error/Winner Probabilitites are added
                    k = random.randint(0, 9999)
                    if (k < (2641)):
                        shot = shot + "nwdx"
                    elif (k < (2641 + 899)):
                        shot = shot + "*"

                elif (i < (1903 + 4052)):
                    # Direction of the shot
                    shot = "2"
                    
                    # Lenght encoding of the shot has to be added
                    j = random.randint(0, 9999)
                    if (j < 1519):
                        shot = shot + "7"
                    elif (j < (1519 + 4903)):
                        shot = shot + "8"
                    else:
                        shot = shot + "9"

                    # Here the Error/Winner Probabilitites are added
                    k = random.randint(0, 9999)
                    if (k < (1510)):
                        shot = shot + "nwdx"
                    elif (k < (1510 + 21)):
                        shot = shot + "*"

                else:
                    # Direction of the shot
                    shot = "3"
                    
                    # Lenght encoding of the shot has to be added
                    j = random.randint(0, 9999)
                    if (j < 2601):
                        shot = shot + "7"
                    elif (j < (2601 + 5046)):
                        shot = shot + "8"
                    else:
                        shot = shot + "9"

                    # Here the Error/Winner Probabilitites are added
                    k = random.randint(0, 9999)
                    if (k < (1513)):
                        shot = shot + "nwdx"
                    elif (k < (1513 + 195)):
                        shot = shot + "*"

            elif (current_rally.get_last_char_of_last_shot() == "5"):
                #print("2ndS return from Deuce Side on serve 5")
                #print("4")
                i = random.randint(0, 9999)
                if (i < 1669):
                    # Direction of the shot
                    shot = "1"
                    
                    # Lenght encoding of the shot has to be added
                    j = random.randint(0, 9999)
                    if (j < 2107):
                        shot = shot + "7"
                    elif (j < (2107 + 5037)):
                        shot = shot + "8"
                    else:
                        shot = shot + "9"

                    # Here the Error/Winner Probabilitites are added
                    k = random.randint(0, 9999)
                    if (k < (2223)):
                        shot = shot + "nwdx"
                    elif (k < (2223 + 744)):
                        shot = shot + "*"

                elif (i < (1669 + 5394)):
                    # Direction of the shot
                    shot = "2"
                    
                    # Lenght encoding of the shot has to be added
                    j = random.randint(0, 9999)
                    if (j < 1823):
                        shot = shot + "7"
                    elif (j < (1823 + 4877)):
                        shot = shot + "8"
                    else:
                        shot = shot + "9"

                    # Here the Error/Winner Probabilitites are added
                    k = random.randint(0, 9999)
                    if (k < (1114)):
                        shot = shot + "nwdx"
                    elif (k < (1114 + 16)):
                        shot = shot + "*"

                else:
                    # Direction of the shot
                    shot = "3"
                    
                    # Lenght encoding of the shot has to be added
                    j = random.randint(0, 9999)
                    if (j < 2452):
                        shot = shot + "7"
                    elif (j < (2452 + 5109)):
                        shot = shot + "8"
                    else:
                        shot = shot + "9"

                    # Here the Error/Winner Probabilitites are added
                    k = random.randint(0, 9999)
                    if (k < (1481)):
                        shot = shot + "nwdx"
                    elif (k < (1481 + 232)):
                        shot = shot + "*"

            elif (current_rally.get_last_char_of_last_shot() == "6"):
                    #print("2ndS return from Deuce Side on serve 6")
                    #print("5")
                    i = random.randint(0, 9999)
                    if (i < 1544):
                        # Direction of the shot
                        shot = "1"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2077):
                            shot = shot + "7"
                        elif (j < (2077 + 5096)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (2316)):
                            shot = shot + "nwdx"
                        elif (k < (2316 + 787)):
                            shot = shot + "*"

                    elif (i < (1544 + 6048)):
                        # Direction of the shot
                        shot = "2"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2037):
                            shot = shot + "7"
                        elif (j < (2037 + 4912)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (1164)):
                            shot = shot + "nwdx"
                        elif (k < (1164 + 14)):
                            shot = shot + "*"

                    else:
                        # Direction of the shot
                        shot = "3"
                        
                        # Lenght encoding of the shot has to be added
                        j = random.randint(0, 9999)
                        if (j < 2277):
                            shot = shot + "7"
                        elif (j < (2277 + 5185)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Here the Error/Winner Probabilitites are added
                        k = random.randint(0, 9999)
                        if (k < (1685)):
                            shot = shot + "nwdx"
                        elif (k < (1685 + 219)):
                            shot = shot + "*"

        # Adding a normal shot to an ongoing rally
        else:
            # We need to seperate between serving and returning in the
            # rally and also between first and second serves
            
            # Here we set the new self.Serving and self.Returning 
            # Variables according to the rally
            if (rally.Rally.get_len_rally(current_rally) % 2 == 0):
                if ("," in rally.Rally.get_first_shot_of_rally(current_rally)):
                    #print("Rally, where Average_Player is returning 2nd")
                    self.Serving = False
                    self.Returning = True
                else: 
                    #print("Rally, where Average_Player is Serving a 1st")
                    self.Serving = True
                    self.Returning = False
            elif (rally.Rally.get_len_rally(current_rally) % 2 == 1):
                if ("," in rally.Rally.get_first_shot_of_rally(current_rally)):
                    #print("rally, where Average_Player is serving a 2nd")
                    self.Serving = True
                    self.Returning = False
                else: 
                    #print("rally, where Average_Player is returning a 1st")
                    self.Serving = False
                    self.Returning = True

            # If Average_Player was starting the rally with a second serve
            if(rally.Rally.get_len_rally(current_rally) % 2 == 1
                and self.Serving == True
                and "," in 
                rally.Rally.get_first_shot_of_rally(current_rally)):
                #print("Average_Player was opening the rally with a second serve")

                # If Opponents last shot was dir 1
                if "1" in current_rally.get_last_shot():
                    #print("Opponents last shot was in dir 1")
                    # probabilities for Average_Players Shot are added
                    
                    i = random.randint(0, 9999)
                    if (i < 4410):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 2395):
                            shot = shot + "7"
                        elif (j < (2395 + 4580)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1509)):
                            shot = shot + "nwdx"
                        elif (k < (1509 + 577)):
                            shot = shot + "*"

                    elif (i < (4410 + 2794)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1728):
                            shot = shot + "7"
                        elif (j < (1728 + 4390)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1411)):
                            shot = shot + "nwdx"
                        elif (k < (1411 + 114)):
                            shot = shot + "*"

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1449):
                            shot = shot + "7"
                        elif (j < (1449 + 4448)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (2271)):
                            shot = shot + "nwdx"
                        elif (k < (2271 + 1025)):
                            shot = shot + "*"

                # ElIf Opponents last shot was dir 2
                elif "2" in current_rally.get_last_shot():
                    #print("Opponents last shot was in dir 2")
                    # probabilities for Average_Players Shot are added
                    
                    i = random.randint(0, 9999)
                    if (i < 3078):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1734):
                            shot = shot + "7"
                        elif (j < (1734 + 4789)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1500)):
                            shot = shot + "nwdx"
                        elif (k < (1500 + 1126)):
                            shot = shot + "*"

                    elif (i < (3078 + 3028)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1487):
                            shot = shot + "7"
                        elif (j < (1487 + 4702)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1046)):
                            shot = shot + "nwdx"
                        elif (k < (1046 + 102)):
                            shot = shot + "*"

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1570):
                            shot = shot + "7"
                        elif (j < (1570 + 4702)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1334)):
                            shot = shot + "nwdx"
                        elif (k < (1334 + 733)):
                            shot = shot + "*"

                # ElIf Opponents last shot was dir 3
                elif "3" in current_rally.get_last_shot():
                    #print("Opponents last shot was in dir 3")
                    # probabilities for Average_Players Shot are added
                    
                    i = random.randint(0, 9999)
                    if (i < 2096):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1478):
                            shot = shot + "7"
                        elif (j < (1478 + 4324)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabilities are added
                        k = random.randint(0, 9999)
                        if (k < (2399)):
                            shot = shot + "nwdx"
                        elif (k < (2399 + 1451)):
                            shot = shot + "*"

                    elif (i < (2096 + 2608)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1332):
                            shot = shot + "7"
                        elif (j < (1332 + 4481)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1233)):
                            shot = shot + "nwdx"
                        elif (k < (1233 + 74)):
                            shot = shot + "*"

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1830):
                            shot = shot + "7"
                        elif (j < (1830 + 4784)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1167)):
                            shot = shot + "nwdx"
                        elif (k < (1167 + 317)):
                            shot = shot + "*"
  
            # ElIf Average_Player started rally with a first Serve
            elif(rally.Rally.get_len_rally(current_rally) % 2 == 0
                and self.Serving == True):
                #print("Average_Player was opening the rally with a first serve")        
                
                # If Opponents last shot was dir 1
                if "1" in current_rally.get_last_shot():
                    #print("Opponents last shot was in dir 1")
                    # probabilities for Average_Players Shot are added
                    i = random.randint(0, 9999)
                    if (i < 4226):
                        shot = "1"

                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 2697):
                            shot = shot + "7"
                        elif (j < (2697 + 4507)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1425)):
                            shot = shot + "nwdx"
                        elif (k < (1425 + 1094)):
                            shot = shot + "*"

                    elif (i < (4226 + 2529)):
                        shot = "2"

                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1882):
                            shot = shot + "7"
                        elif (j < (1882 + 4457)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1323)):
                            shot = shot + "nwdx"
                        elif (k < (1323 + 233)):
                            shot = shot + "*"

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)

                        # Shot length is added
                        if (j < 1616):
                            shot = shot + "7"
                        elif (j < (1616 + 4478)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1979)):
                            shot = shot + "nwdx"
                        elif (k < (1979 + 1501)):
                            shot = shot + "*"

                # ElIf Opponents last shot was dir 2
                elif "2" in current_rally.get_last_shot():
                    #print("Opponents last shot was in dir 2")
                    # probabilities for Average_Players Shot are added

                    i = random.randint(0, 9999)
                    if (i < 3413):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1834):
                            shot = shot + "7"
                        elif (j < (1834 + 4817)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1263)):
                            shot = shot + "nwdx"
                        elif (k < (1263 + 1758)):
                            shot = shot + "*"

                    elif (i < (3413 + 2377)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1604):
                            shot = shot + "7"
                        elif (j < (1604 + 4689)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (975)):
                            shot = shot + "nwdx"
                        elif (k < (975 + 291)):
                            shot = shot + "*"

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1701):
                            shot = shot + "7"
                        elif (j < (1701 + 4970)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1229)):
                            shot = shot + "nwdx"
                        elif (k < (1229 + 1320)):
                            shot = shot + "*"

                # ElIf Opponents last shot was dir 3
                elif "3" in current_rally.get_last_shot():
                    #print("Opponents last shot was in dir 3")
                    # probabilities for Average_Players Shot are added
                    
                    i = random.randint(0, 9999)
                    if (i < 2513):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1705):
                            shot = shot + "7"
                        elif (j < (1705 + 4102)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (2043)):
                            shot = shot + "nwdx"
                        elif (k < (2043 + 1985)):
                            shot = shot + "*"

                    elif (i < (2513 + 2254)):
                        shot = "2"

                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1440):
                            shot = shot + "7"
                        elif (j < (1440 + 4439)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1175)):
                            shot = shot + "nwdx"
                        elif (k < (1175 + 217)):
                            shot = shot + "*"

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)

                        # Shot length is added
                        if (j < 2046):
                            shot = shot + "7"
                        elif (j < (2046 + 4818)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1114)):
                            shot = shot + "nwdx"
                        elif (k < (1114 + 660)):
                            shot = shot + "*"
            
            # ElIf Average_Player was returning a second serve in the rally
            elif(rally.Rally.get_len_rally(current_rally) % 2 == 0
                and self.Returning == True
                and "," in 
                rally.Rally.get_first_shot_of_rally(current_rally)):
                #print("Average_Player is returning a second serve in this rally")
                
                # If Opponents last shot was dir 1
                if "1" in current_rally.get_last_shot():
                    #print("Opponents last shot was in dir 1")
                    # probabilities for Average_Players Shot are added
                    
                    i = random.randint(0, 9999)
                    if (i < 4295):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 2347):
                            shot = shot + "7"
                        elif (j < (2347 + 4746)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1516)):
                            shot = shot + "nwdx"
                        elif (k < (1516 + 506)):
                            shot = shot + "*"

                    elif (i < (4295 + 3146)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1856):
                            shot = shot + "7"
                        elif (j < (1856 + 4224)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1420)):
                            shot = shot + "nwdx"
                        elif (k < (1420 + 80)):
                            shot = shot + "*"

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1447):
                            shot = shot + "7"
                        elif (j < (1447 + 4398)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (2375)):
                            shot = shot + "nwdx"
                        elif (k < (2375 + 892)):
                            shot = shot + "*"

                # ElIf Opponents last shot was dir 2
                elif "2" in current_rally.get_last_shot():
                    #print("Opponents last shot was in dir 2")
                    # probabilities for Average_Players Shot are added
                    i = random.randint(0, 9999)
                    if (i < 3052):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1713):
                            shot = shot + "7"
                        elif (j < (1713 + 4879)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1531)):
                            shot = shot + "nwdx"
                        elif (k < (1531 + 1123)):
                            shot = shot + "*"

                    elif (i < (3052 + 3126)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1373):
                            shot = shot + "7"
                        elif (j < (1373 + 4816)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (936)):
                            shot = shot + "nwdx"
                        elif (k < (936 + 99)):
                            shot = shot + "*"

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1528):
                            shot = shot + "7"
                        elif (j < (1528 + 5039)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"
                        
                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1258)):
                            shot = shot + "nwdx"
                        elif (k < (1258 + 734)):
                            shot = shot + "*"

                # ElIf Opponents last shot was dir 3
                elif "3" in current_rally.get_last_shot():
                    #print("Opponents last shot was in dir 3")
                    # probabilities for Average_Players Shot are added
                    i = random.randint(0, 9999)
                    if (i < 1859):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1277):
                            shot = shot + "7"
                        elif (j < (1277 + 4271)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (2493)):
                            shot = shot + "nwdx"
                        elif (k < (2493 + 1221)):
                            shot = shot + "*"

                    elif (i < (1859 + 2822)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1355):
                            shot = shot + "7"
                        elif (j < (1355 + 4429)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1171)):
                            shot = shot + "nwdx"
                        elif (k < (1171 + 67)):
                            shot = shot + "*"

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1837):
                            shot = shot + "7"
                        elif (j < (1837 + 4429)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1155)):
                            shot = shot + "nwdx"
                        elif (k < (1155 + 271)):
                            shot = shot + "*"

            # ElIf Average_Player was returning a first serve in the rally
            elif(rally.Rally.get_len_rally(current_rally) % 2 == 1
                and self.Returning == True):
                #print("Average_Player is returning a first serve in this rally")
                
                # If Opponents last shot was dir 1
                if "1" in current_rally.get_last_shot():
                    #print("Opponents last shot was in dir 1")
                    # probabilities for Average_Players Shot are added
                    
                    i = random.randint(0, 9999)
                    if (i < 4180):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 2587):
                            shot = shot + "7"
                        elif (j < (2587 + 4533)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1780)):
                            shot = shot + "nwdx"
                        elif (k < (1780 + 598)):
                            shot = shot + "*"

                    elif (i < (4180 + 3276)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1915):
                            shot = shot + "7"
                        elif (j < (1915 + 4308)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1568)):
                            shot = shot + "nwdx"
                        elif (k < (1568 + 91)):
                            shot = shot + "*"

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1632):
                            shot = shot + "7"
                        elif (j < (1632 + 4177)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (2566)):
                            shot = shot + "nwdx"
                        elif (k < (2566 + 976)):
                            shot = shot + "*"

                # ElIf Opponents last shot was dir 2
                elif "2" in current_rally.get_last_shot():
                    #print("Opponents last shot was in dir 2")
                    # probabilities for Average_Players Shot are added
                    i = random.randint(0, 9999)
                    if (i < 3005):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1710):
                            shot = shot + "7"
                        elif (j < (1710 + 4779)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1613)):
                            shot = shot + "nwdx"
                        elif (k < (1613 + 1142)):
                            shot = shot + "*"

                    elif (i < (3005 + 3345)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1363):
                            shot = shot + "7"
                        elif (j < (1363 + 4751)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1047)):
                            shot = shot + "nwdx"
                        elif (k < (1047 + 114)):
                            shot = shot + "*"

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1489):
                            shot = shot + "7"
                        elif (j < (1489 + 4974)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1309)):
                            shot = shot + "nwdx"
                        elif (k < (1309 + 824)):
                            shot = shot + "*"

                # ElIf Opponents last shot was dir 3
                elif "3" in current_rally.get_last_shot():
                    #print("Opponents last shot was in dir 3")
                    # probabilities for Average_Players Shot are added
                    i = random.randint(0, 9999)
                    if (i < 1979):
                        shot = "1"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1404):
                            shot = shot + "7"
                        elif (j < (1404 + 4112)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (2780)):
                            shot = shot + "nwdx"
                        elif (k < (2780 + 1314)):
                            shot = shot + "*"

                    elif (i < (1979 + 3030)):
                        shot = "2"
                        # Shot length is added
                        j = random.randint(0, 9999)
                        if (j < 1556):
                            shot = shot + "7"
                        elif (j < (1556 + 4265)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1366)):
                            shot = shot + "nwdx"
                        elif (k < (1366 + 71)):
                            shot = shot + "*"

                    else:
                        shot = "3"
                        j = random.randint(0, 9999)
                        # Shot length is added
                        if (j < 1978):
                            shot = shot + "7"
                        elif (j < (1978 + 4724)):
                            shot = shot + "8"
                        else:
                            shot = shot + "9"

                        # Error and Winner Probabiliteis are added
                        k = random.randint(0, 9999)
                        if (k < (1325)):
                            shot = shot + "nwdx"
                        elif (k < (1325 + 349)):
                            shot = shot + "*"

            else: 
                shot = "123"
                print("Error: Szenario not covered.")
                print("Error occured with rally: " + str(current_rally.get_rally()))

        if simulation_phase == False:
            current_rally.add_shot_to_rally(shot)
        else: 
            if shot == None:
                print("Error, Bot shot didnt get a value!")
                shot = "28"
            return shot
        shot = ""
        
        #print("Rally_after_Average_Stat_Bot: " + str(current_rally.get_rally()))
        #print("----------------------------")
        
    def set_turn(self, bool_var):
        self.turn = bool_var

    def get_turn(self):
        return self.turn