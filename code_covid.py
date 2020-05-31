# -*- coding: utf-8 -*-
"""
Created on Sat May 30 17:48:57 2020

@author: myria
"""
#%%
# =============================================================================
# IMPORTATIONS
# =============================================================================
# voilaaaa
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
    def __init__(self, x, y, max_size, status="healthy", hygiene = 1, mask = False, walk_range = 50):
        self.x = x # position
        self.y = y
        self.status = status # health status ("healthy","sick", "removed")
        self.hygiene = hygiene
        self.mask = mask
        self.walk_range = walk_range
        self.max_size = max_size
        self.death_prob = 0

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
        if (self.get_status != "removed"):
            r1 = random.uniform(-1, 1)
            r2 = random.uniform(-1, 1)
            self.update_x(int(self.x + r1*self.walk_range))
            self.update_y(int(self.y + r2*self.walk_range))

            if (self.get_x() > self.get_max_size()):
                self.x = self.get_max_size()

            if (self.get_x() < 0):
                self.x = 0

            if (self.get_y() > self.get_max_size()):
                self.y = self.get_max_size()

            if (self.get_y() < 0):
                self.y = 0

            if (self.status == "sick"):
                self.death_prob += 1/(21*24) # update on the death_prob
                r3 = np.random.uniform(0, 1)

                if (r3 < self.death_prob):
                    self.change_status("removed") # the walker is removed with an increasing probability

    def get_hygiene(self):
        return self.hygiene

    def get_max_size(self):
        return self.max_size

    def get_contamined(self, other):
        if (self.get_distance(other) <= 50 and other.get_status() == "sick"):
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

# plt.plot(xx, yy)

#%%
# =============================================================================
# GLOBAL PARAMETERS
# =============================================================================

niter = 300 #Iteration number
npersonne = 500 #Number of people
frac_healthy = 0.9 #Initial fraction of healthy people
size = 5000 #Size of the simulation grid
pour = 0.1*niter

#%%
# =============================================================================
# MAIN
# =============================================================================

tab = [] #Empty list

#For the animation
fig = plt.figure()
camera = Camera(fig)

#Temporal loop
for i in range(npersonne):
    r = random.uniform(0,1)
    s = ""
    if r < frac_healthy:
        s = "healthy"

    else :
        s = "sick"
    tab.append(personne(random.uniform(0, size), random.uniform(0, size),  max_size = size, status = s))

# Loop updating the attribute of every walker
for i in range(niter):
    # Loop to update the position of the walkers
    for j in tab:
        j.update_pos()

    # Loop to determine who's contaminated
    for f in range(len(tab)):
        for w in range((i+1), len(tab)):
            tab[f].get_contamined(tab[w])

    #
    if i%pour == 0:

        for k in tab:
            colour = {
            "sick" : "red",
            "healthy" : "blue",
            "removed" : "black"
            }
            plt.plot(k.get_x(), k.get_y(), ls = " ", marker='.', color = colour[k.get_status()])
            if (k.get_status() == "removed"):
                tab.remove(k)

        camera.snap()

        print("Progress = ", np.round((i/niter)*100, 2), "%")

#%%
#Animate and save
animation = camera.animate()
animation.save('animation.mp4')
