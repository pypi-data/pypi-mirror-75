from __init__ import *
from .indiv import *
from .indi import *

def solve_depi(ckt):
    base_g,base_zi = solve_indiv(ckt)
    #print(np.matrix(base_g))
# collecting all the vcis
    vi_ = []
    for x in range(0,len(ckt)):
        if(ckt[x][0].split('.')[0]=="VI"):
            vi_.append(ckt[x])
    g = base_g
    for y in range(0,len(vi_)):#effect of depend cs is + on leaving node and viz
        effected_node_pos = vi_[y][1]
        
        if(effected_node_pos!=0):
            
            if(vi_[y][3]!=0):
                pos_eff_col = vi_[y][3] - 1
                g[effected_node_pos - 1][pos_eff_col] = g[effected_node_pos - 1][pos_eff_col] + vi_[y][-1]
                
            if(vi_[y][4]!=0):
                neg_eff_col = vi_[y][4] - 1
                g[effected_node_pos - 1][neg_eff_col] = g[effected_node_pos - 1][neg_eff_col] - vi_[y][-1]

        effected_node_neg = vi_[y][2]
        if(effected_node_neg!=0):
            if(vi_[y][-2]!=0):
                pos_eff_cool = vi_[y][-2] - 1
                g[effected_node_neg - 1][pos_eff_cool] = g[effected_node_neg - 1][pos_eff_cool] + vi_[y][-1]
            if(vi_[y][-3]!=0):
                neg_eff_cool = vi_[y][-3] - 1
                g[effected_node_neg - 1][neg_eff_cool] = g[effected_node_neg - 1][neg_eff_cool] - vi_[y][-1]
    A = g #actually base_g[] is A matrix obtained form indiv 
    return (A,base_zi)






#


