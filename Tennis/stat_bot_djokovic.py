import constants as const
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

    def add_shot(self, current_ralley):
        '''Adds the most likely shot based on djokovic data'''
        i = random.randint(0, 99)
        shot = "123"
        current_ralley.add_shot_to_ralley(shot)
        print(current_ralley.get_ralley())

    def set_turn(self, bool_var):
        self.turn = bool_var

    def get_turn(self):
        return self.turn