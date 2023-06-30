class Ralley:
    def __init__(self, ralley=[]):
        self.ralley = ralley

    def update_ralley(self, current_shot):
        self.ralley.append(current_shot)

    def clear_ralley(self):
        self.ralley.clear()

    def get_ralley(self):
        return self.ralley
    
    def get_len_ralley(self):
        return self.ralley.len()