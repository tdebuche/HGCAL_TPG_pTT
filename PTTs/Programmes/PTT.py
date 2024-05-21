import numpy as np
import matplotlib.pyplot as plt
import os
from shapely.geometry import Polygon
import functions
from STCtoPTT import pTTSTCs
from ModuleSumtoPTT import pTTModules
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path+'/../../ProgrammesRessources')
UV = np.load('UVModules.npy')
G = np.load('ModulesGeometry.npy')
Z = np.load('Z.npy')
STCLD = np.load('STCLD.npy')
STCHD = np.load('STCHD.npy')
Values2024 = np.load('ValuesBins2024.npy')
Values2028 = np.load('ValuesBins2028.npy')


######### PTTarray -> array(24,20,maxmodulesperPTT,5(or6)) -> 5 for CE-E (without STC indices) -> 6 for CE-H ########
############# 24 -> phi, 20 -> eta, maxmod... ok, 5 : i (numéro du module), u,v, ratio (for CEE) ##########
############# 24 -> phi, 20 -> eta, maxmod... ok, 6 : i (numéro du module), u,v, ratio, indice STC (for CEH) #######


def PTTLayer(Layer,STCyesorno,edges):
    if Layer < 27:
        return pTTModules(G,Layer,edges)
    else :
        if not STCyesorno:
            return pTTModules(G,Layer,edges)      
        if STCyesorno :
            return pTTSTCs(STCLD,STCHD,Layer,edges)  


def constructionPTT(Layer,STCyesorno,edges,Values):
    listpttpermodules = PTTLayer(Layer,STCyesorno,edges)
    nb_binphi,nb_bineta,phimin,phimax,etamin,etamax = Values
    nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
    if Layer < 48 and not STCyesorno : 
        L =[[[] for j in range(nb_bineta)] for i in range(nb_binphi)]
        for i in range(len(listpttpermodules)):
            for j in range(len(listpttpermodules[i])):
                iptt,jptt,ratio = listpttpermodules[i][j]
                u = UV[Layer-1,i,0]
                v = UV[Layer-1,i,1]
                L[iptt][jptt].append([i,u,v,ratio])
                
    if Layer < 27 and STCyesorno :   
        L =[[[] for j in range(nb_bineta)] for i in range(nb_binphi)]
        for i in range(len(listpttpermodules)):
            for j in range(len(listpttpermodules[i])):
                iptt,jptt,ratio = listpttpermodules[i][j]
                u = UV[Layer-1,i,0]
                v = UV[Layer-1,i,1]
                L[iptt][jptt].append([i,u,v,ratio])

    if Layer > 26 and STCyesorno :
        L =[[[] for j in range(nb_bineta)] for i in range(nb_binphi)]
        for i in range(len(listpttpermodules)):
            for j in range(len(listpttpermodules[i])):
                for k in range(len(listpttpermodules[i][j])):
                    iptt,jptt,ratio = listpttpermodules[i][j][k]
                    u = UV[Layer-1,i,0]
                    v = UV[Layer-1,i,1]
                    L[iptt][jptt].append([i,u,v,j,ratio])

    return(L)


def PTTarray(Layer,STCyesorno,edges):
    if edges:
        Values = Values2028
    else :
        Values = Values2024
    L = constructionPTT(Layer,STCyesorno,edges,Values)
    nb_binphi,nb_bineta,phimin,phimax,etamin,etamax = Values
    nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
    
    max = 0
    for i in range(len(L)):
        for j in range(len(L[i])):
            if len(L[i][j]) >max:
                max = len(L[i][j])
    if Layer < 27:
        A = np.zeros((nb_binphi,nb_bineta,max,4))
    else :
        if not STCyesorno:
            A = np.zeros((nb_binphi,nb_bineta,max,4)) 
        if STCyesorno:
            A = np.zeros((nb_binphi,nb_bineta,max,5)) 
    for i in range(len(L)):
        for j in range(len(L[i])):
            for k in range(len(L[i][j])):
                A[i,j,k] = np.array(L[i][j][k])
    return A

