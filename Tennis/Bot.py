# hier soll eine ralley reingegeben werden 
# und dann soll der nächste Schlag basierend auf echten Daten
# zurückgegeben werden

import pandas as pd

class Bot:
    def __init__(self, name=""):
        self.name = name

    def get_next_shot(ralley):
        # ToDo return the next shot based on the ralley and the data
        ...

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