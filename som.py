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
num_ep=200

w=[]
data=[]
mins=[]

def randlist(n):
    for i in range(0,n):
        data.append([])
        data[-1].append(rr.random())
        data[-1].append(rr.random())
        data[-1].append(rr.random())
        #data[-1].append(random.randint(0,2))

def matlist():
    test=scipy.io.loadmat('SOM_data.mat')
    #print(test['data'])
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
        for j in range(n):
            v=[]
            for k in range(4):
                v.append(rr.random()*10-5)
            w[-1].append(v)

def dist(p1,p2):
    sum=0.0
    #print("dif")
    #print(len(p1)) #TU JE BUG
    for i in range(len(p1)):
        #print((p2[i] - p1[i]))
        sum+=pow((p2[i] - p1[i]),2)
    return math.sqrt(sum)    

def omega1(k1,l1,k2,l2,lamb):
    return pow(lamb,max(abs(k2-k1),abs(l2-l1)))

def omega2(k1,l1,k2,l2,lamb):
    #print("dist")
    #print(dist(w[k1][l1],w[k2][l2]))
    return math.exp(-1.0*(pow((k1 - k2),2)+pow((l1 - l2),2))/(lamb*lamb))
    #return math.exp(-1.0*pow(dist(winner,w[k2][l2]),2)/(lamb*lamb))

#matlist()
#randlist(rand_size)
irislist()
#print(data)
randnet(w_size)
lambi=5
lambf=0.4
lamb=lambi
print(data)
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
                #print("----")
                wadd=[]
                omg=omega2(mink,minl,k,l,lamb)
                #for i in range(len(w[k][l])):
                    #print(i)
                    #wadd.append(omg*alpha*(x[i]-w[k][l][i]))
                    #print("wa")
                    #print(omega1(mink,minl,k,l,0.25))
                    #print(omega2(mink,minl,k,l,lamb))
                    #print((x[i]-w[k][l][i]))
                    #print(wadd)
                #print(wadd)
                #print("add")
                #print(w[k][l])
                for i in range(len(w[k][l])):
                    w[k][l][i]+=omg*alpha*(x[i]-w[k][l][i])
                #print(w[k][l])
        #print(mins[-1])
        #print(min)
    lamb=lambi*(lambf/lambi)**(ep/num_ep);
    #halt
    #lamb=lamb-0.003
    print(lamb)
    print(mins[-1])

figure(1)
a=[]
x_min=float('inf')
x_max=float('-inf')
for k in range(w_size):
    a.append([])
    for l in range(w_size):
        a[-1].append(w[k][l][0])
        if (w[k][l][0]>x_max):
            x_max=w[k][l][0]
        if (w[k][l][0]<x_min):
            x_min=w[k][l][0]
        #a.append(rr.randint(1,20))
A = rand(5,5)
imshow(a, cmap='winter',interpolation='nearest', vmin=x_min, vmax=x_max)
grid(True)
print(A)
print(a)
print(x_min)
print(x_max)
plt.show()
fig = plt.figure()
plot(mins)
plt.show()









def tooold():
    print(w)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x=[]
    y=[]
    z=[]
    dx=[]
    dy=[]
    dz=[]
    for k in range(w_size):
        for l in range(w_size):
            x.append(w[k][l][0])
            y.append(w[k][l][1])
            z.append(w[k][l][2])
    for i in range(rand_size):
        dx.append(data[i][0])
        dy.append(data[i][1])
        dz.append(data[i][2])
    ax.plot_trisurf(x,y,z)
    ax.scatter(dx,dy,dz)
    plt.show()