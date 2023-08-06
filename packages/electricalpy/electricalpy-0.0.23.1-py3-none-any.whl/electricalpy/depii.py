from __init__ import *
from .indi import *
from .depi import *
from .depev import *
from .depiv import *


def solve_depii(ckt):
    base_aa, base_zz = solve_depiv(ckt)
#here only b mat is modified
#lets collect all the II srcs
    ii_ = []
    volo_ = []
    for x in range(0,len(ckt)):
        if(ckt[x][0].split('.')[0]=="II"):
            ii_.append(ckt[x])
        if(ckt[x][0].split('.')[0]=="V"):
            volo_.append(ckt[x])

    if(len(ii_)!=0):
        no_no = no_nodes(ckt)
        a = base_aa
        
        for x in range(0,len(ii_)):
            for y in range(0,len(volo_)):
                if(ii_[x][3]==volo_[y][0]):
                    if(ii_[x][1]!=0):
                        a[ii_[x][1]-1][no_no+y] = a[ii_[x][1]-1][no_no+y] + ii_[x][-1]
                    if(ii_[x][2]!=0):
                        a[ii_[x][2]-1][no_no+y] = a[ii_[x][2]-1][no_no+y] - ii_[x][-1]
        A=a
        z=base_zz
    else:
        A = base_aa
        z = base_zz
    return(A,z)
    


