
from __init__ import *
from .indi import *
from .depi import *
from .depev import *
from .depiv import *
from .indiv import *
from .depii import *


            



def solve_circuit(ckt):
    nooo__ = no_nodes(ckt)
    def mody(ckt):
        for tt in range(0,len(ckt)):
            if(ckt[tt][0].split('.')[0]=='IV'):
                if(ckt[tt][3].split('.')[0]!='V'):
                    f_node = 1 + no_nodes(ckt)
                    target = ckt[tt][3]
                    for uu in range(0,len(ckt)):
                        if(target == ckt[uu][0]):
                            ckt.append(["V."+str(f_node),f_node,ckt[uu][2],0])
                            ckt[uu][2] = f_node
                            ckt[tt][3] = "V."+str(f_node)
                            
                            
            if(ckt[tt][0].split('.')[0]=='II'):
                if(ckt[tt][3].split('.')[0]!='V'):
                    f_node = 1 + no_nodes(ckt)
                    target = ckt[tt][3]
                    for uu in range(0,len(ckt)):
                        if(target == ckt[uu][0]):
                            ckt.append(["V."+str(f_node),f_node,ckt[uu][2],0])
                            ckt[uu][2] = f_node
                            ckt[tt][3] = "V."+str(f_node)
        return ckt

            

    modification_times  = 0
    
    for x in range(0,len(ckt)):
        if(ckt[x][0].split('.')[0]=='IV'):
            if(ckt[x][-2].split('.')[0]!='V'):
                modification_times = modification_times + 1
        if(ckt[x][0].split('.')[0]=="II"):
            if(ckt[x][-2].split('.')[0]!='V'):
                modification_times = modification_times + 1

    
    for x in range(0,modification_times):
        ckt = mody(ckt)
    

    #print(ckt)
    a,z = solve_depii(ckt)


    f_res = mat_multiply(np.linalg.inv(a),z)
    return f_res[0:nooo__]
    #return a,z














        
