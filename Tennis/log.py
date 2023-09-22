import constants as const
import pandas as pd

class Log:
    '''The Ralleys, the points and the setting of the match is logged
    and saved if it was chosen to save the data'''
    logging_enabled = const.MenuVariables.logging
    def __init__(self):
        self.df = pd.DataFrame(columns=['Points_A', 'Points_B', 
                                   'Games_A', 'Games_B',
                                   'Sets_A', 'Sets_B', 'Serving_Player', 
                                   'Ralley'])
    
    def add_score_to_df(self, points_A, points_B, games_A, games_B, sets_A, 
                        sets_B, serving_player, ralley):
        
        if points_A == "AD":
            points_A = 50
        if points_B == "AD":
            points_B = 50

        new_row = pd.DataFrame({'Points_A': points_A,
                   'Points_B': points_B,
                   'Games_A': games_A,
                   'Games_B': games_B,
                   'Sets_A': sets_A,
                   'Sets_B': sets_B,
                   'Serving_Player': serving_player,
                   'Ralley': str(ralley)}, index = [1])
        self.df = pd.concat([self.df.loc[:], new_row]).reset_index(drop=True)
        self.show_df()
        
    def show_df(self):
        print(self.df)

    def add_ralley_to_df(self, ralley):
        ...

    def export_to_csv(df):
        # Data is saved and exported in a csv file
        df.to_csv("results_simulation.csv")