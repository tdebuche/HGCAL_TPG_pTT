import numpy as np
import json
from STCtopTTs import pTT_single_STC_layer
from ModuleSumtopTTs import pTT_single_module_layer


Values2024 = np.load('ProgrammesRessources/ValuesBins2024.npy')
Values2028 = np.load('ProgrammesRessources/ValuesBins2028.npy')


######### PTTarray -> array(24,20,maxmodulesperPTT,5(or6)) -> 5 for CE-E (without STC indices) -> 6 for CE-H ########
############# 24 -> phi, 20 -> eta, maxmod... ok, 5 : i (numéro du module), u,v, ratio (for CEE) ##########
############# 24 -> phi, 20 -> eta, maxmod... ok, 6 : i (numéro du module), u,v, ratio, indice STC (for CEH) #######


def pTT_single_layer(args,Layer,Modules,STCs):
    if Layer < 27:
        return pTT_single_module_layer(args,Layer,Modules)
    else :
        if not STCyesorno:
            return pTT_single_module_layer(args,Layer,Modules)      
        if STCyesorno :
            return pTT_single_STC_layer(args,Layer,STCs)  


def build_pTTs(args,Layer,Modules,STCs,Values):
    pTTs = pTT_single_layer(args,Layer,Modules,STCs)
    nb_binphi,nb_bineta,phimin,phimax,etamin,etamax = Values
    nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
    reversed_pTTs = [[[] for j in range(nb_bineta)] for i in range(nb_binphi)]
    if Layer < 48 and not STCyesorno : 
        for module_idx in range(len(pTTs)):
            for pTT_idx in range(len(pTTs[module_idx])):
                eta,phi,ratio = pTTs[i][j]
                u = UV[Layer-1][i][0]
                v = UV[Layer-1][i][1]
                reversed_pTTs[phi][eta].append([Module_type[Layer-1][i],u,v,ratio])
                                          
    if Layer < 27 and STCyesorno :   
        L =[[[] for j in range(nb_bineta)] for i in range(nb_binphi)]
        for i in range(len(listpttpermodules)):
            for j in range(len(listpttpermodules[i])):
                iptt,jptt,ratio = listpttpermodules[i][j]
                u = UV[Layer-1][i][0]
                v = UV[Layer-1][i][1]
                L[iptt][jptt].append([Module_type[Layer-1][i],u,v,ratio])

    if Layer > 26 and STCyesorno :
        L =[[[] for j in range(nb_bineta)] for i in range(nb_binphi)]
        for i in range(len(listpttpermodules)):
            for j in range(len(listpttpermodules[i])):
                for k in range(len(listpttpermodules[i][j])):
                    iptt,jptt,ratio = listpttpermodules[i][j][k]
                    u = UV[Layer-1][i][0]
                    v = UV[Layer-1][i][1]
                    L[iptt][jptt].append([STC_type[Layer-1][i],u,v,STC_index[Layer-1][i],ratio])

    return(L)


