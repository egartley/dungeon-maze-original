import os
import time
import math

class Score:
    def __init__(self, name):
        self.start_t = time.time()
        self.end_t = time.time()
        self.different_t = 0
        self.player_score = 0
        self.kill_count = 0
        self.is_no_write = True
        self.total = 0
        self.name = name
        self.topScores = []
        self.min_score = 0
        self.max_score = 0
        

    def get_path(self):
        absolute_path = os.path.dirname(__file__)
        absolute_path = absolute_path.replace("src", "")
        relative_path = "topScores.txt"
        full_path = os.path.join(absolute_path, relative_path)
        return full_path

    def cal_score(self):
        if self.player_score == 0:
            self.player_score = math.ceil((self.kill_count * 100) + (self.total * .5) + 1000)

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
      self.start_t = time.time()
        
    def end_time(self):
        self.end_t = time.time()
        self.total += self.end_t - self.start_t
    
    def determine_writability(self):
        full_path = self.get_path()
        with open(full_path) as f:
            lines = f.readlines()
        lst = []
        for i in range(len(lines)):
            if i != 0:
                lst.append(lines[i].split())
        self.top_scores = lst
        self.max_score = self.top_scores[0][1]
        self.min_score = self.top_scores[9][1]
        
        if self.player_score > self.min_score:
            if self.player_score < self.max_score:
                i = 0
                for i in range(1,8):
                    if self.player_score > self.top_scores[1]:
                        break
                push_incrementor = len(self.top_scores) - i + 1
                for k in range (0,push_incrementor):
                    tmp = self.top_scores[i]
                    if k == 0:
                        pass
                        
                    
            elif self.player_score == self.max_score:
                other_scores = self.top_scores[1:8]
                row = [self.name, str(self.player_score), str(self.total), str(self.kill_count),str(os.date, time.time())]
                tmp_list = self.top_scores[0] + row + other_scores
                self.topScores = tmp_list
        else:
            pass
                
            
            

    def update_kill(self):
        self.kill_count += 1

    
