import numpy as np
import matplotlib.pyplot as plt
import os
from shapely.geometry import Polygon
from functions import etaphitoXY
from functions import etaphiRADtoXY
from functions import XYtoetaphi
from functions import polygontopoints
from functions import pointtopolygon
from functions import binetaphitoXY
from functions import binetaphiRADtoXY
from functions import etaphicentre
from functions import ModulestoVertices
from functions import BintoBinVertices
from functions import STCtoSTCVertices
from STCtoPTT import pTTSTCs
from ModuleSumtoPTT import pTTModules

os.chdir("../../ProgrammesRessources")

UV = np.load('UVModules.npy')
Binetaphi = np.load('Binetaphi2024.npy')
#Binetaphi = np.load('Binetaphi2024.npy')
G = np.load('ModulesGeometry.npy')
Z = np.load('Z.npy')
STCLD = np.load('STCLD.npy')
STCHD = np.load('STCHD.npy')
etamin = 1.305


######### PTTarray -> array(24,20,maxmodulesperPTT,5(or6)) -> 5 for CE-E (without STC indices) -> 6 for CE-H ########
############# 24 -> phi, 20 -> eta, maxmod... ok, 5 : i (numéro du module), u,v, ratio (for CEE) ##########
############# 24 -> phi, 20 -> eta, maxmod... ok, 6 : i (numéro du module), u,v, ratio, indice STC (for CEH) #######


def PTTLayer(Layer,STCyesorno):
    if Layer < 27:
        return pTTModules(G,Layer)
    else :
        if not STCyesorno:
            return pTTModules(G,Layer)       #without STCs
        if STCyesorno :
            return pTTSTCs(STCLD,STCHD,Layer)  #with STCs



def constructionPTT(Layer,STCyesorno):
    listpttpermodules = PTTLayer(Layer,STCyesorno)
    if Layer < 48 and not STCyesorno : #put 48 if without STCs
        L =[[[] for j in range(20)] for i in range(24)]
        for i in range(len(listpttpermodules)):
            for j in range(len(listpttpermodules[i])):
                iptt,jptt,ratio = listpttpermodules[i][j]
                u = UV[Layer-1,i,0]
                v = UV[Layer-1,i,1]
                L[iptt][jptt].append([i,u,v,ratio])
    if Layer < 27 and STCyesorno :   # and 27 if with STCs
        L =[[[] for j in range(20)] for i in range(24)]
        for i in range(len(listpttpermodules)):
            for j in range(len(listpttpermodules[i])):
                iptt,jptt,ratio = listpttpermodules[i][j]
                u = UV[Layer-1,i,0]
                v = UV[Layer-1,i,1]
                L[iptt][jptt].append([i,u,v,ratio])

    if Layer > 26 and STCyesorno :
        L =[[[] for j in range(20)] for i in range(24)]
        for i in range(len(listpttpermodules)):
         for j in range(len(listpttpermodules[i])):
                for k in range(len(listpttpermodules[i][j])):
                    iptt,jptt,ratio = listpttpermodules[i][j][k]
                    u = UV[Layer-1,i,0]
                    v = UV[Layer-1,i,1]
                    L[iptt][jptt].append([i,u,v,j,ratio])

    return(L)


def PTTarray(Layer,STCyesorno):
    L = constructionPTT(Layer,STCyesorno)
    max = 0
    for i in range(len(L)):
        for j in range(len(L[i])):
            if len(L[i][j]) >max:
                max = len(L[i][j])
    if Layer < 27:
        A = np.zeros((24,20,max,4))
    else :
        if not STCyesorno:
            A = np.zeros((24,20,max,4)) #without STCs
        if STCyesorno:
            A = np.zeros((24,20,max,5)) #with STCs
    for i in range(len(L)):
        for j in range(len(L[i])):
            for k in range(len(L[i][j])):
                A[i,j,k] = np.array(L[i][j][k])
    return A

