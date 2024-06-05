import constants as const
from datetime import datetime

class Scoring:
    '''In this class the whole scoring process for points, games and 
    sets is implemented'''
    RALLY_ERROR = const.ShotEncodings.RALLY_ERROR
    ERROR_TYPE = const.ShotEncodings.ERROR_TYPE
    WINNER = const.ShotEncodings.WINNER
    set_scores = []
    sets_count = 0
    point_count_per_game = 0
    sets_to_play = const.MenuVariables.sets_to_play
    matches_played = 0

    def __init__(self, points_A, games_A, sets_A, points_B, games_B, 
                 sets_B, score, serving_player=1):
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
        self.point_count_per_game = 0
        self.games_A = 0
        self.games_B = 0
        self.sets_A = 0
        self.sets_B = 0

        self.a_wins = 0
        self.b_wins = 0
    
    def get_score(self):
        # Score is returned in a string, depending on how far we are in 
        # the set (only exising points, games and sets are displayed)
        score = str(self.points_A) + "-" + str(self.points_B) 
        
        if self.games_A != 0 or self.games_B != 0:
            score =  str(self.games_A) + "-" + str(self.games_B) + ", " + score

        if self.sets_count > 0:
            score =  str(self.set_scores) + score
        
        return score
    
    def get_points_A(self):
        return self.points_A
    
    def get_points_B(self):
        return self.points_B
    
    def get_games_A(self):
        return self.games_A
    
    def get_games_B(self):
        return self.games_B
    
    def get_sets_A(self):
        return self.sets_A
    
    def get_sets_B(self):
        return self.sets_B
    
    def get_set_count(self):
        return self.sets_count
    
    def get_match_count(self):
        return self.matches_played
    
    def update_point_count_per_game(self, x):
        self.point_count_per_game += x

    def get_point_count_per_game(self):
        return self.point_count_per_game
    
    def reset_point_count_per_game(self):
        self.point_count_per_game = 0
    
    def update_points(self, rally, last_char, shot_count):
        
        # if bottom player (1) was serving
        if self.get_serving_player() == 1:
            # Modulo of shotcount = 0 means that the terminal shot was 
            # done by player 2
            if shot_count % 2 == 0:
                # If that shot was an error, player 1 gets a point
                if (last_char in self.ERROR_TYPE 
                    or last_char in self.RALLY_ERROR):
                    self.give_point(1)
                # If that shot was a winner, player 2 gets that point
                elif last_char in self.WINNER:
                    self.give_point(2)
            # Modulo of shotcount = 1 means, that the terminal shot was 
            # done by player 1        
            elif shot_count % 2 == 1:
                # If that shot was an error, player 2 gets a point
                if (last_char in self.ERROR_TYPE 
                    or last_char in self.RALLY_ERROR):
                    self.give_point(2)
                # If that shot was a winner, player 2 gets that point
                elif last_char in self.WINNER:
                    self.give_point(1)
        
        # if top player (2) was serving
        elif self.get_serving_player() == 2:
            # Modulo of shotcount = 0 means that the terminal shot was 
            # done by player 1
            if shot_count % 2 == 0:
                # If that shot was an error, player 2 gets a point
                if (last_char in self.ERROR_TYPE 
                    or last_char in self.RALLY_ERROR):
                    self.give_point(2)
                # If that shot was a winner, player 1 gets that point
                elif last_char in self.WINNER:
                    self.give_point(1)
            # Modulo of shotcount = 1 means, that the terminal shot was 
            # done by player 2
            elif shot_count % 2 == 1:
                # If that shot was an error, player 1 gets a point
                if (last_char in self.ERROR_TYPE 
                    or last_char in self.RALLY_ERROR):
                    self.give_point(1)
                # If that shot was a winner, player 2 gets that point
                elif last_char in self.WINNER:
                    self.give_point(2)

    def give_point(self, player):
        # Point is given so point count per game is updated
        self.update_point_count_per_game(1)

        # When there is a tiebreak, points are added according to 
        # tiebreak rules
        if self.games_A == 6 and self.games_B == 6:
            if player == 1:
                self.points_A += 1
                # When a player has more than 6 points and is leading by
                #  two points, he won the tiebreak
                if (self.points_A > 6 
                    and self.points_A - self.points_B >= 2):
                    self.give_game(1)
                    self.points_A = 0
                    self.points_B = 0
                # The serving player switches after every 2 points when 
                # the sum of the score in the tiebreak is odd
                elif (self.points_A + self.points_B) % 2 == 1:
                    self.switch_serving_player()
            elif player == 2:
                self.points_B += 1
                # When a player has more than 6 points and is leading by
                #  two points, he won the tiebreak
                if self.points_B > 6 and self.points_B - self.points_A >= 2:
                    self.give_game(2)
                    self.points_A = 0
                    self.points_B = 0
                elif (self.points_A + self.points_B) % 2 == 1:
                    self.switch_serving_player()

        # If there is no tiebreak, points are given according to 15, 30,
        # 40, game rules    
        else:
            if player == 1:
                # depending on the own points and the opponents points, 
                # the score in a gme is updated
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
                # depending on the own points and the opponents points, 
                # the score in a gme is updated
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
        const.Changing.rally_terminated = True

    def give_game(self, player):
        # When this is called, the server has to be switched
        
        self.switch_serving_player()
        # When a game is finished, the points per game count has to be 
        # reset
        self.reset_point_count_per_game()
        # Updates the score in a set
        if player == 1:
            # if player a leads by 2 games in a set and both players 
            # game count in a set is 5 or smaller, 
            # just add a game to the player who won the game
            if self.games_A < 6: 
                self.games_A += 1
                # When a player gets his 6th game in a set and has a 
                # lead by 2 games with that, he wins the set
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
            # if player a leads by 2 games in a set and both players 
            # game count in a set is 5 or smaller, 
            # just add a game to the player who won the game
            if self.games_B < 6: 
                self.games_B += 1
                # When a player gets his 6th game in a set and has a 
                # lead by 2 games with that, he wins the set
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
        # The set score is appended to the score list and set_count is 
        # updated and set per player is updated for the player who won 
        # the point
        self.sets_count += 1
        self.set_scores.append(str(games_A) + "-" + str(games_B) + " ")
        if player == 1:
            self.sets_A += 1
        elif player == 2:
            self.sets_B += 1
        
        # print statements for the Terminal
        if const.MenuVariables.sets_to_play == 3:
            if self.sets_A == 2:
                print("Player A / Bottom Bot wins!")
                self.a_wins += 1
                self.matches_played += 1
                self.reset_score()
            elif self.sets_B == 2:
                print("Player B / Top Bot wins!")
                self.b_wins += 1
                self.matches_played += 1
                self.reset_score()
        elif const.MenuVariables.sets_to_play == 5:
            if self.sets_A == 3:
                print("Player A / Bottom Bot wins!")
                self.a_wins += 1
                self.matches_played += 1
                self.reset_score()
            elif self.sets_B == 3:
                print("Player B / Top Bot wins!")
                self.b_wins += 1
                self.matches_played += 1
                self.reset_score()

    def switch_serving_player(self):
        # The serving player changes, because they switch after each
        # game
        if self.get_serving_player() == 1:
            self.set_serving_player(2)
        else:
            self.set_serving_player(1)

    def set_serving_player(self, player):
        self.serving_player = player

    def get_serving_player(self):
        return self.serving_player
    
    def get_point_count_per_game(self):
        return self.point_count_per_game
    
    def reset_score(self):
        print("---------------------------------------------")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        print("Match: " + str(self.matches_played) + " / " + str(const.MenuVariables.simu_matches) + " is over.")
        print("Score: " + str(self.set_scores))
        print("A(Bottom Bot)-wins: " + str(self.a_wins))
        print("B(Top Bot)-wins: " + str(self.b_wins))
        self.score = ""
        self.sets_count = 0
        self.set_scores.clear()
        self.points_A = 0
        self.points_B = 0
        self.games_A = 0
        self.games_B = 0
        self.sets_A = 0
        self.sets_B = 0