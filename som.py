import random
import scipy.io
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

alpha=0.5
lamb=0.8

w_size=10
rand_size=100

w=[]
data=[]

def randlist(n):
    for i in range(0,n):
        data.append([])
        data[-1].append(random.random())
        data[-1].append(random.random())
        data[-1].append(random.random())
        #data[-1].append(random.randint(0,2))

def matlist():
    test=scipy.io.loadmat('SOM_data.mat')
    print(test['data'])
    rand_size=test['data'][0].size
    for i in range(test['data'][0].size):
        data.append([])
        data[-1].append(test['data'][0][i])
        data[-1].append(test['data'][1][i])
        data[-1].append(test['data'][2][i])

def randnet(n):
    for i in range(n):
        w.append([])
        for j in range(n):
            v=[]
            for k in range(3):
                v.append(random.random())
            w[-1].append(v)

def dist(p1,p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 +
                     (p2[1] - p1[1]) ** 2 +
                     (p2[2] - p1[2]) ** 2)    

def omega1(k1,l1,k2,l2,lamb):
    return pow(lamb,max(abs(k2-k1),abs(l2-l1)))

def omega2(k1,l1,k2,l2,lamb):
    return math.exp(-1.0*pow(dist(w[k1][l1],w[k2][l2]),2))/(lamb*lamb)

matlist()
#randlist(rand_size)
randnet(w_size)
for ep in range(100):
    perm=list(range(rand_size))
    random.shuffle(perm)
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
        for k in range(w_size):
            for l in range(w_size):
                wadd=[omega1(mink,minl,k,l,lamb)*alpha*(xi-wi) for xi,wi in zip(x,w[k][l])]
                for i in range(3):
                    w[k][l][i]+=wadd[i]
    alpha=alpha-0.001
    lamb=lamb-0.003
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
