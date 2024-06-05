import scoring
import ball
import constants as const

class Rally:
    '''This class keeps track of the rally and also calls the scoring 
    class, when a rally is finished'''
    # Initializing the encodings for the shots, so we can see if a shot 
    # terminates a rally
    RALLY_ERROR = const.ShotEncodings.RALLY_ERROR
    ERROR_TYPE = const.ShotEncodings.ERROR_TYPE
    WINNER = const.ShotEncodings.WINNER
    SECOND_SERVE = const.ShotEncodings.SECOND_SERVE
    LAST_RALLY = []

    def __init__(self, rally=[], shot_count=0):
        self.rally = rally
        self.shot_count = shot_count

    def add_shot_to_rally(self, current_shot):
        # This function just adds a given shot to the current rally
        self.rally.append(current_shot)
        self.shot_count += 1

    def clear_rally(self):
        # This function resets the rally and gets called after a rally 
        # is won by a player/bot
        self.shot_count = 0
        self.rally.clear()

    def get_rally(self):
        # returns the current rally
        return self.rally
    
    def get_len_rally(self):
        # returns the length of a rally
        return len(self.rally)
    
    def remove_last_n_elements_of_rally(self, n):
        # n is the number of elements to keep
        x = len(self.rally) - n
        del self.rally[-x:]
    
    def set_last_rally(self, rally):
        self.LAST_RALLY = rally

    def remove_last_shot(self):
        del self.rally[-1]

    def get_last_rally(self):
        return self.LAST_RALLY

    def get_shot_count(self):
        # returns the shot count
        return self.shot_count
    
    def get_first_shot_of_rally(self):
        r = self.get_rally()
        second_to_last_shot = r[0]
        return second_to_last_shot
    
    def get_last_shot(self):
        r = self.get_rally()
        return r[len(r)-1]
    
    def get_last_char_of_last_shot(self):
        # this is called in score_update and returns 
        # the last char of the last shot of the current rally
        r = self.get_rally()

        # last_shot is the last element of the current rally
        last_shot = r[len(r)-1]
        # last_char is the last element of the last_shot 
        last_char = last_shot[len(last_shot)-1]
        return last_char

    def return_shot_at_pos(self, pos):
        '''Returns the shot enconding at a given position of a rally'''
        return str(self.rally[pos])

    def score_update(self, score, current_ball):
        # If the last char in rally is a terminal shot,
        # add a point to the score accordingly
        
        c = self.get_last_char_of_last_shot()
        serving_player = scoring.Scoring.get_serving_player(score)
        point_count_in_game = scoring.Scoring.get_point_count_per_game(score)

        if c in self.SECOND_SERVE and len(self.rally) == 1:
            self.shot_count = 0
            ball.Ball.reset_ball(current_ball, 
                                 serving_player, 
                                 point_count_in_game)
       
        if c in self.RALLY_ERROR or c in self.ERROR_TYPE or c in self.WINNER:
            
            score.update_points(self.rally, c, self.get_shot_count())
            # update Score, dependent on who is serving
            self.set_last_rally(self.get_rally())
            const.Changing.rally = list(self.get_last_rally())
            self.clear_rally()
            # After every rally, the ball is put to the position, 
            # where the next player has to serve from
            
            # This is the amount of points in that game, even: next
            # serve from Deuce side, odd: next serve from Ad Side
            point_count_in_game = scoring.Scoring.get_point_count_per_game(
                score)
            # This is the player who is serving during the ongoing game 
            serving_player = scoring.Scoring.get_serving_player(score)
            ball.Ball.reset_ball(current_ball, 
                                 serving_player, 
                                 point_count_in_game)