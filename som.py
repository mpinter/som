import random
import math

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
        data[-1].append(random.randint(0,2))

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
    return lamb^math.max(abs(k2-k1),abs(l2-l1))

def omega2(k1,l1,k2,l2,lamb):
    return exp(-1*dist(w[k1][l1],w[k2][l2])^2)/lamb*lamb

randlist(rand_size)
randnet(w_size)
for ep in range(100):
    perm=random.shuffle(list(range(rand_size)))
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
                wadd=[omega1(mink,minl,k,l,x)*alpha*(xi-wi) for xi,wi in zip(x,w[k][l])]
                for i in range(3):
                    w[k][l][i]+=wadd[i]
    alpha=alpha-0.001;
    lamb=lamb-0.003;
