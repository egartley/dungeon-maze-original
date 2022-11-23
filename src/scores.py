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
        full_path = self.get_path()
        lst = []
        with open(full_path,'r') as f:
            lines = f.readlines()
            i = 0
            for i in range(len(lines)):
                one_line = lines[i]
                lst.append(one_line.split(' '))
                i+=1
            f.close()
        self.top_scores = copy.deepcopy(lst)

    def start_time(self):
      self.start_t = time.time()
      
    def end_time(self):
        self.end_t = time.time()
        self.total += self.end_t - self.start_t
    
    def determine_writability(self):
        self.max_score = int(self.top_scores[1][1])
        self.min_score = int(self.top_scores[10][1])
        
        if self.player_score > int(self.min_score):
            if self.player_score < int(self.max_score):
                flag = False
                for i in range(1,11):
                    if i == 0:
                        pass
                    elif self.player_score > int(self.top_scores[i][1]):
                        flag = True
                        break
                   
                if flag:        
                    row = [self.name, str(self.player_score), str(time.strftime("%H:%M:%S", time.gmtime(self.total))), str(self.kill_count),str(time.ctime(time.time()))]
                    self.top_scores.insert(i, row)
            elif self.player_score == int(self.max_score):
                row = [self.name, str(self.player_score), str(time.strftime("%H:%M:%S", time.gmtime(self.total))), str(self.kill_count),str(time.ctime(time.time()))]
                self.top_scores.insert(0, row)
        else:
            pass
        i = 0
        k = 0
        l = len(self.top_scores)
        if l > 11:
            l = 11
        tmp = ['0'] * l
        for i in range(l):
            string = ""
            for k in range (len(self.top_scores[i])):
                string += str(self.top_scores[i]) + " "
                
                k+=1
            tmp[i] = string
            i+=1
        with open('topScores.txt','w',) as file: 
            file.writelines(tmp)
            file.close()
            
    def update_kill(self):
        self.kill_count += 1

    
