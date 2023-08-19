

class Scoring:

    RALLEY_ERROR = ["n", "w", "d", "x"]
    ERROR_TYPE = ["@", "#"]
    WINNER = ["*"]
    set_scores = []
    sets_count = 0

    def __init__(self, points_A, games_A, sets_A, points_B, games_B, sets_B, score, serving_player="bottom_player"):
        self.points_A = points_A
        self.games_A = games_A
        self.sets_A = sets_A
        self.points_B = points_B
        self.games_B = games_B
        self.sets_B = sets_B
        self.score = score
        self.serving_player = serving_player

        self.points_A = 0
        self.points_B = 0
    
    def get_score(self):
        
        score = str(self.points_A) + "-" + str(self.points_B) 
        
        if self.games_A != 0 or self.games_B != 0:
            score =  str(self.games_A) + "-" + str(self.games_B) + ", " + score

        if self.sets_count > 0:  
            score =  str(self.set_scores) + score
        
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

        if self.games_A == 6 and self.games_B == 6:
            if player == 1:
                self.points_A += 1
                if self.points_A > 6 and self.points_A - self.points_B >= 2:
                    self.give_game(1)
                    self.points_A = 0
                    self.points_B = 0
            elif player == 2:
                self.points_B += 1
                if self.points_B > 6 and self.points_B - self.points_A >= 2:
                    self.give_game(2)
                    self.points_A = 0
                    self.points_B = 0
            
        else:
            if player == 1:
                # depending on the own points and the opponents points, the score in a gme is updated
                if self.points_A == 0:
                    self.points_A = 15
                elif self.points_A == 15:
                    self.points_A = 30
                elif self.points_A == 30:
                    self.points_A = 40
                elif self.points_A == 40 and self.points_B == "AD":
                    self.points_B = 40
                elif self.points_A == 40 and self.points_B == 40:
                    self.points_A = "AD"
                else:
                    self.give_game(1)
                    self.points_A = 0
                    self.points_B = 0

            if player == 2:
                # depending on the own points and the opponents points, the score in a gme is updated
                if self.points_B == 0:
                    self.points_B = 15
                elif self.points_B == 15:
                    self.points_B = 30
                elif self.points_B == 30:
                    self.points_B = 40
                elif self.points_B == 40 and self.points_A == "AD":
                    self.points_A = 40
                elif self.points_B == 40 and self.points_A == 40:
                    self.points_B = "AD"
                else:
                    self.give_game(2)
                    self.points_A = 0
                    self.points_B = 0

    def give_game(self, player):
        # updates the score in a set
        if player == 1:
            # if player a leads by 2 games in a set and both players game count in a set is 5 or smaller, 
            # just add a game to the player who won the game
            if self.games_A < 6: 
                self.games_A += 1
                # When a player gets his 6th game in a set and has a lead by 2 games with that, he wins the set
                if self.games_A == 6 and self.games_A - self.games_B >= 2:
                    self.give_set(1, self.games_A, self.games_B)
                    self.games_A = 0
                    self.games_B = 0

            elif self.games_A == 6 and self.games_B == 5:
                self.games_A += 1
                self.give_set(1, self.games_A, self.games_B)
                self.games_A = 0
                self.games_B = 0

            elif self.games_A == 6 and self.games_B == 6:
                self.games_A += 1
                self.give_set(1, self.games_A, self.games_B)
                self.games_A = 0
                self.games_B = 0
        
        elif player == 2:
            # if player a leads by 2 games in a set and both players game count in a set is 5 or smaller, 
            # just add a game to the player who won the game
            if self.games_B < 6: 
                self.games_B += 1
                # When a player gets his 6th game in a set and has a lead by 2 games with that, he wins the set
                if self.games_B == 6 and self.games_B - self.games_A >= 2:
                    self.give_set(2, self.games_A, self.games_B)
                    self.games_A = 0
                    self.games_B = 0
              
            elif self.games_B == 6 and self.games_A == 5:
                self.games_B += 1
                self.give_set(2, self.games_A, self.games_B)
                self.games_A = 0
                self.games_B = 0
            
            elif self.games_B == 6 and self.games_A == 6:
                self.games_B += 1
                self.give_set(2, self.games_A, self.games_B)
                self.games_A = 0
                self.games_B = 0

    def give_set(self, player, games_A, games_B):
        
        self.sets_count += 1
        self.set_scores.append(str(games_A) + "-" + str(games_B) + " ")
        if player == 1:
            self.sets_A += 1
        elif player == 2:
            self.sets_B += 1

    def set_serving_player(self, player):
        self.serving_player = player

    def get_serving_player(self):
        return self.serving_player