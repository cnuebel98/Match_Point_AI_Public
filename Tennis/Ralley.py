import scoring
import ball

class Ralley:
    
    # Initializing the encodings for the shots, so we can see if a shot terminates a ralley
    RALLEY_ERROR = ["n", "w", "d", "x"]
    ERROR_TYPE = ["@", "#"]
    WINNER = ["*"]
    SECOND_SERVE = [","]

    def __init__(self, ralley=[], shot_count=0):
        self.ralley = ralley
        self.shot_count = shot_count

    def add_shot_to_ralley(self, current_shot):
        # This function just adds a given shot to the current ralley
        self.ralley.append(current_shot)
        self.shot_count += 1

    def clear_ralley(self):
        # This function resets the ralley and gets called after a ralley is won by a player/bot
        self.shot_count = 0
        self.ralley.clear()

    def get_ralley(self):
        # returns the current ralley
        return self.ralley
    
    def get_len_ralley(self):
        # returns the length of a ralley
        return len(self.ralley)
    
    def get_shot_count(self):
        # returns the shot count
        return self.shot_count
    
    def get_last_char_of_last_shot(self):
        # this is called in score_update and returns 
        # the last char of the last shot of the current ralley
        r = self.get_ralley()

        # last_shot is the last element of the current ralley
        last_shot = r[len(r)-1]
        # last_char is the last element of the last_shot 
        last_char = last_shot[len(last_shot)-1]
        return last_char

    def score_update(self, score, current_ball):
        # If the last char in ralley is a terminal shot, 
        # add a point to the score accordingly
        
        c = self.get_last_char_of_last_shot()
        serving_player = scoring.Scoring.get_serving_player(score)
        point_count_in_game = scoring.Scoring.get_point_count_per_game(score)

        if c in self.SECOND_SERVE and len(self.ralley) == 1:
            self.shot_count = 0
            ball.Ball.reset_ball(current_ball, serving_player, point_count_in_game)
       
        if c in self.RALLEY_ERROR or c in self.ERROR_TYPE or c in self.WINNER:
            # print("Ralley Terminated")
            score.update_points(self.ralley, c, self.get_shot_count())
            # update Score, dependent on who is serving

            self.clear_ralley()
            # After every ralley, the ball is put to the position, where the next player has to serve from
            # This is the player who is serving during the ongoing game
            
            # This is the amount of points in that game, even: next serve from Deuce side, odd: next serve from Ad Side
            point_count_in_game = scoring.Scoring.get_point_count_per_game(score)
            serving_player = scoring.Scoring.get_serving_player(score)
            ball.Ball.reset_ball(current_ball, serving_player, point_count_in_game)