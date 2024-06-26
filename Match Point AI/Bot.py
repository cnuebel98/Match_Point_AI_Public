import pandas as pd
import random
import rally
import constants as const

class Bot:
    '''The Bot class has the functions for return random shot and some 
    DE stuff'''
    SERVE_DIRECTION = const.ShotEncodings.SERVE_DIRECTION
    EVERY_SHOT_TYPE = const.ShotEncodings.EVERY_SHOT_TYPE
    RETURN_SHOT_TYPES = const.ShotEncodings.RETURN_SHOT_TYPES
    RETURN_DEPTH = const.ShotEncodings.RETURN_DEPTH
    DIRECTIONS = const.ShotEncodings.DIRECTIONS
    RALLY_ERROR = const.ShotEncodings.RALLY_ERROR
    ERROR_TYPE = const.ShotEncodings.ERROR_TYPE
    WINNER = const.ShotEncodings.WINNER
    EXTRA_STUFF = const.ShotEncodings.EXTRA_STUFF
    WINNER_PROBA = 15
    ERROR_PROBA = 15

    def __init__(self, name="", turn=False):
        self.name = name
        self.turn = turn

    def import_data(self):
        # get the dataset and make it into a pandas dataframe that can 
        # be operated on 14 and 15 are the columns that have the rally 
        # sequences in them

        df = pd.read_csv(
            r"C:\Users\carlo\TrainingsTool\Tennis\Datasets\
                rallys_only_m_from_2017.csv")
        
        test_df = df.head(10000)
        
        shot_list_of_lists = []
        shot_list = []

        for i in range(0, len(test_df)):
            for j in range(0, 2):
                shot_list = self.turn_rally_into_shot_list(
                    str(test_df.iloc[i, j]))
                shot_list_of_lists.append(shot_list)
              
        new_df = pd.DataFrame(shot_list_of_lists)
        new_df.rename(columns={new_df.columns[0]: "One"}, inplace = True)
        new_df = new_df.drop(new_df[new_df["One"] == "%"].index)
       
    def add_shot_unused(self, rally):
        # ToDo return the next shot based on the rally and the data
        shot = 42
        rally.add_shot_to_rally(shot)
        
    def add_shot(self, current_rally, score, current_tree):
        # We will have a 30% Chance of terminating a point,
        # 15% chance of a winner and 15% Chance of an Error
        i = random.randint(0, 99)

        randomReturnType = self.RETURN_SHOT_TYPES[
            random.randint(0, len(self.RETURN_SHOT_TYPES)-1)]
        randomReturnDirection = self.DIRECTIONS[
            random.randint(0, len(self.DIRECTIONS)-1)]
        randomReturnDepth = self.RETURN_DEPTH[
            random.randint(0, len(self.RETURN_DEPTH)-1)]
        randomRallyError = self.RALLY_ERROR[
            random.randint(0, len(self.RALLY_ERROR)-1)]
        randomErrorType = self.ERROR_TYPE[
            random.randint(0, len(self.ERROR_TYPE)-1)]
        randomShotType = self.EVERY_SHOT_TYPE[
            random.randint(0, len(self.EVERY_SHOT_TYPE)-1)]
        randomShotDirection = self.DIRECTIONS[
            random.randint(0, len(self.DIRECTIONS)-1)]

        # When rally is empty, add a random serve
        if current_rally.get_shot_count() == 0:
            # Add random serve direction
            randomServeDirection = self.SERVE_DIRECTION[
                random.randint(0, len(self.SERVE_DIRECTION)-1)]
            shot = randomServeDirection
            # This is Ace probability, same as winner probability
            if i < self.WINNER_PROBA:
                # this is an ace
                shot = shot + self.WINNER
            elif i > 99 - self.ERROR_PROBA:
                # this is a fault on service (can be either first or 
                # second serve, first fault -> "," is added to shot 
                # encoding)
                shot = shot + randomRallyError
                if rally.Rally.get_len_rally(current_rally) == 0:
                    shot = shot + ","

        # If shot count in that rally is 1, add a return: Return cant 
        # be a volley for example, thats why this has to be different
        elif current_rally.get_shot_count() == 1:
            # Add valid return stroke including depth encoding
            shot = randomReturnType + randomReturnDirection
            # Add winner and error probabilities on return
            if i < self.WINNER_PROBA:
                shot = shot + randomReturnDepth + self.WINNER
            elif i > 99 - self.ERROR_PROBA:
                shot = shot + randomRallyError + randomErrorType
            else: shot = shot + randomReturnDepth

        # Just add random shots consisting of lenght and direction and 
        # 15% Chance of a winner and 15% Chance of an error
        else:
            # Add any shot after the return shot
            shot = randomShotType + randomShotDirection + randomReturnDepth
            # This adds winner and error encoding to shot with given 
            # probabilities
            if i < self.WINNER_PROBA:
                shot = shot + self.WINNER
            elif i > 99 - self.ERROR_PROBA:
                shot = shot + randomRallyError + randomErrorType
        
        # Add that shot to the rally
        current_rally.add_shot_to_rally(shot)
        print(current_rally.get_rally())

    def turn_rally_into_shot_list(self, rally):
        r = rally
        shot_list = []
        shot = ""
        #r = "6s39f!3x@"

        if r != "nan":
            for i in range(0, len(r)):
                # If the char is the last char in the rally, its added 
                # to the shot and the shot is added to the shot list
                if i == len(r)-1:
                    shot = shot + r[i]
                    shot_list.append(shot)
                    shot = ""

                # If char of rally is in serve Direction, its added to 
                # the shot
                elif r[i] in self.SERVE_DIRECTION:
                    shot = shot + r[i]
                    if r[i+1] in self.EVERY_SHOT_TYPE:
                        shot_list.append(shot)
                        shot = ""
                
                # If the charstand for one of the normal shot types, its 
                # added here and if the next char also is a normal shot 
                # type, shot is over and gets added
                elif r[i] in self.EVERY_SHOT_TYPE:
                    shot = shot + r[i]
                    if r[i+1] in self.EVERY_SHOT_TYPE:
                        shot_list.append(shot)
                        shot = ""
                
                # if char is error type or winner, rally is over
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
                
                # If Char is a Rally Error (not a type)
                elif r[i] in self.RALLY_ERROR:
                    shot = shot + r[i]
                    if r[i+1] not in self.ERROR_TYPE:
                        shot_list.append(shot)
                        shot = ""
                
                # if Char is one of the extra encodings for special 
                # cases
                elif r[i] in self.EXTRA_STUFF:
                    shot = shot + r[i]
                    if r[i+1] in self.EVERY_SHOT_TYPE:
                        shot_list.append(shot)
                        shot = ""

                # This gets printed when there is a rally, that is not
                # covered by those if statements
                else: print("Unknown Rally was given in " + r 
                            + " of the Dataset")
            #print(len(shot_list)) gives back 3 -> because there are 3 
            # shots in the rally
            return shot_list
        # when the rally is NaN a percent sign gets returned
        else: return "%"

    def set_turn(self, bool_var):
        self.turn = bool_var

    def get_turn(self):
        return self.turn