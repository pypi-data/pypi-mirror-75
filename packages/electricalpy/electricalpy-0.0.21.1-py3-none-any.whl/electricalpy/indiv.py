from __init__ import *
from .indi import *

def solve_indiv(ckt):
    base_g,base_z = solve_indi(ckt)
# time for b mat
    v_ = []
    for x in range(len(ckt)):
        if(ckt[x][0].split('.')[0] == "V"):
            v_.append(ckt[x])
    n = no_nodes(ckt)
    no_iv_srcs = len(v_)
    if(no_iv_srcs!=0):
        b = np.zeros((n,no_iv_srcs))

    #lets fill b mat with +1 for +ve connected to that node

        for x in range(0,len(v_)):
            if(v_[x][1]!=0):
                node_no_of_neg_terminal = v_[x][1]
                b[node_no_of_neg_terminal-1][x] = b[node_no_of_neg_terminal-1][x] + 1
            if(v_[x][2]!=0):
                node_no_of_pos_terminal = v_[x][2]
                b[node_no_of_pos_terminal-1][x] = b[node_no_of_pos_terminal-1][x] - 1
    #b is done now, time for c
        a = np.column_stack((base_g,b)).tolist()
        c = transpose(b).tolist()
        d = np.zeros((no_iv_srcs,no_iv_srcs)).tolist()
        c_with_d = np.column_stack((c,d))

        a = np.vstack((a,c_with_d)).tolist()
    #done with a now, time for z

        z = base_z
        for x in range(0,len(v_)):
            z= np.vstack((z,v_[x][-1]))
    else:
        a = base_g
        z = base_z
        

    
    return (a,z)
ckt = [
	['V.1',1,0,2],
        ['V.2',3,0,3],
        ['R.1',1,2,2],
        ['R.2',2,0,3],
        ['R.3',2,3,2]]

ckt2 = [
    ["V.1",1,0,1],
    ["I.1",0,3,1],
    ["R.1",3,1,2],
    ["R.2",1,2,1],
    ["R.3",2,0,1]]

ckt3 = [
    ["R.1",0,1,1],
    ["R.2",2,0,1],
    ["V.1",2,1,1],
    ["I.1",0,2,2]]
ckt4 = [
	["I.1",0,1,2],
	["R.1",1,2,1],
	["R.2",2,0,1],
	["R.3",3,0,1],
	["EV.1",2,3,1,2,2]
	]
ckt5 = [
    ["V.1",1,0,2],
    ["R.1",2,1,1],
    ["R.2",2,0,10],
    ["R.3",2,3,5],
    ["R.4",3,0,15],
    ["I.1",0,3,4]]


tt = solve_indiv(ckt5)

