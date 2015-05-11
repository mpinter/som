import random

def fw(f,l):
    for idx,i in enumerate(l):
        if (idx==4):
            f.write(str(int(i))+'\n')
        else:
            f.write(str(i)+' ')

with open("iris.dat") as f:
    with open("iris_more.dat",'w') as fm:
        with open("iris_less.dat",'w') as fl:
            for line in f:
                x=list(map(float,line.split()))
                if random.random()>0.5:
                    if int(x[4])==1:
                        fw(fm,x)
                    else:
                        fw(fl,x)
                fw(fm,x)
                if int(x[4])==1:
                    fw(fl,x)