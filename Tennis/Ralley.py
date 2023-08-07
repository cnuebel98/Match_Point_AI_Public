
class Ralley:
    
    # ToDo: Initialized the encodings for the shots, so we can see if a shot terminates a ralley
    RALLEY_ERROR = ["n", "w", "d", "x"]
    ERROR_TYPE = ["@", "#"]
    WINNER = ["*"]

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
        return self.ralley.len()
    
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

    def score_update(self):
        # If the last char in ralley is a terminal shot, 
        # add a point to the score accordingly
        
        #print(self.get_shot_count())
        c = self.get_last_char_of_last_shot()
        #print(c)

        if c in self.RALLEY_ERROR or c in self.ERROR_TYPE:
            print("yes, bot error")
            # ToDo: update Score
            self.clear_ralley()
        elif c in self.WINNER:
            print("BotWinner")
            # ToDo: Update Score
            self.clear_ralley()
    