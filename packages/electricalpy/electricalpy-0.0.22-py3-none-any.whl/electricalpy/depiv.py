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


c1 = [
    ["V.1",1,0,5],
    ["R.1",1,2,1],
    ["R.2",2,0,1],
    ["R.3",3,0,1],
    ["IV.1",2,3,"V.1",3]]

c2 = [
    ["R.1",1,0,1],
    ["R.2",2,0,1],
    ["R.3",3,0,1],
    ["V.1",2,1,5],
    ["IV.1",2,3,"V.1",2]]

c3 = [
    ["V.1",1,0,3],
    ["R.1",1,2,1],
    ["R.2",2,0,1],
    ["R.3",2,3,1],
    ["IV.1",3,0,"V.1",2]]
c4 = [
    ["IV.1",1,0,"V.1",3],
    ["IV.2",2,3,"V.2",2],
    ["V.1",2,0,5],
    ["V.2",3,0,3],
    ["R.1",1,0,1],
    ["R.2",1,2,1],
    ["R.3",3,0,1]]
# mody
m = [
    ["V.1",1,0,5],
    ["R.1",2,1,1],
    ["R.2",2,0,1],
    ["R.3",3,0,1],
    ["IV.1",2,3,"R.1",3]]
m2 = [
    ["V.1",1,0,5],
    ["R.1",2,1,1],
    ["R.2",2,0,1],
    ["R.3",3,0,1],
    ["IV.1",2,3,"V.1",3]]

m3 = [['V.1', 1, 0, 5],
      ['R.1', 2, 1, 1],
      ['R.2', 2, 4, 1],
      ['R.3', 3, 0, 1],
      ['IV.1', 2, 3, 'V.4', 3],
      ['V.4', 4, 0, 0]]
aa= solve_depiv(c2)

