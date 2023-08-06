from __init__ import *
import numpy as np
import matplotlib.pyplot as plt
import sympy as sy
import math
def mat_multiply(A,B):
    result= np.zeros((np.shape(A)[0],np.shape(B)[1]),dtype=np.complex_)
    for i in range(len(A)): 
  
    # iterating by coloum by B  
        for j in range(len(B[0])): 
  
        # iterating by rows of B 
            for k in range(len(B)): 
                result[i][j] += A[i][k] * B[k][j]
    return result
    
def transpose(mat):
    result = np.zeros((np.shape(mat)[1],np.shape(mat)[0]),dtype=np.complex_)
    for i in range(len(mat)):
   # iterate through columns
       for j in range(len(mat[0])):
           result[j][i] = mat[i][j]
    return result

def no_nodes(ckt):
    b = len(ckt)
    nodes = 0
    for x in range(0, b):
        if(ckt[x][1]>=nodes):
            nodes = ckt[x][1]
        if(ckt[x][2]>=nodes):
            nodes = ckt[x][2]
    return nodes

def solve_indi(ckt):
    n = no_nodes(ckt)
    g = np.zeros((n,n),dtype=np.complex_)
    r_ = []
    for x in range(0,len(ckt)):
        temp = (ckt[x][0]).split('.')[0]
        if(temp == 'R'):
            r_.append((ckt[x]))

    for x in range(0,len(r_)):
        r_[x][-1] = 1/r_[x][-1]
    
    nodearray = []
    for tt in range(1, 1+n):
        nodearray.append(tt)
    volt_srcs = []
    for x in range(0,len(ckt)):
        temp = (ckt[x][0]).split('.')[0]
        if(temp == 'V'):
            volt_srcs.append((ckt[x]))
        if(temp == 'Ha'):
            volt_srcs.append((ckt[x]))
    
#finding diagonal elements
    dias = np.zeros((n))
    for y in range(0,len(r_)):
        for z in range(1,3):
            nodenum = r_[y][z]
            
            for xy in range(0,len(nodearray)):
                if(nodearray[xy]==nodenum):
                    g[xy][xy] = r_[y][-1]+ g[xy][xy]
#finding off diagonal elements
    r_non_zero = []
    for x in range(0,len(r_)):
        if(r_[x][1]!=0):
            if(r_[x][2]!=0):
                r_non_zero.append(r_[x])
    for x in range(0,len(r_non_zero)):
        g[r_non_zero[x][1]-1][r_non_zero[x][2]-1]=g[r_non_zero[x][1]-1][r_non_zero[x][2]-1]+r_non_zero[x][-1]
        g[r_non_zero[x][2]-1][r_non_zero[x][1]-1]=g[r_non_zero[x][2]-1][r_non_zero[x][1]-1]+r_non_zero[x][-1]
#multiplying -1 for off diagonals
    g = g* (-1)
    for x in range(0,len(g)):
        g[x][x]=g[x][x]*(-1)

# i matrix
    i_ = []
    for x in range(0,len(ckt)):
        if(ckt[x][0].split('.')[0]=="I"):
            i_.append(ckt[x])
    zi = np.zeros((n,1))

# adding +1 into entering node and -1 to exiting node of zi mat
    for y in range(0,len(i_)):
        if(i_[y][1]!=0):
            zi[i_[y][1]-1][0] = zi[i_[y][1]-1][0] + -i_[y][-1]
        if(i_[y][2]!=0):
            zi[i_[y][2]-1][0] = zi[i_[y][2]-1][0] + i_[y][-1]
    return (g,zi)
ckt3 = [
    ["VI.1",1,0,2,1,2], 
    ["VI.2",3,2,2,0,2],
    ["R.1",1,2,1],
    ["R.2",2,0,1],
    ["R.3",3,0,1],
    ["V.1",3,0,10]]
yy = solve_indi(ckt3)
