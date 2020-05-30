# -*- coding: utf-8 -*-
"""
Created on Sun May 24 15:21:31 2020

@author: joeda
"""


# EPIDEMIC SPREAD IN A POPULATION OF RANDOM WALKERS ON A LATTICE
import numpy as np
import matplotlib.pyplot as plt

#---------------------------------------------------------------------------
N = 128 # lattice size
M = 8000 # number of random walkers
L = 20 # lifetime parameter
k = L/2 #temps avant hospitalisation/apparition des symptômes
max_iter = 1000 # maximum number of iterations
#---------------------------------------------------------------------------

def frontiere(walkers):
    walkers['x']=np.where(walkers['x']>N,N,walkers['x'])
    walkers['x']=np.where(walkers['x']<1,1,walkers['x'])
    walkers['y']=np.where(walkers['y']>N,N,walkers['y'])
    walkers['y']=np.where(walkers['y']<1,1,walkers['y'])


def update(walkers) :
    global n_sick,n_hopital,n_dead
    n_sick=np.sum(walkers['statut']==2)
    n_hopital=np.sum(walkers['statut']==1)
    n_dead=np.sum(walkers['statut']==3)
    ts_sick[iterate]=n_sick

    print("iteration {0}, sick {1},hospitalized {2} dead {3}.".format(iterate,n_sick,n_hopital,n_dead))


personne=np.dtype([

        ('x', np.int32, (1)),
        ('y', np.int32, (1)),
        ('statut', np.int8, (1)),
        ('lifespan',np.float32,(1))

    ])

grille=np.zeros((N,N))

#Les statuts possibles :
    #0 sain
    #1 infecté, asymptomatique
    #2 infecté, symptomatique
    #3 Hospitaliser
    #4 rétabli ou mort


x_step =np.array([-1,0,1,0]) # template arrays
y_step =np.array([0,-1,0,1])
"""
x,y =np.zeros(M),np.zeros(M) # walker (x,y) coordinates
infect =np.zeros(M) # walker health status
lifespan=np.zeros(M) # time left to live
"""

ts_sick =np.zeros(max_iter) # time series of sick walkers

walkers=np.zeros(M,dtype=personne)
walkers['x']=np.random.randint(0,N,size=M)
walkers['y']=np.random.randint(0,N,size=M)
walkers['lifespan']+=L
"""
for j in range(M): # place walkers on lattice
    x[j]=np.random.random_integers(0,N)
    y[j]=np.random.random_integers(0,N)
    lifespan[j]=L
"""
jj=np.random.randint(0,M) # infect one random walker
walkers[jj]['statut']=2
n_sick,n_dead,n_hopital,iterate=1,0,0,0 # various counters

while (n_sick+n_hopital > 0) and (iterate < max_iter): # temporal iteration
    #update(walkers)

    #Étape 1 : Vérifions s'il y a de nouveaux infecté



    etat=np.where(walkers['statut']==0)# sain
    sain=walkers[etat][:]
    infection=np.where(grille[sain['x']-1,sain['y']-1]==1,True,False)

    ratio=0.25 #25% de la population est symptomatique
    r=np.random.uniform(0,1,M)[etat]

    sain['statut']=np.where(np.logical_and(infection,r<ratio),1,2)

    walkers[etat]=sain[:]

    #connection=np.dtype()
    grille=np.zeros((N,N))
    #update(walkers)
    #------------------------------------------------

    #étape 2.1 : Vérifions l'état des infectés
    etat=np.where(walkers['statut']==1) # infecté symptomatique
    infecte1=walkers[etat][:]
    infecte1['lifespan']-=1
    infecte1['statut']=np.where(infecte1['lifespan']<=L-k,3,1)
    walkers[etat]=infecte1[:]
    grille[infecte1['x']-1,infecte1['y']-1]=1
    #Les malades doivent se deplacer ;
    #les malades seront diviser en sous catégorie ; asymptomatique et symptomatique
    #les asymptomatiques propagent l'infection pendant le temps L
    #les symptomatiques propagent l'infection pendant K et sont isolé, et meurt après L
    #update(walkers)
     #------------------------------------------------

    #étape 2.2 : Vérifions l'état des infectés
    etat=np.where(walkers['statut']==2) #infecte asymptomatique
    infecte2=walkers[etat][:]
    infecte2['lifespan']-=1
    infecte2['statut']=np.where(infecte2['lifespan']<=0,3,2)
    walkers[etat]=infecte2[:]

    grille[infecte2['x']-1,infecte2['y']-1]=1


    #étape 3 : déplacement
    ii=np.random.choice([0,1,2,3],size=M)
    walkers['x']+=x_step[ii] # update walker coordinates
    walkers['y']+=y_step[ii]
    #Condition frontiere
    frontiere(walkers)

    update(walkers)
    iterate+=1
# end of temporal loop
plt.plot(range(0,iterate+10),ts_sick[0:iterate+10])
plt.show()
# END
