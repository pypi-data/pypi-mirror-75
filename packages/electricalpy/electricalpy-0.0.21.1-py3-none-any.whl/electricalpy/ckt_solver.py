
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


ckt2 = [
    ["V.1",1,0,5],
    ["R.1",2,1,1],
    ["R.2",2,0,1],
    ["R.3",3,0,1],
    ["IV.1",2,3,"R.2",3]]
ckt1 = [
    ["I.1",0,1,1],
    ["R.1",1,2,2],
    ["R.2",2,0,2],
    ["R.3",2,3,2],
    ["II.1",0,3,"R.1",2],
    ["IV.1",2,3,"R.1",2]]

jjaja = [
	["V.1",1,0,2],
	["R.1",2,1,1],
	["R.2",2,0,10],
	["R.3",2,3,5],
	["I.1",0,3,4],
	["R.4",3,0,15]]


uu = solve_circuit(jjaja)












        
