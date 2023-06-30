class Ralley:
    def __init__(self, ralley=[], shot_count=0):
        self.ralley = ralley
        self.shot_count = shot_count

    def add_shot_to_ralley(self, current_shot):
        self.ralley.append(current_shot)
        self.shot_count += 1

    def clear_ralley(self):
        self.ralley.clear()

    def get_ralley(self):
        return self.ralley
    
    def get_len_ralley(self):
        return self.ralley.len()
    
    def get_shot_count(self):
        return self.shot_count