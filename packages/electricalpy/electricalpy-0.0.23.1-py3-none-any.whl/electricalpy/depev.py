from __init__ import *
from .indiv import *
from .indi import *
from .depi import *

def solve_depv(ckt):
    base_A, base_z = solve_depi(ckt)
    z = base_z
#sorting out the EV sources
    ev_ = []
    for x in range(0,len(ckt)):
        if(ckt[x][0].split('.')[0]=="EV"):
            ev_.append(ckt[x])
#adding no zeros equal to no.of EV in z
    if(len(ev_)!=0):
        for x in range(0,len(ev_)):
            z = np.vstack((z,[0]))
    #done with z now lets modify b in A[]
        b = np.zeros((len(base_A),len(ev_)))
    #now lets fill b mat ;)
        for x in range(0,len(ev_)):
            if(ev_[x][1]!=0):
                pos_eff_row = ev_[x][1] - 1
                b[pos_eff_row][x] = 1
            if(ev_[x][2]!=0):
                neg_eff_row = ev_[x][2] - 1
                b[neg_eff_row][x] = -1
    #lets add b into A
        mod_A = np.column_stack((base_A,b))
    #time to modify c matrix
        c = transpose(b)# here b is the matrix createed in this file
    #only difference is we need to add/sub gain from c respective row col
        for x in range(0,len(ev_)):
            if(ev_[x][3]!=0):
                neg_eff = ev_[x][3]-1
                c[x][neg_eff] = c[x][neg_eff] - ev_[x][-1]
            if(ev_[x][4]!=0):
                pos_eff = ev_[x][4]-1
                c[x][pos_eff] = c[x][pos_eff] + ev_[x][-1]
    #done with c mat,  now should match the size of c and a
        # creating fake d matrix with all zeros
        d = np.zeros((len(ev_),len(ev_)))
    #joining c,d
        c = np.column_stack((c,d))
        A = np.vstack((mod_A,c))

    else:
        A = base_A
        z = base_z
    return (A,z)
        
    
    
































    
