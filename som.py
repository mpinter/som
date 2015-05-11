import random as rr
import scipy.io
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pylab import *
from mpl_toolkits.mplot3d import Axes3D

alpha=0.12
lamb=5

w_size=10
rand_size=100
num_ep=25

w=[]
w_react=[]
data=[]
mins=[]

def react():
    for k in range(w_size):
        for l in range(w_size):
            min=float('inf')
            ws=w[k][l]
            pos=0
            for x in data:
                if dist(ws,x)<min:
                    min=dist(ws,x)
                    pos=int(x[4])-1
            w_react[k][l][pos]=1.0

def randlist(n):
    for i in range(0,n):
        data.append([])
        data[-1].append(rr.random())
        data[-1].append(rr.random())
        data[-1].append(rr.random())
        #data[-1].append(random.randint(0,2))

def matlist():
    test=scipy.io.loadmat('SOM_data.mat')
    rand_size=test['data'][0].size
    for i in range(test['data'][0].size):
        data.append([])
        data[-1].append(test['data'][0][i])
        data[-1].append(test['data'][1][i])
        data[-1].append(test['data'][2][i])

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
                v.append(rr.random()*10-5)
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

#matlist()
#randlist(rand_size)
irislist()
randnet(w_size)
lambi=5
lambf=0.4
lamb=lambi
for ep in range(num_ep):
    mins.append(0.0)
    perm=list(range(rand_size))
    rr.shuffle(perm)
    for j in perm:
        x=data[j]
        min=float('inf')
        mink=47
        minl=47
        for k in range(w_size):
            for l in range(w_size):
                ws=w[k][l]
                if dist(ws,x)<min:
                    min=dist(ws,x)
                    mink=k
                    minl=l
        mins[-1]+=min
        winner=list(w[mink][minl])
        for k in range(w_size):
            for l in range(w_size):
                wadd=[]
                omg=omega2(mink,minl,k,l,lamb)
                for i in range(len(w[k][l])):
                    w[k][l][i]+=omg*alpha*(x[i]-w[k][l][i])
    lamb=lambi*(lambf/lambi)**(ep/num_ep)
    #print(lamb)
    #print(mins[-1])
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
#print(a[0])
for i in range(len(w[k][l])):
    figure(1)                
    imshow(a[i], cmap='winter',interpolation='nearest', vmin=a_min[i], vmax=a_max[i])
    grid(True)
    plt.show()
figure(1)
react()
print(w_react)
imshow(w_react,interpolation='nearest')
grid(True)
plt.show()
fig = plt.figure()
plot(mins)
plt.show()