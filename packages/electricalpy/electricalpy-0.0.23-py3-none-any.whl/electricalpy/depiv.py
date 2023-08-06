from __init__ import *
from .indi import *
from .depi import *
from .depev import *

def solve_depiv(ckt):
    base_a,base_z = solve_depv(ckt)
#collecting all IV sources
    iv_ = []
    for x in range(0,len(ckt)):
        if(ckt[x][0].split('.')[0]=="IV"):
            iv_.append(ckt[x])
    
#first lets modify z matrix
    z = base_z

    if(len(iv_)!=0):
        for x in range(0,len(iv_)):
            z = np.vstack((z,[0]))  #adding a zero row for each Iv
        
    #collecting all IV sources
        iv_ = []
        for x in range(0,len(ckt)):
            if(ckt[x][0].split('.')[0]=="IV"):
                iv_.append(ckt[x])          
    # now we are done with z lets move to b []
        b = np.zeros((len(base_a),len(iv_)))
    # lets fill b []
        for x in range(0,len(iv_)):
            if(iv_[x][1]!=0):
                pos_eff_row = iv_[x][1] - 1
                b[pos_eff_row][x] = 1
            if(iv_[x][2]!=0):
                neg_eff_row = iv_[x][2] - 1
                b[neg_eff_row][x] = -1
        
    #done filling b, lets fill c
        c = np.zeros((len(iv_),no_nodes(ckt)))
        for x in range(0,len(iv_)):
            if(iv_[x][1]!=0):
                poss_eff = iv_[x][1] - 1
                c[x][poss_eff] = 1
            if(iv_[x][2]!=0):
                negg_eff = iv_[x][2] - 1
                c[x][negg_eff] = -1
    #done with c matrix now lets make d
        volt_m = []
        for x in range(0,len(ckt)):
            if(ckt[x][0].split('.')[0]=="V"):
                volt_m.append(ckt[x])

        a_with_b_mod = np.column_stack((base_a,b))
           
        d = np.zeros((len(iv_),(len(iv_)+len(volt_m))))
        
    # lets fill d mat
        for x in range(0,len(iv_)):
            for y in range(0,len(volt_m)):
                if(iv_[x][3] == volt_m[y][0]):
                    d[x][y] = d[x][y] - iv_[x][-1]
    # lets join d to c
        c = np.column_stack((c,d))
    # last join c to a
        A = np.vstack((a_with_b_mod,c))
        
    else:
        A = base_a
        z = base_z
    return(A,z)




