

class Scoring:

    RALLEY_ERROR = ["n", "w", "d", "x"]
    ERROR_TYPE = ["@", "#"]
    WINNER = ["*"]

    def __init__(self, points_A, games_A, sets_A, points_B, games_B, sets_B, score, serving_player="bottom_player"):
        self.points_A = points_A
        self.games_A = games_A
        self.sets_A = sets_A
        self.points_B = points_B
        self.games_B = games_B
        self.sets_B = sets_B
        self.score = score
        self.serving_player = serving_player
    
    def get_score(self):
        
        
        score = str(self.points_A) + "-" + str(self.points_B) #+ ", " + str(self.games_A) + "-" + str(self.games_B)
        
        return score
    
    def update_points(self, ralley, last_char, shot_count):
        #print(ralley)
        #print(shot_count)
        #print(self.get_serving_player())
        #print(last_char)

        # if bottom player (1) was serving
        if self.get_serving_player() == 1:
            # Modulo of shotcount = 0 means that the terminal shot was done by player 2
            if shot_count % 2 == 0:
                # If that shot was an error, player 1 gets a point
                if last_char in self.ERROR_TYPE or last_char in self.RALLEY_ERROR:
                    self.give_point(1)
                # If that shot was a winner, player 2 gets that point
                elif last_char in self.WINNER:
                    self.give_point(2)
            # Modulo of shotcount = 1 means, that the terminal shot was done by player 1        
            elif shot_count % 2 == 1:
                # If that shot was an error, player 2 gets a point
                if last_char in self.ERROR_TYPE or last_char in self.RALLEY_ERROR:
                    self.give_point(2)
                # If that shot was a winner, player 2 gets that point
                elif last_char in self.WINNER:
                    self.give_point(1)
        
        # if top player (2) was serving
        elif self.get_serving_player() == 2:
            # Modulo of shotcount = 0 means that the terminal shot was done by player 1
            if shot_count % 2 == 0:
                # If that shot was an error, player 2 gets a point
                if last_char in self.ERROR_TYPE or last_char in self.RALLEY_ERROR:
                    self.give_point(2)
                # If that shot was a winner, player 1 gets that point
                elif last_char in self.WINNER:
                    self.give_point(1)
            # Modulo of shotcount = 1 means, that the terminal shot was done by player 2        
            elif shot_count % 2 == 1:
                # If that shot was an error, player 1 gets a point
                if last_char in self.ERROR_TYPE or last_char in self.RALLEY_ERROR:
                    self.give_point(1)
                # If that shot was a winner, player 2 gets that point
                elif last_char in self.WINNER:
                    self.give_point(2)

    def give_point(self, player):
        if player == 1:
            self.points_A += 1
            print("bottom player won the point")
        if player == 2:
            self.points_B += 1
            print("top player won the point")

    def set_serving_player(self, player):
        self.serving_player = player

    def get_serving_player(self):
        return self.serving_player