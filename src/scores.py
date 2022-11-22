import os
import time

class Score:
    def __init__(self, name):
        self.start_t = 0
        self.end_t = 0
        self.different_t = 0
        self.player_score = 0
        self.kill_count = 0
        self.is_no_write = True
        self.total = 0
        self.name = name
        

    def get_path(self):
        absolute_path = os.path.dirname(__file__)
        absolute_path = absolute_path.replace("src", "")
        relative_path = "topScores.txt"
        full_path = os.path.join(absolute_path, relative_path)
        return full_path

    def cal_score(self):
        if self.player_score == 0:
            self.player_score = (self.kill_count * 100) - (self.different_t) + 1000
            print(self.different_t)

    def read_score(self):
        full_path = self.get_path()
        with open(full_path) as f:
            lines = f.readlines()
        lst = []
        for i in range(len(lines)):
            lst.append(lines[i].split())
        return lst

    def write_score(self, my_score):
        full_path = self.get_path()
        if self.is_no_write:
            with open(full_path, "a") as f:
                f.write(my_score)
            self.is_no_write = False

    def start_time(self):
        if self.start_t == 0:
            self.start_t = time.time()
        
    def end_time(self):
        if self.end_t == 0:
            self.end_t = time.time()
            self.total += self.end_t - self.start_t
            self.start_t = 0
            self.end_t = 0
            

    def update_kill(self):
        self.kill_count += 1

    
