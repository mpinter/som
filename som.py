import random as rr
import scipy.io
import math
import copy as copyimport
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pylab import *
from mpl_toolkits.mplot3d import Axes3D

alpha=0.12
lambi=5
lambf=0.4

w_size=10
rand_size=100
num_ep=25

w=[]
w_react=[]
data=[]
mins=[]
adj=[]

def irislist():
    with open("iris.dat") as f:
        for line in f:
            data.append(list(map(float,line.split())))

def randnet(n):
    for i in range(n):
        w.append([])
        w_react.append([])
        for j in range(n):
            v=[]
            for k in range(4):
                v.append(rr.random()*8-5)
            w[-1].append(v)
            w_react[-1].append([0.0]*3)

def dist(p1,p2):
    sum=0.0
    for i in range(len(p1)):
        sum+=pow((p2[i] - p1[i]),2)
    return math.sqrt(sum)    

def omega1(k1,l1,k2,l2,lamb):
    return pow(lamb,max(abs(k2-k1),abs(l2-l1)))

def omega2(k1,l1,k2,l2,lamb):
    return math.exp(-1.0*(pow((k1 - k2),2)+pow((l1 - l2),2))/(lamb*lamb))

def react():
    for k in range(w_size):
        for l in range(w_size):
            min=float('inf')
            ws=w[k][l]
            pos=0
            for x in data:
                d=dist(ws,x)
                if d<min:
                    min=d
                    pos=int(x[4])-1
            w_react[k][l][pos]=1.0


### MAIN ALGORITHM ###


#matlist()
#randlist(rand_size)
irislist()
randnet(w_size)
lamb=lambi
for ep in range(num_ep):
    mins.append(0.0)
    adj.append(0.0)
    perm=list(range(rand_size))
    rr.shuffle(perm)
    w_snapshot=copyimport.deepcopy(w)
    for j in perm:
        x=data[j]
        min=float('inf')
        mink=47
        minl=47
        for k in range(w_size):
            for l in range(w_size):
                ws=w[k][l]
                d=dist(ws,x)
                if d<min:
                    min=d
                    mink=k
                    minl=l
        mins[-1]+=min
        for k in range(w_size):
            for l in range(w_size):
                omg=omega2(mink,minl,k,l,lamb)
                for i in range(len(w[k][l])):
                    w[k][l][i]+=omg*alpha*(x[i]-w[k][l][i])
    lamb=lambi*(lambf/lambi)**(ep/num_ep)
    mins[-1]/=num_ep
    for k in range(w_size):
        for l in range(w_size):
            adj[-1]+=dist(w_snapshot[k][l],w[k][l])
    adj[-1]/=num_ep
    #print(mins[-1])


### GRAPHS ###


#ATTRIBUTE VALUES#

a=[]
a_min=[float('inf')]*len(w[0][0])
a_max=[float('-inf')]*len(w[0][0])
for i in range(len(w[k][l])):
    a.append([])
    for k in range(w_size):
        a[-1].append([])
        for l in range(w_size):
            a[-1][-1].append(w[k][l][i])
            if (w[k][l][i]>a_max[i]):
                a_max[i]=w[k][l][i]
            if (w[k][l][i]<a_min[i]):
                a_min[i]=w[k][l][i]
for i in range(len(w[k][l])):
    figure(1)                
    imshow(a[i], cmap='winter',interpolation='nearest', vmin=a_min[i], vmax=a_max[i])
    grid(True)
    plt.show()

# REACT TO CLASSES #

figure(1)
react()
imshow(w_react,interpolation='nearest')
grid(True)
plt.show()

# PLOT MINS #

fig = plt.figure()
plot(mins)
plt.show()

# PLOT ADJUSTMENTS #

fig = plt.figure()
plot(adj)
plt.show()