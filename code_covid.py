# -*- coding: utf-8 -*-
"""
Created on Sat May 30 17:48:57 2020

@author: myria
"""
#%%
# =============================================================================
# IMPORTATIONS
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import math
import random
from datetime import datetime
from celluloid import Camera
from joblib import Parallel, delayed
from scipy import signal

#%%
# =============================================================================
# CLASSES & FUNCTIONS
# =============================================================================

class personne:
    def __init__(self, x, y, status="healthy", hygiene = 1, mask = False, walk_range = 50):
        self.x = x
        self.y = y
        self.status = status
        self.hygiene = hygiene
        self.mask = mask
        self.walk_range = walk_range
        
    def change_status(self, s):
        self.status = s
        
    def get_x(self):
        return self.x
        
    def get_y(self):
        return self.y
        
    def get_status(self):
        return str(self.status)
        
    def get_distance(self, other):
        temp_x = (self.get_x() - other.get_x())**2
        temp_y = (self.get_y() - other.get_y())**2
        return math.sqrt(temp_x + temp_y)
        
    def update_x(self, new_x):
        self.x = new_x
        
    def update_y(self, new_y):
        self.y = new_y
         
    def update_pos(self):
        r1 = random.uniform(-1, 1)
        r2 = random.uniform(-1, 1)
        self.update_x(int(self.x + r1*self.walk_range))
        self.update_y(int(self.y + r2*self.walk_range))
        
    def get_hygiene(self):
        return self.hygiene
        
    def get_contamined(self, other):
        if (self.get_distance(other) <= 10 and other.get_status() == "sick"):
            r1 = random.uniform(0, 1) #*self.hygiene*other.hygiene

            if (other.mask and self.mask):
                if (r1 < 0.05):
                    self.change_status("sick")
            elif (other.mask and not self.mask):
                if (r1 < 0.12):
                    self.change_status("sick")
            elif (self.mask):
                if (r1 < 0.2):
                    self.change_status("sick")
            else :
                if (r1 < 0.6):
                    self.change_status("sick")

#%%
# =============================================================================
# HYGIENE FUNCTION
# =============================================================================

x = np.linspace(0, 20, 1000)
y = 9*np.cos(.1*x)**2 + 1
min_y = np.argmin(y)
y = y[:min_y]
x = x[:min_y]

x_monte = np.linspace(max(x), 18, 1000)
y_monte = 9*np.sin(2*x_monte)**2 + 1

max_y = np.argmax(y_monte)
y_monte = y_monte[:max_y]
x_monte = x_monte[:max_y]

xx = np.concatenate((x, x_monte))
yy = np.concatenate((y, y_monte))

plt.plot(xx, yy)

#%%
# =============================================================================
# GLOBAL PARAMETERS
# =============================================================================

niter = 300
npersonne = 500
frac_healthy = 0.9
size = 1000

#%%
# =============================================================================
# MAIN
# =============================================================================

tab = [] #np.array([personne(0,0,"healthy")])
fig = plt.figure()
camera = Camera(fig)                

for i in range(npersonne):
    r = random.uniform(0,1)
    s = ""
    if r < frac_healthy:
        s = "healthy"
    else :
        s = "sick"
    tab.append(personne(random.uniform(0, size), random.uniform(0, size), s))
      
for i in range(niter):

    for j in tab:
        j.update_pos() 
        
    for f in range(len(tab)):
        for w in range((i+1), len(tab)):
            tab[f].get_contamined(tab[w])
            
    if i%10 == 0:
        
        for k in tab:
            colour = {
            "sick" : "red",
            "healthy" : "blue"
            }
            plt.plot(k.get_x(), k.get_y(), ls = " ", marker='.', color = colour[k.get_status()])
        camera.snap()
        
        print("Progrès = ", (i/niter)*100, "%")
        
        
#%%        
animation = camera.animate()
animation.save('animation.mp4')
