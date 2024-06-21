import numpy as np
import matplotlib.pyplot as plt
import os
from shapely.geometry import Polygon
import functions
from STCtopTTs import pTT_single_STC_layer
from ModuleSumtopTTs import pTT_single_module_layer
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path+'/../../ProgrammesRessources')

UV =  functions.item_list('Modules.json','uv')
G =  functions.item_list('Modules.json','vertices')
Module_type =  functions.item_list('Modules.json','type')

STCs = functions.item_list('STCs.json','vertices')
STCLD = STCs[33:47]
STCHD = STCs[26:33]
STC_type =  functions.item_list('STCs.json','type')
STC_index = functions.item_list('STCs.json','index')
Values2024 = np.load('ValuesBins2024.npy')
Values2028 = np.load('ValuesBins2028.npy')


######### PTTarray -> array(24,20,maxmodulesperPTT,5(or6)) -> 5 for CE-E (without STC indices) -> 6 for CE-H ########
############# 24 -> phi, 20 -> eta, maxmod... ok, 5 : i (numéro du module), u,v, ratio (for CEE) ##########
############# 24 -> phi, 20 -> eta, maxmod... ok, 6 : i (numéro du module), u,v, ratio, indice STC (for CEH) #######


def pTT_single_layer(Layer,STCyesorno,edges):
    if Layer < 27:
        return pTT_single_module_layer(G,Layer,edges)
    else :
        if not STCyesorno:
            return pTT_single_module_layer(G,Layer,edges)      
        if STCyesorno :
            return pTT_single_STC_layer(STCLD,STCHD,Layer,edges)  


def build_pTTs(Layer,STCyesorno,edges,Values):
    listpttpermodules = pTT_single_layer(Layer,STCyesorno,edges)
    nb_binphi,nb_bineta,phimin,phimax,etamin,etamax = Values
    nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
    if Layer < 48 and not STCyesorno : 
        L =[[[] for j in range(nb_bineta)] for i in range(nb_binphi)]
        for i in range(len(listpttpermodules)):
            for j in range(len(listpttpermodules[i])):
                iptt,jptt,ratio = listpttpermodules[i][j]
                u = UV[Layer-1][i][0]
                v = UV[Layer-1][i][1]
                L[iptt][jptt].append([Module_type[Layer-1][i],u,v,ratio])
                                          
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


