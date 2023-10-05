import constants as const
import scoring
import random

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
        i = random.randint(0, 9999)
        x = score.get_point_count_per_game()
        #print(x)
        shot = "123"
        if (current_ralley.get_shot_count() == "0"):
            # Add a first serve
            ...
        elif (current_ralley.get_shot_count() == "1" 
              and current_ralley.get_last_char_of_last_shot() == ","):
            # Add Second Serve
            ...
        current_ralley.add_shot_to_ralley(shot)
        print(current_ralley.get_ralley())

    def set_turn(self, bool_var):
        self.turn = bool_var

    def get_turn(self):
        return self.turn