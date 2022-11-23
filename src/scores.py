import copy
import os
import time
import math



class Score:
    def __init__(self, name,dif):
        self.start_t = time.time()
        self.end_t = time.time()
        self.different_t = 0
        self.player_score = 0
        self.kill_count = 0
        self.is_no_write = True
        self.read = True
        self.total = 0
        self.name = name
        self.topScores = self.read_score()
        self.min_score = 0
        self.max_score = 0
        self.string_lst = [None] * 12
        self.total_multiplier = 0
        if dif == 2:
            self.total_multiplier = .75
        elif dif == 1:
            self.total_multiplier = .6
        else:
            self.total_multiplier = .45
        
        

    def get_path(self):
        absolute_path = os.path.dirname(__file__)
        absolute_path = absolute_path.replace("src", "")
        relative_path = "topScores.txt"
        full_path = os.path.join(absolute_path, relative_path)
        return full_path

    def cal_score(self):
        if self.player_score == 0:
            self.player_score = math.ceil((self.kill_count * 100) + (self.total * self.total_multiplier) + 1000)

    def read_score(self):
        if self.read:
            self.read = False
            full_path = self.get_path()
            with open(full_path,'r') as f:
                lines = f.read().split("\n")
                for i in range(0, len(lines) - 1):
                    print(i)
                    lines[i] = lines[i].split(',')
                    print('now equals')
                    print(lines[i])
                f.close()
            
            self.top_scores = copy.deepcopy(lines)
            

    def start_time(self):
      self.start_t = time.time()
      
    def end_time(self):
        self.end_t = time.time()
        self.total += self.end_t - self.start_t
    
    def determine_writability(self):
        
        
        self.max_score = int(self.top_scores[1][1])
        self.min_score = int(self.top_scores[10][1])
        
        if self.player_score < int(self.min_score):
            pass
        else:
            for i in range(1,10):
                if self.player_score > int(self.top_scores[i][1]):
                    break
            row = [self.name, str(self.player_score), str(time.strftime("%H:%M:%S", time.gmtime(self.total))), str(self.kill_count),str(time.ctime(time.time()))]
            self.top_scores.insert(i,row)      
            print(self.top_scores)
            
            
            
            with open('topScores.txt','w',) as file: 
                file.writelines(tmp)
                file.close()
            
    def update_kill(self):
        self.kill_count += 1

    
