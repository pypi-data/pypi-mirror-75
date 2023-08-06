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


