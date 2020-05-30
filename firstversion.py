import numpy as np
import matplotlib.pyplot as plt
import math
import random
from datetime import datetime
class personne:
    def __init__(self,x,y,status="healthy",hygiene=1,mask=False,walk_range=500):
        self.x = x
        self.y = y
        self.status = status
        self.hygiene = hygiene
        self.mask = mask
        self.walk_range=walk_range
    def change_status(self,s):
        self.status = s
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_status(self):
        return str(self.status)
    def get_distance(self,other):
        temp_x = (self.get_x()-other.get_x())**2
        temp_y = (self.get_y()-other.get_y())**2
        return math.sqrt(temp_x+temp_y)
    def update_x(self,new_x):
        self.x = new_x
    def update_y(self,new_y):
        self.y=new_y
    def update_pos(self):
        r1= random.uniform(-1,1)
        r2 = random.uniform(-1,1)
        self.update_x(int(self.x + r1*self.walk_range))
        self.update_y(int(self.y+r2*self.walk_range))
    def get_hygiene(self):
        return self.hygiene
    def get_contamined(self,other):
        if (self.get_distance(other) <=2 and other.get_status == "sick"):
            r1 = random.uniform(0,1)*self.hygiene*other.hygiene
            if (other.mask and self.mask):
                if (r1<0.05):
                    self.change_status("sick")
            elif (other.mask and not self.mask):
                if (r1<0.12):
                    self.change_status("sick")
            elif (self.mask):
                if (r1<0.2):
                    self.change_status("sick")
            else :
                if (r1<0.3):
                    self.change_status("sick")
                                    
c = np.array([personne(0,0,"healthy"),personne(5,5,"sick"),personne(10,10,"healthy")])
for i in range(len(c)):
    for j in range(i+1,len(c)):
        print(c[i].get_distance(c[j]))
