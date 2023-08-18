# hier soll eine ralley reingegeben werden 
# und dann soll der nächste Schlag basierend auf echten Daten
# zurückgegeben werden

import pandas as pd
import random

class Bot:

    SERVE_DIRECTION = ["4", "5", "6"]
    EVERY_SHOT_TYPE = ["f", "b", "r", "s", "v", "z", "o", "p", "y", "l", "m", "h", "i", "j", "k", "t", "u"]
    RETURN_SHOT_TYPES = ["f", "b", "r", "s", "y", "l", "m", "h", "i", "t", "u"]
    RETURN_DEPTH = ["7", "8", "9"]
    DIRECTIONS = ["1", "2", "3"]
    RALLEY_ERROR = ["n", "w", "d", "x"]
    ERROR_TYPE = ["@", "#"]
    WINNER = "*"
    EXTRA_STUFF = ["+", ";", "^", "S", "R", "C", "!", "0", "-", "=", "P", "Q", "c", "q", "e", "N"]
    WINNER_PROBA = 15
    ERROR_PROBA = 15

    def __init__(self, name="", turn=False):
        self.name = name
        self.turn = turn

    def import_data(self):
        # get the dataset and make it into a pandas dataframe 
        # that can be operated on
        # 14 and 15 are the columns that have the ralley sequences in them
        #df_new = df.iloc[:,14:16]
        #df_new.to_csv(r"C:\Users\carlo\TrainingsTool\Tennis\Datasets\ralleys_only_m_from_2017", index = False)
        #print(df_new.head(10))
        #print(len(df_new))

        df = pd.read_csv(r"C:\Users\carlo\TrainingsTool\Tennis\Datasets\ralleys_only_m_from_2017.csv")
        
        test_df = df.head(10000)
        
        shot_list_of_lists = []
        shot_list = []

        #shot_list = self.turn_ralley_into_shot_list(str(test_df.iloc[0,0]))

        for i in range(0, len(test_df)):
            for j in range(0, 2):
                shot_list = self.turn_ralley_into_shot_list(str(test_df.iloc[i, j]))
                shot_list_of_lists.append(shot_list)
              
        new_df = pd.DataFrame(shot_list_of_lists)
        new_df.rename(columns={new_df.columns[0]: "One"}, inplace = True)
        new_df = new_df.drop(new_df[new_df["One"] == "%"].index)
        #print(new_df)
       
    def add_shot(self, ralley):
        # ToDo return the next shot based on the ralley and the data
        shot = 42
        ralley.add_shot_to_ralley(shot)
        #print(ralley.get_ralley())

    def add_random_shot(self, ralley):
        # We will have a 30% Chance of finishing a point,
        # 15% cahnce of a winner and 15% Chance of a Error
        i = random.randint(0, 99)
        randomReturnType = self.RETURN_SHOT_TYPES[random.randint(0, len(self.RETURN_SHOT_TYPES)-1)]
        randomReturnDirection = self.DIRECTIONS[random.randint(0, len(self.DIRECTIONS)-1)]
        randomReturnDepth = self.RETURN_DEPTH[random.randint(0, len(self.RETURN_DEPTH)-1)]
        randomRalleyError = self.RALLEY_ERROR[random.randint(0, len(self.RALLEY_ERROR)-1)]
        randomErrorType = self.ERROR_TYPE[random.randint(0, len(self.ERROR_TYPE)-1)]
        randomShotType = self.EVERY_SHOT_TYPE[random.randint(0, len(self.EVERY_SHOT_TYPE)-1)]
        randomShotDirection = self.DIRECTIONS[random.randint(0, len(self.DIRECTIONS)-1)]

        # When ralley is empty, add a random serve
        if ralley.get_shot_count() == 0:
            # Add random serve direction
            randomServeDirection = self.SERVE_DIRECTION[random.randint(0, len(self.SERVE_DIRECTION)-1)]
            shot = randomServeDirection
            # ToDo: add Ace/Error probabilities
            # ToDo: Handle second serves

        # If shot count in that ralley is 1, add a return: Return cant be a volley for example, 
        # thats why this has to be different
        elif ralley.get_shot_count() == 1:
            # Add valid return stroke including depth encoding
            shot = randomReturnType + randomReturnDirection
            # Add winner and error probabilities on return
            if i < self.WINNER_PROBA:
                shot = shot + randomReturnDepth + self.WINNER
            elif i > 99 - self.ERROR_PROBA:
                shot = shot + randomRalleyError + randomErrorType
            else: shot = shot + randomReturnDepth

        # Just add random shots consisting of lenght and direction and 
        # 15% Chance of a winner and 15% Chance of a 
        else:
            # Add any shot after the return shot
            shot = randomShotType + randomShotDirection + randomReturnDepth
            # Add winner and error probabilities
            if i < self.WINNER_PROBA:
                shot = shot + self.WINNER
            elif i > 99 - self.ERROR_PROBA:
                shot = shot + randomRalleyError + randomErrorType
        
        # Add that shot to the ralley
        ralley.add_shot_to_ralley(shot)
        print(ralley.get_ralley())

    def turn_ralley_into_shot_list(self, ralley):
        
        r = ralley
        shot_list = []
        shot = ""
        #r = "6s39f!3x@"

        if r != "nan":
            for i in range(0, len(r)):
                # If the char is the last char in the ralley, its added to the shot
                # and the shot is added to the shot list
                if i == len(r)-1:
                    shot = shot + r[i]
                    shot_list.append(shot)
                    shot = ""

                # If char of ralley is in serve Direction, its added to the shot
                elif r[i] in self.SERVE_DIRECTION:
                    shot = shot + r[i]
                    if r[i+1] in self.EVERY_SHOT_TYPE:
                        shot_list.append(shot)
                        shot = ""
                
                # If the charstand for one of the normal shot types, its added here 
                # and if the next char also is a normal shot type, shot is over and gets added
                elif r[i] in self.EVERY_SHOT_TYPE:
                    shot = shot + r[i]
                    if r[i+1] in self.EVERY_SHOT_TYPE:
                        shot_list.append(shot)
                        shot = ""
                
                # if char is error type or winner, ralley is over
                elif r[i] in self.ERROR_TYPE or r[i] in self.WINNER:
                    shot = shot + r[i]
                    shot_list.append(shot)
                    shot = ""

                # If char is a direction encoding
                elif r[i] in self.DIRECTIONS:
                    shot = shot + r[i]
                    if r[i+1] in self.EVERY_SHOT_TYPE:
                        shot_list.append(shot)
                        shot = ""

                # If char is a depth encoding
                elif r[i] in self.RETURN_DEPTH:
                    shot = shot + r[i]
                    if r[i+1] in self.EVERY_SHOT_TYPE:
                        shot_list.append(shot)
                        shot = ""
                
                # If Char is a Ralley Error (not a type)
                elif r[i] in self.RALLEY_ERROR:
                    shot = shot + r[i]
                    if r[i+1] not in self.ERROR_TYPE:
                        shot_list.append(shot)
                        shot = ""
                
                # if Char is one of the extra encodings for special cases
                elif r[i] in self.EXTRA_STUFF:
                    shot = shot + r[i]
                    if r[i+1] in self.EVERY_SHOT_TYPE:
                        shot_list.append(shot)
                        shot = ""

                # This gets printed when there is a ralley, that is not covered by those if statements
                else: print("Unknown Ralley was given in " + r + " of the Dataset")
            #print(len(shot_list)) gives back 3 -> because there are 3 shots in the ralley
            return shot_list
        # when the ralley is NaN a percent sign gets returned
        else: return "%"

    def set_turn(self, bool_var):
        self.turn = bool_var

    def get_turn(self):
        return self.turn