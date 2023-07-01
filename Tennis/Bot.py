# hier soll eine ralley reingegeben werden 
# und dann soll der nächste Schlag basierend auf echten Daten
# zurückgegeben werden

import pandas as pd
import random

class Bot:

    SERVE_DIRECTION = ["4", "5", "6"]
    EVERY_SHOT_TYPE = ["f", "b", "r", "s", "v", "z", "o", "p", "y", "l", "m", "h", "i", "j", "k", "t"]
    RETURN_SHOT_TYPES = ["f", "b", "r", "s", "y", "l", "m", "h", "i", "t"]
    RETURN_DEPTH = ["7", "8", "9"]
    DIRECTIONS = ["1", "2", "3"]
    RALLEY_ERROR = ["n", "w", "d", "x"]
    ERROR_TYPE = ["@", "#"]
    WINNER = "*"
    WINNER_PROBA = 15
    ERROR_PROBA = 15

    def __init__(self, name="", turn=False):
        self.name = name
        self.turn = turn

    def import_data():
        # get the dataset and make it into a pandas dataframe 
        # that can be operated on
        df = pd.read_csv(r"C:\Users\carlo\TrainingsTool\Tennis\Datasets\charting-m-points-from-2017-new.csv", 
                         low_memory=False, 
                         encoding= 'unicode_escape')
        
        # 14 and 15 are the columns that have the ralley sequences in them
        df_new = df.iloc[:,14:16]
        print(df_new.head(10))
        print(len(df_new))

    def add_shot(self, ralley):
        # ToDo return the next shot based on the ralley and the data
        shot = 42
        ralley.add_shot_to_ralley(shot)
        print(ralley.get_ralley())

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

        # If shot count in that ralley is 1, add a return
        elif ralley.get_shot_count() == 1:
            # Add valid return stroke including depth encoding
            shot = randomReturnType + randomReturnDirection
            # Add winner and error probabilities on return
            if i < self.WINNER_PROBA:
                shot = shot + randomReturnDepth + self.WINNER
            elif i > 99 - self.ERROR_PROBA:
                shot = shot + randomRalleyError + randomErrorType
            else: shot = shot + randomReturnDepth

        # Otherwise just add random shots
        else:
            # Add any shot after the return shot
            shot = randomShotType + randomShotDirection
            # Add winner and error probabilities
            if i < self.WINNER_PROBA:
                shot = shot + self.WINNER
            elif i > 99 - self.ERROR_PROBA:
                shot = shot + randomRalleyError + randomErrorType
        
        # Add that shot to the ralley
        ralley.add_shot_to_ralley(shot)
        print(ralley.get_ralley())

    def set_turn(self, bool_var):
        self.turn = bool_var

    def get_turn(self):
        return self.turn