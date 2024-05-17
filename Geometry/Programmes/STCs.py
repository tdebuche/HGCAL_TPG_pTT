import numpy as np
import matplotlib.pyplot as plt
import math
import os
import functions

os.chdir("../Ressources")
G = np.load('ModulesGeometry.npy')
Z = np.load("Z.npy")

#There are two scenarios for the orientation of  STCs 
Scenario = 0
Possibilities = ['first','second']
orientation = Possibilities[Scenario]
antiorientation = Possibilities[(Scenario + 1)%2]

#Create two arrays : one for HD layers (27-33) and one for LD layers (34-47)          

#1st : array(7,nb_Modules,nb_STCperModule,[[Xvertices],[Yvertices]],  2nd : array(7,nb_Modules,nb_STC,[[Xvertices],[Yvertices]]

def STCLayersLD(Geometry,Layermin, Layermax): #Returns the STCs of a LD layer (34-47)
    L=[]
    l = []
    for Layer in range(Layermin,Layermax+1):
        Modules = Geometry[Layer-1]
        for index in range(len(Modules)):
            Module = Modules[i]
            l.append(STCLD(Module,Layer,index))
        L.append(l)
        l = []
    maxmoduleperlayer  =0
    for i in range(len(L)):
        if len(L[i]) >maxmoduleperlayer:
            maxmoduleperlayer = len(L[i])
    maxstcpermodule = 0
    for i in range(len(L)):
        for j in range(len(L[i])):
            if len(L[i][j]) >maxstcpermodule:
                maxstcpermodule = len(L[i][j])
    stc = np.zeros((len(L),maxmoduleperlayer,maxstcpermodule,2,5))
    for i in range(len(L)):
        for j in range(len(L[i])):
            for k in range(len(L[i][j])):
                for m in range(len(L[i][j][k][0])):
                    stc[i,j,k,0,m] = L[i][j][k][0][m]
                    stc[i,j,k,1,m] = L[i][j][k][1][m]
    return stc

def STCLayersHD(Geometry,Layermin, Layermax): #Returns the STCs of an HD layer (27-33)
    L=[]
    l = []
    for Layer in range(Layermin,Layermax+1):
        Modules = Geometry[Layer-1]
        for index in range(len(Modules)):
            Module = Modules[index]
            l.append(STCHD(Module,Layer))
        L.append(l)
        l = []
    maxmoduleperlayer  =0
    for i in range(len(L)):
        if len(L[i]) >maxmoduleperlayer:
            maxmoduleperlayer = len(L[i])
    maxstcpermodule = 0
    for i in range(len(L)):
        for j in range(len(L[i])):
            if len(L[i][j]) >maxstcpermodule:
                maxstcpermodule = len(L[i][j])
    stc = np.zeros((len(L),maxmoduleperlayer,maxstcpermodule,2,5))
    for i in range(len(L)):
        for j in range(len(L[i])):
            for k in range(len(L[i][j])):
                for m in range(len(L[i][j][k][0])):
                    stc[i,j,k,0,m] = L[i][j][k][0][m]
                    stc[i,j,k,1,m] = L[i][j][k][1][m]
    return stc



def STCLD(Module,Layer,index): #Return the STCs of a single LD module
    if type(index,Layer) == 'Si_Module':
        a = 0
        for i in range(len(Module[0])):
            if Module[0,i] != 0 or Module[1,i] != 0:
                a +=1
        if a == 6:
            return STC6LD(Module,Layer)
        if a == 4:
            return STC4LD(Module,Layer)
        if a ==  5:
            return STC5LD(Module,Layer)
    if type(index,Layer) == 'Scintillator_Module':
        Scint_Letter,Scint_Number = Scintillatortype(index,Layer)
        return(ScintillatorSTCs(Module,Layer,Scint_Letter,Scint_Number))
    return []


def STCHD(Module,Layer): #Return the STCs of a single HD module
    z = Z[Layer-1]
    a = 0
    for i in range(len(Module[0])):
        if Module[0,i] != 0 or Module[1,i] != 0:
            a +=1
    if a != 0:
        eta,phi = functions.etaphicentre(Module,z)
        if (eta < 2.3 and z>  Z[27-1]) or (eta < 2.2 and z ==  Z[27-1]) :
            return STCLD(Module,Layer)
        if a == 6:
            return STC6HD(Module,Layer)
        if a == 4:
            return STC4HD(Module,Layer)
        if a ==  5:
            return STC5HD(Module,Layer)
    return []

def type(index,Layer): #Return the type of the module Modules[index]
    IndminScint = [95,95,95,95,72,72,52,52,52,52,37,37,37,37]
    if index < IndminScint[Layer-34]:
        return 'Si_Module'
    return 'Scintillator_Module'

def Scintillatortype(index,Layer): #Return the type of the Scintillator Modules[index], see CMS-HGC-ScintMB-Docs_V0_9 page 5
    IndminScint = [95,95,95,95,72,72,52,52,52,52,37,37,37,37]
    
    if index < IndminScint[Layer-34]:
        return 'error'
    if Layer > 33 and Layer < 38:
        if (index - IndminScint[Layer-34])%2 == 0:
            return ('J',8)
        if (index - IndminScint[Layer-34])%2 == 1:
            if Layer == 34:
                return('J',4)
            if Layer == 35:
                return('J',6)
            if Layer == 34:
                return('J',7)
            if Layer == 34:
                return('J',8)
    if Layer == 38 or Layer == 39:
        if (index - IndminScint[Layer-34])%4 == 0:
            return ('C',5)
        if (index - IndminScint[Layer-34])%4 == 1:
            return ('D',8)
        if (index - IndminScint[Layer-34])%4 == 2:
            return ('E',8)
        if (index - IndminScint[Layer-34])%4 == 3:
            if Layer == 38:
                return ('G',3)
            if Layer == 39:
                return ('G',5)
    if Layer > 39 and Layer <44:
        if (index - IndminScint[Layer-34])%4 == 0:
            return ('B',12)
        if (index - IndminScint[Layer-34])%4 == 1:
            return ('D',8)
        if (index - IndminScint[Layer-34])%4 == 2:
            return ('E',8)
        if (index - IndminScint[Layer-34])%4 == 3:
            if Layer == 40:
                return ('G',7)
            if Layer > 40 :
                return ('G',8)
    if Layer > 43:
        if (index - IndminScint[Layer-34])%5 == 0:
            return ('A',5)
        if (index - IndminScint[Layer-34])%5 == 1:
            return ('B',12)
        if (index - IndminScint[Layer-34])%5 == 2:
            return ('D',8)
        if (index - IndminScint[Layer-34])%5 == 3:
            return ('E',8)
        if (index - IndminScint[Layer-34])%5 == 4:
            if Layer < 47:
                return ('G',8)
            if Layer == 47 :
                return ('G',6)
        



#Tous les fonctions sont basés sur le même principe : trouver le sommet marker_i tel que la coupe soit définie par les sommets marker_i et marker_i +1. Ensuite, selon la position de ce sommet on peut trouver l'orientation de la coupe et donc les STC. Lorque un module  a 6 sommest (et donc est entier marker_i est le sommet en haut à gauche de l'hexagone.

def ScintillatorSTCs(Scintillator,Layer,Scint_Letter,Scint_Number):
    z = Z[Layer-1]
    L = []
    etamin,phimax = functions.XYtoetaphi(Scintillator[0,0],Scintillator[1,0],z)
    marker_i =0
    for i in range(4):
        x = Scintillator[0,i]
        y = Scintillator[1,i]
        eta,phi = functions.XYtoetaphi(x,y,z)
        if eta <= etamin and phi >= phimax:
            etamin,phimax = eta,phi
            marker_i = i
    I = np.array([(marker_i +i)%4 for i in range(4)])
    if Scint_Letter in ['J','K','D','E','G'] and Scint_Number > 5 :
        ratio = Scint_Number/8
        x1,y1 = (((Scintillator[0,I[0]]-Scintillator[0,I[1]]) /(ratio*2) +Scintillator[0,I[1]]),((Scintillator[1,I[0]]-Scintillator[1,I[1]])/(ratio*2)+Scintillator[1,I[1]]))
        x2,y2 = ((Scintillator[0,I[1]]+Scintillator[0,I[2]])/2,(Scintillator[1,I[1]]+Scintillator[1,I[2]])/2)
        x3,y3 = (((Scintillator[0,I[3]]-Scintillator[0,I[2]]) /(ratio*2) +Scintillator[0,I[2]]),((Scintillator[1,I[3]]-Scintillator[1,I[2]])/(ratio*2)+Scintillator[1,I[2]]))
        x4,y4 = ((Scintillator[0,I[3]]+Scintillator[0,I[0]])/2,(Scintillator[1,I[3]]+Scintillator[1,I[0]])/2)
        x,y = ((x1+x3)/2,y+y3)/2)
        L.append([[Scintillator[0,I[0]],x1,x,x4],[Scintillator[1,I[0]],y1,y,y4]])
        L.append([[Scintillator[0,I[1]],x2,x,x1],[Scintillator[1,I[1]],y2,y,y1]])
        L.append([[Scintillator[0,I[2]],x3,x,x2],[Scintillator[1,I[2]],y3,y,y2]])
        L.append([[Scintillator[0,I[3]],x4,x,x3],[Scintillator[1,I[3]],y4,y,y3]])
    if Scint_Letter in ['A','B','C']:
        ratio = Scint_Number/8
        x1,y1 = (((Scintillator[0,I[1]]-Scintillator[0,I[0]]) /(ratio*2) +Scintillator[0,I[0]]),((Scintillator[1,I[1]]-Scintillator[1,I[0]])/(ratio*2)+Scintillator[1,I[0]]))
        x2,y2 = ((Scintillator[0,I[1]]+Scintillator[0,I[2]])/2,(Scintillator[1,I[1]]+Scintillator[1,I[2]])/2)
        x3,y3 = (((Scintillator[0,I[2]]-Scintillator[0,I[3]]) /(ratio*2) +Scintillator[0,I[3]]),((Scintillator[1,I[2]]-Scintillator[1,I[3]])/(ratio*2)+Scintillator[1,I[3]]))
        x4,y4 = ((Scintillator[0,I[3]]+Scintillator[0,I[0]])/2,(Scintillator[1,I[3]]+Scintillator[1,I[0]])/2)
        x,y = ((x1+x3)/2,y+y3)/2)
        L.append([[Scintillator[0,I[0]],x1,x,x4],[Scintillator[1,I[0]],y1,y,y4]])
        L.append([[Scintillator[0,I[1]],x2,x,x1],[Scintillator[1,I[1]],y2,y,y1]])
        L.append([[Scintillator[0,I[2]],x3,x,x2],[Scintillator[1,I[2]],y3,y,y2]])
        L.append([[Scintillator[0,I[3]],x4,x,x3],[Scintillator[1,I[3]],y4,y,y3]])
    if Scint_Letter in ['J','K','D','E','G'] and Scint_Number <= 5 :
        x2,y2 = ((Scintillator[0,I[1]]+Scintillator[0,I[2]])/2,(Scintillator[1,I[1]]+Scintillator[1,I[2]])/2)
        x4,y4 = ((Scintillator[0,I[3]]+Scintillator[0,I[0]])/2,(Scintillator[1,I[3]]+Scintillator[1,I[0]])/2)
        L.append([[Scintillator[0,I[0]],Scintillator[0,I[1]],x2,x4],[Scintillator[1,I[0]],Scintillator[1,I[1]],y2,y4]])
        L.append([[Scintillator[0,I[2]],Scintillator[0,I[3]],x4,x2],[Scintillator[1,I[2]],Scintillator[1,I[3]],y4,y2]])
    return L

def STC6LD(Module,Layer): #Return the STCs of a single LD module with 6 vertices
    z = Z[Layer-1]
    L = []
    xmin = Module[0,0]
    marker_i =0
    for i in range(len(Module[0])):
        x = Module[0,i]
        if  x < xmin-0.5:
            marker_i = i
            xmin = x
    if Module[1,(marker_i +1)%6] >Module[1,marker_i] and  Module[0,(marker_i +1)%6] == Module[0,marker_i]:
        marker_i = (marker_i +1)%6
    I = np.array([(marker_i +i)%6 for i in range(6)])
    eta,phi = functions.etaphicentre(Module,z)
    x,y = functions.etaphitoXY(eta,phi,z)
    if orientation == 'first':
        L.append([[Module[0,I[4]],Module[0,I[5]],Module[0,I[0]],x],[Module[1,I[4]],Module[1,I[5]],Module[1,I[0]],y]])
        L.append([[Module[0,I[0]],Module[0,I[1]],Module[0,I[2]],x],[Module[1,I[0]],Module[1,I[1]],Module[1,I[2]],y]])
        L.append([[Module[0,I[2]],Module[0,I[3]],Module[0,I[4]],x],[Module[1,I[2]],Module[1,I[3]],Module[1,I[4]],y]])

    if orientation == 'second':
        L.append([[Module[0,I[0]],Module[0,I[1]],x,Module[0,I[5]]],[Module[1,I[0]],Module[1,I[1]],y,Module[1,I[5]]]])
        L.append([[Module[0,I[1]],Module[0,I[2]],Module[0,I[3]],x],[Module[1,I[1]],Module[1,I[2]],Module[1,I[3]],y]])
        L.append([[Module[0,I[3]],Module[0,I[4]],Module[0,I[5]],x],[Module[1,I[3]],Module[1,I[4]],Module[1,I[5]],y]])
    return(L)

def STC6HD(Module,Layer): #Return the STCs of a single HD module with 6 vertices
    z = Z[Layer-1]
    L = []
    xmin = Module[0,0]
    marker_i =0
    for i in range(len(Module[0])):
        x = Module[0,i]
        if  x < xmin-0.5:
            marker_i = i
            xmin = x
    if Module[1,(marker_i +1)%6] >Module[1,marker_i] and  Module[0,(marker_i +1)%6] == Module[0,marker_i]:
        marker_i = (marker_i +1)%6
    I = np.array([(marker_i +i-2)%6 for i in range(6)])
    eta,phi = functions.etaphicentre(Module,z)
    x,y = functions.etaphitoXY(eta,phi,z)
    if orientation == 'first':
        for par in range(3):
            centrepetit = np.array([[Module[0,I[0]],Module[0,I[1]],Module[0,I[2]],x],[Module[1,I[0]],Module[1,I[1]],Module[1,I[2]],y]])
            etap,phip=functions.etaphicentre(centrepetit,z)
            xp,yp = functions.etaphitoXY(etap,phip,z)
            x1,y1 = ((Module[0,I[0]]+Module[0,I[1]])/2,(Module[1,I[0]]+Module[1,I[1]])/2)
            x2,y2 = ((Module[0,I[1]]+Module[0,I[2]])/2,(Module[1,I[1]]+Module[1,I[2]])/2)
            x3,y3 = ((Module[0,I[2]]+x)/2,(Module[1,I[2]]+y)/2)
            x4,y4 = ((Module[0,I[0]]+x)/2,(Module[1,I[0]]+y)/2)
            first = [[Module[0,I[1]],x2,xp,x1],[Module[1,I[1]],y2,yp,y1]]
            second = [[Module[0,I[2]],x3,xp,x2],[Module[1,I[2]],y3,yp,y2]]
            third = [[x,x4,xp,x3],[y,y4,yp,y3]]
            fourth = [[Module[0,I[0]],x1,xp,x4],[Module[1,I[0]],y1,yp,y4]]
            L.append(first)
            L.append(second)
            L.append(third)
            L.append(fourth)
            I = (I + 2)%6

    if orientation == 'second':
        for par in range(3):
            centrepetit = np.array([[Module[0,I[0]],Module[0,I[1]],x,Module[0,I[5]]],[Module[1,I[0]],Module[1,I[1]],y,Module[1,I[5]]]])
            etap,phip= functions.etaphicentre(centrepetit,z)
            xp,yp = functions.etaphitoXY(etap,phip,z)
            x1,y1 = ((Module[0,I[0]]+Module[0,I[1]])/2,(Module[1,I[0]]+Module[1,I[1]])/2)
            x2,y2 = ((Module[0,I[1]]+x)/2,(Module[1,I[1]]+y)/2)
            x3,y3 = ((Module[0,I[5]]+x)/2,(Module[1,I[5]]+y)/2)
            x4,y4 = ((Module[0,I[0]]+Module[0,I[5]])/2,(Module[1,I[0]]+Module[1,I[5]])/2)
            first = [[Module[0,I[0]],x1,xp,x4],[Module[1,I[0]],y1,yp,y4]]
            second = [[Module[0,I[1]],x2,xp,x1],[Module[1,I[1]],y2,yp,y1]]
            third = [[x,x3,xp,x2],[y,y3,yp,y2]]
            fourth = [[Module[0,I[5]],x4,xp,x3],[Module[1,I[5]],y4,yp,y3]]
            L.append(first)
            L.append(second)
            L.append(third)
            L.append(fourth)
            I = (I + 2)%6
    return(L)

def STC4LD(Module,Layer): #Return the STCs of a single LD module with 4 vertices
    z = Z[Layer-1]
    L = []
    res = 0
    marker_i =0
    xmin = Module[0,0]
    ymin = Module[1,0]
    xmax = Module[0,0]
    ymax = Module[1,0]
    ixmin = 0
    ixmax = 0
    iymin=0
    iymax = 0
    for i in range(4):
        if i < 3:
            dist = (Module[0,i]-Module[0,i+1])**2 + (Module[1,i]-Module[1,i+1])**2
            if  dist > res:
                marker_i = i
                res = dist
        if i == 3:
            dist = (Module[0,i]-Module[0,0])**2 + (Module[1,i]-Module[1,0])**2
            if  dist > res:
                marker_i = i
                res = dist
    for i in range(4):
        x = Module[0,i]
        y = Module[1,i]
        if  x < xmin:
            ixmin = i
            xmin = x
        if  x > xmax:
            ixmax = i
            xmax = x
        if  y < ymin:
            iymin = i
            ymin = y
        if  y > ymax:
            iymax = i
            ymax = y
    x,y = ((Module[0,marker_i]+Module[0,marker_i+1])/2,(Module[1,marker_i]+Module[1,marker_i+1])/2)
    I =np.array([(i+marker_i) for i in range(4)])%4
    type = 0
    subtype = 0
    if Module[0,marker_i] == xmin and Module[1,marker_i] == ymax:
        type = 'first'
        subtype = 0
    if Module[0,marker_i] == xmax and Module[1,marker_i] == ymin:
        type = 'second'
        subtype = 0
    if Module[0,marker_i] == xmin and Module[1,marker_i] == ymin:
        type = 'first'
        subtype = 1
    if Module[0,marker_i] == xmax and Module[1,marker_i] != ymin and Module[1,marker_i] != ymax:
        type = 'first'
        subtype = 1
    if Module[0,marker_i] == xmin and Module[1,marker_i] != ymin and Module[1,marker_i] != ymax:
        type = 'second'
        subtype = 1
    if Module[0,marker_i] == xmax and Module[1,marker_i] == ymax:
        type = 'second'
        subtype = 0
    a =np.sqrt((Module[0,I[1]]-Module[0,I[2]])**2 + (Module[1,I[1]]-Module[1,I[2]])**2)
    c = np.sqrt((Module[0,I[2]]-Module[0,I[3]])**2 + (Module[1,I[2]]-Module[1,I[3]])**2)
    if type == orientation:
        px = Module[0,I[0]] + a/(np.sqrt(res)) * (Module[0,I[1]]-Module[0,I[0]])
        py = Module[1,I[0]] + a/(np.sqrt(res)) * (Module[1,I[1]]-Module[1,I[0]])
        small = [[Module[0,I[0]],px,Module[0,I[3]]],[Module[1,I[0]],py,Module[1,I[3]]]]
        big =[[Module[0,I[1]],Module[0,I[2]],Module[0,I[3]],px],[Module[1,I[1]],Module[1,I[2]],Module[1,I[3]],py]]
    if type == antiorientation:
        px = Module[0,I[0]] + (1-a/np.sqrt(res)) * (Module[0,I[1]]-Module[0,I[0]])
        py = Module[1,I[0]] + (1-a/np.sqrt(res)) * (Module[1,I[1]]-Module[1,I[0]])
        big = [[Module[0,I[0]],px,Module[0,I[2]],Module[0,I[3]]],[Module[1,I[0]],py,Module[1,I[2]],Module[1,I[3]]]]
        small = [[Module[0,I[1]],Module[0,I[2]],px],[Module[1,I[1]],Module[1,I[2]],py]]
    if subtype == 0:
        L.append(small)
        L.append(big)
    if subtype == 1:
        L.append(big)
        L.append(small)
    return(L)


def STC4HD(Module,Layer): #Return the STCs of a single HD module with 4 vertices
    z = Z[Layer-1]
    L = []
    res = 0
    marker_i =0
    xmin = Module[0,0]
    ymin = Module[1,0]
    xmax = Module[0,0]
    ymax = Module[1,0]
    ixmin = 0
    ixmax = 0
    iymin=0
    iymax = 0
    for i in range(4):
        if i < 3:
            dist = (Module[0,i]-Module[0,i+1])**2 + (Module[1,i]-Module[1,i+1])**2
            if  dist > res:
                marker_i = i
                res = dist
        if i == 3:
            dist = (Module[0,i]-Module[0,0])**2 + (Module[1,i]-Module[1,0])**2
            if  dist > res:
                marker_i = i
                res = dist
    for i in range(4):
        x = Module[0,i]
        y = Module[1,i]
        if  x < xmin:
            ixmin = i
            xmin = x
        if  x > xmax:
            ixmax = i
            xmax = x
        if  y < ymin:
            iymin = i
            ymin = y
        if  y > ymax:
            iymax = i
            ymax = y
    x,y = ((Module[0,marker_i]+Module[0,marker_i+1])/2,(Module[1,marker_i]+Module[1,marker_i+1])/2)
    I =np.array([(i+marker_i) for i in range(4)])%4
    type = 0
    subtype = 0
    if Module[0,marker_i] == xmin and Module[1,marker_i] == ymax:
        type = 'first'
        subtype = 0
    if Module[0,marker_i] == xmax and Module[1,marker_i] == ymin:
        type = 'second'
        subtype =1
    if Module[0,marker_i] == xmin and Module[1,marker_i] == ymin:
        type = 'first'
        subtype = 1
    if Module[0,marker_i] == xmax and Module[1,marker_i] != ymin and Module[1,marker_i] != ymax:
        type = 'first'
        subtype = 1
    if Module[0,marker_i] == xmin and Module[1,marker_i] != ymin and Module[1,marker_i] != ymax:
        type = 'second'
        subtype = 0
    if Module[0,marker_i] == xmax and Module[1,marker_i] == ymax:
        type = 'second'
        subtype = 1
    a =np.sqrt((Module[0,I[1]]-Module[0,I[2]])**2 + (Module[1,I[1]]-Module[1,I[2]])**2)
    c = np.sqrt((Module[0,I[2]]-Module[0,I[3]])**2 + (Module[1,I[2]]-Module[1,I[3]])**2)
    if type == orientation:

        X1 = Module[:,I[3]] + (Module[:,I[0]]-Module[:,I[3]]) *c/(2*a)
        P = Module[:,I[0]] + (Module[:,I[1]]-Module[:,I[0]]) *a/(np.sqrt(res))
        X4 = Module[:,I[3]] + (P-Module[:,I[3]]) *c/(2*a)
        X8 = Module[:,I[2]] + (Module[:,I[1]]-Module[:,I[2]]) *c/(2*a)
        X = Module[:,I[0]] + (Module[:,I[1]]-Module[:,I[0]]) *((a-c/2)/np.sqrt(res))
        Y = P + (Module[:,I[0]]-Module[:,I[1]]) *((a-c/2)/(np.sqrt(res)))
        if (X[0]-Y[0])**2 + (X[1]-Y[1])**2 < 0.01:
            Y = X
        Z = (P + Module[:,I[1]])/2
        P3 = (X4 + X8) /2
        x1,y1  = (X1[0],X1[1])
        x4,y4 = (X4[0],X4[1])
        x8,y8 = (X8[0],X8[1])
        x9,y9 = ((Module[0,I[2]]+Module[0,I[3]])/2,(Module[1,I[2]]+Module[1,I[3]])/2)
        xp3,yp3 = (P3[0],P3[1])
        xX,yX = (X[0],X[1])
        xY,yY = (Y[0],Y[1])
        xZ,yZ = (Z[0],Z[1])
        xP,yP =(P[0],P[1])
        first = [[Module[0,I[0]],xX,x1],[Module[1,I[0]],yX,y1]]
        second = [[xY,xP,x4],[yY,yP,y4]]
        third = [[Module[0,I[3]],x1,xX,xY,x4],[Module[1,I[3]],y1,yX,yY,y4]]
        fourth =  [[Module[0,I[2]],x9,xp3,x8],[Module[1,I[2]],y9,yp3,y8]]
        fifth = [[Module[0,I[3]],x4,xp3,x9],[Module[1,I[3]],y4,yp3,y9]]
        sixth =[[xP,xZ,xp3,x4],[yP,yZ,yp3,y4]]
        seventh = [[Module[0,I[1]],x8,xp3,xZ],[Module[1,I[1]],y8,yp3,yZ]]
        if subtype == 0:
            L.append(first)
            L.append(second)
            L.append(third)
            L.append(fourth)
            L.append(fifth)
            L.append(sixth)
            L.append(seventh)
        if subtype ==1:
            L.append(fourth)
            L.append(fifth)
            L.append(sixth)
            L.append(seventh)
            L.append(first)
            L.append(second)
            L.append(third)
    if type == antiorientation:
        X2 = Module[:,I[2]] + (Module[:,I[1]]-Module[:,I[2]]) *c/(2*a)
        P = Module[:,I[1]] + (Module[:,I[0]]-Module[:,I[1]]) *a/(np.sqrt(res))
        X6 = Module[:,I[3]] + (Module[:,I[0]]-Module[:,I[3]]) *c/(2*a)
        X3 = Module[:,I[2]] + (P-Module[:,I[2]]) *c/(2*a)
        X = Module[:,I[1]] + (Module[:,I[0]]-Module[:,I[1]]) *((a-c/2)/np.sqrt(res))
        Y = P + (Module[:,I[1]]-Module[:,I[0]]) *((a-c/2)/(np.sqrt(res)))
        if (X[0]-Y[0])**2 + (X[1]-Y[1])**2 < 0.01:
            Y = X
        Z = (P + Module[:,I[0]])/2
        P2 = (X3 + X6) /2
        x2,y2  = (X2[0],X2[1])
        x6,y6 = (X6[0],X6[1])
        x3,y3 = (X3[0],X3[1])
        x5,y5 = ((Module[0,I[2]]+Module[0,I[3]])/2,(Module[1,I[2]]+Module[1,I[3]])/2)
        xp2,yp2 = (P2[0],P2[1])
        xX,yX = (X[0],X[1])
        xY,yY = (Y[0],Y[1])
        xZ,yZ = (Z[0],Z[1])
        xP,yP =(P[0],P[1])
        first = [[Module[0,I[3]],x6,xp2,x5],[Module[1,I[3]],y6,yp2,y5]]
        second =  [[Module[0,I[0]],xZ,xp2,x6],[Module[1,I[0]],yZ,yp2,y6]]
        third = [[xZ,xP,x3,xp2],[yZ,yP,y3,yp2]]
        fourth = [[Module[0,I[2]],x5,xp2,x3],[Module[1,I[2]],y5,yp2,y3]]
        fifth = [[Module[0,I[1]],x2,xX],[Module[1,I[1]],y2,yX]]
        sixth = [[Module[0,I[2]],x3,xY,xX,x2],[Module[1,I[2]],y3,yY,yX,y2]]
        seventh = [[xP,xY,x3],[yP,yY,y3]]
        if subtype == 0:
            L.append(first)
            L.append(second)
            L.append(third)
            L.append(fourth)
            L.append(fifth)
            L.append(sixth)
            L.append(seventh)
        if subtype == 1:
            L.append(fifth)
            L.append(sixth)
            L.append(seventh)
            L.append(first)
            L.append(second)
            L.append(third)
            L.append(fourth)
    return(L)


def STC5LD(Module,Layer):  #Return the STCs of a single LD module with 5 vertices
    z = Z[Layer-1]
    res = 0
    marker_i =0
    for i in range(5):
        if i < 4:
            dist = (Module[0,i]-Module[0,i+1])**2 + (Module[1,i]-Module[1,i+1])**2
            if  dist > res:
                marker_i = i
                res = dist
        if i == 4:
            dist = (Module[0,i]-Module[0,0])**2 + (Module[1,i]-Module[1,0])**2
            if  dist > res:
                marker_i = i
                res = dist
    typemod = 0
    for i in range(5):
        if i < 4:
            dist = (Module[0,i]-Module[0,i+1])**2 + (Module[1,i]-Module[1,i+1])**2
            if  dist < res/4:
                typemod = 1
        if i == 4:
            dist = (Module[0,i]-Module[0,0])**2 + (Module[1,i]-Module[1,0])**2
            if  dist < res/4:
                typemod = 1
    if typemod == 0:
        return STC5bigLD(Module,Layer,marker_i)
    if typemod == 1:
        return STC5smallLD(Module,Layer,marker_i)

def STC5HD(Module,Layer):  #Return the STCs of a single HD module with 5 vertices
    z = Z[Layer-1]
    res = 0
    marker_i =0
    for i in range(5):
        if i < 4:
            dist = (Module[0,i]-Module[0,i+1])**2 + (Module[1,i]-Module[1,i+1])**2
            if  dist > res:
                marker_i = i
                res = dist
        if i == 4:
            dist = (Module[0,i]-Module[0,0])**2 + (Module[1,i]-Module[1,0])**2
            if  dist > res:
                marker_i = i
                res = dist
    typemod = 0
    for i in range(5):
        if i < 4:
            dist = (Module[0,i]-Module[0,i+1])**2 + (Module[1,i]-Module[1,i+1])**2
            if  dist < res/4:
                typemod = 1
        if i == 4:
            dist = (Module[0,i]-Module[0,0])**2 + (Module[1,i]-Module[1,0])**2
            if  dist < res/4:
                typemod = 1
    if typemod == 0:
        return STC5bigHD(Module,Layer,marker_i)
    if typemod == 1:
        return STC5smallHD(Module,Layer,marker_i)


def STC5bigLD(Module,Layer,marker_i):  #Return the STCs of a single LD module with 5 vertices (when the type of the truncated module is "big"(two cuts are possible with 5vertices))
    z = Z[Layer-1]
    L = []
    xmin = Module[0,0]
    ymin = Module[1,0]
    xmax = Module[0,0]
    ymax = Module[1,0]
    ixmin = 0
    ixmax = 0
    iymin=0
    iymax = 0
    for i in range(5):
        x = Module[0,i]
        y = Module[1,i]
        if  x < xmin:
            ixmin = i
            xmin = x
        if  x > xmax:
            ixmax = i
            xmax = x
        if  y < ymin:
            iymin = i
            ymin = y
        if  y > ymax:
            iymax = i
            ymax = y
    I  = np.array([(marker_i + j)  for j in range(5)])%5
    centre = np.array([[Module[0,(marker_i+j)%5] for j in [0,1,2,4]],[Module[1,(marker_i+j)%5] for j in [0,1,2,4]]])
    eta,phi = functions.etaphicentre(centre,z)
    x,y = functions.etaphitoXY(eta,phi,z)
    type = 0
    subtype = 0
    if np.abs(Module[0,marker_i]-xmax)<0.5 and np.abs(Module[1,marker_i] - ymax)<0.5:
        type = 'first'
        subtype = 0
    if np.abs(Module[0,marker_i]- xmin)<0.5 and np.abs(Module[1,marker_i]-ymin)<0.5:
        type = 'second'
        subtype = 0
    if np.abs(Module[0,marker_i] - xmin)<0.5 and np.abs(Module[1,marker_i] - ymin)>0.5 and np.abs(Module[1,marker_i] - ymax)>0.5:
        type = 'first'
        subtype = 1
    if np.abs(Module[0,marker_i] -xmax)<0.5 and np.abs(Module[1,marker_i] - ymin)>0.5 and np.abs(Module[1,marker_i] - ymax)>0.5:
        type = 'second'
        subtype = 1
    if np.abs(Module[0,marker_i] - xmin)>0.5 and np.abs(Module[0,marker_i] - xmax)>0.5 and np.abs(Module[1,marker_i] - ymin)<0.5:
        type = 'first'
        subtype = 2
    if np.abs(Module[0,marker_i] - xmin)>0.5 and np.abs(Module[0,marker_i] - xmax)>0.5 and np.abs(Module[1,marker_i] - ymax)<0.5:
        type = 'second'
        subtype = 2
    if type == orientation:
        small = [[Module[0,I[0]],Module[0,I[1]],x],[Module[1,I[0]],Module[1,I[1]],y]]
        big1 = [[Module[0,I[1]],Module[0,I[2]],Module[0,I[3]],x],[Module[1,I[1]],Module[1,I[2]],Module[1,I[3]],y]]
        big2 = [[Module[0,I[3]],Module[0,I[4]],Module[0,I[0]],x],[Module[1,I[3]],Module[1,I[4]],Module[1,I[0]],y]]
        if subtype == 0:
            L.append(small)
            L.append(big1)
            L.append(big2)
        if subtype == 1:
            L.append(big2)
            L.append(small)
            L.append(big1)
        if subtype == 2:
            L.append(big1)
            L.append(big2)
            L.append(small)
    if  type == antiorientation:
        X,Y = ((Module[0,marker_i]+Module[0,marker_i+1])/2,(Module[1,marker_i]+Module[1,marker_i+1])/2)
        small1 =[[Module[0,I[0]],X,x,Module[0,I[4]]],[Module[1,I[0]],Y,y,Module[1,I[4]]]]
        small2 = [[Module[0,I[1]],Module[0,I[2]],x,X],[Module[1,I[1]],Module[1,I[2]],y,Y]]
        big  = [[Module[0,I[2]],Module[0,I[3]],Module[0,I[4]],x],[Module[1,I[2]],Module[1,I[3]],Module[1,I[4]],y]]
        if subtype == 0:
            L.append(big)
            L.append(small1)
            L.append(small2)
        if subtype == 1:
            L.append(small2)
            L.append(big)
            L.append(small1)
        if subtype == 2:
            L.append(small1)
            L.append(small2)
            L.append(big)
    return L


def STC5bigHD(Module,Layer,marker_i):  #Return the STCs of a single HD module with 5 vertices, for a "big" module
    L = []
    xmin = Module[0,0]
    ymin = Module[1,0]
    xmax = Module[0,0]
    ymax = Module[1,0]
    ixmin = 0
    ixmax = 0
    iymin=0
    iymax = 0
    for i in range(5):
        x = Module[0,i]
        y = Module[1,i]
        if  x < xmin:
            ixmin = i
            xmin = x
        if  x > xmax:
            ixmax = i
            xmax = x
        if  y < ymin:
            iymin = i
            ymin = y
        if  y > ymax:
            iymax = i
            ymax = y
    I  = np.array([(marker_i + j)  for j in range(5)])%5
    centre = np.array([[Module[0,(marker_i+j)%5] for j in [0,1,2,4]],[Module[1,(marker_i+j)%5] for j in [0,1,2,4]]])
    eta,phi = functions.etaphicentre(centre,z)
    x,y = functions.etaphitoXY(eta,phi,z)

    type = 0
    if Module[0,marker_i] == xmax and Module[1,marker_i] == ymax:
        type = 'first'
    if Module[0,marker_i] == xmin and Module[1,marker_i] == ymin:
        type = 'second'
    if Module[0,marker_i] == xmin and Module[1,marker_i] != ymin and Module[1,marker_i] != ymax:
        type = 'first'
    if Module[0,marker_i] == xmax and Module[1,marker_i] != ymin and Module[1,marker_i] != ymax:
        type = 'second'
    if Module[0,marker_i] != xmin and Module[0,marker_i] != xmax and Module[1,marker_i] == ymin:
        type = 'first'
    if Module[0,marker_i] != xmin and Module[0,marker_i] != xmax and Module[1,marker_i] == ymax:
        type = 'second'
    if type == orientation:
        xp1,yp1 = ((Module[0,I[0]]+Module[0,I[1]])/2,(Module[1,I[0]]+Module[1,I[1]])/2)
        xp2,yp2 = ((Module[0,I[2]]+x)/2,(Module[1,I[2]]+y)/2)
        xp3,yp3 = ((Module[0,I[4]]+x)/2,(Module[1,I[4]]+y)/2)
        x3,y3  = ((x+Module[0,I[1]])/2,(y+Module[1,I[1]])/2)
        x4,y4 = ((Module[0,I[0]]+x)/2,(Module[1,I[0]]+y)/2)
        x5,y5 = ((Module[0,I[1]]+Module[0,I[2]])/2,(Module[1,I[1]]+Module[1,I[2]])/2)
        x6,y6 = ((Module[0,I[2]]+Module[0,I[3]])/2,(Module[1,I[2]]+Module[1,I[3]])/2)
        x7, y7 = ((x+Module[0,I[3]])/2,(y+Module[1,I[3]])/2)
        x8,y8 = ((Module[0,I[3]]+Module[0,I[4]])/2,(Module[1,I[3]]+Module[1,I[4]])/2)
        x9,y9 = ((Module[0,I[4]]+Module[0,I[0]])/2,(Module[1,I[4]]+Module[1,I[0]])/2)
        L.append([[Module[0,I[0]],xp1,x4],[Module[1,I[0]],yp1,y4]])
        L.append([[xp1,x3,x,x4],[yp1,y3,y,y4]])
        L.append([[Module[0,I[1]],x3,xp1],[Module[1,I[1]],y3,yp1]])
        L.append([[Module[0,I[1]],x5,xp2,x3],[Module[1,I[1]],y5,yp2,y3]])
        L.append([[Module[0,I[2]],x6,xp2,x5],[Module[1,I[2]],y6,yp2,y5]])
        L.append([[x3,xp2,x7,x],[y3,yp2,y7,y]])
        L.append([[Module[0,I[3]],x7,xp2,x6],[Module[1,I[3]],y7,yp2,y6]])
        L.append([[Module[0,I[3]],x8,xp3,x7],[Module[1,I[3]],y8,yp3,y7]])
        L.append([[Module[0,I[4]],x9,xp3,x8],[Module[1,I[4]],y9,yp3,y8]])
        L.append([[Module[0,I[0]],x4,xp3,x9],[Module[1,I[0]],y4,yp3,y9]])
        L.append([[x7,xp3,x4,x],[y7,yp3,y4,y]])

    if  type == antiorientation:
        xp1,yp1 = ((Module[0,I[3]]+x)/2,(Module[1,I[3]]+y)/2)
        X0,Y0 = ((Module[0,I[0]]+Module[0,I[1]])/2,(Module[1,I[0]]+Module[1,I[1]])/2)
        xp3,yp3 = ((Module[0,I[2]]+x)/2,(Module[1,I[2]]+y)/2)
        x3,y3 = ((Module[0,I[4]]+x)/2,(Module[1,I[4]]+y)/2)
        xp3,yp3  = ((x+Module[0,I[1]])/2,(y+Module[1,I[1]])/2)
        xp2,yp2 = ((Module[0,I[0]]+x)/2,(Module[1,I[0]]+y)/2)
        x9,y9 = ((Module[0,I[1]]+Module[0,I[2]])/2,(Module[1,I[1]]+Module[1,I[2]])/2)
        x1,y1 = ((Module[0,I[2]]+Module[0,I[3]])/2,(Module[1,I[2]]+Module[1,I[3]])/2)
        x4, y4 = ((x+Module[0,I[2]])/2,(y+Module[1,I[2]])/2)
        x2,y2 = ((Module[0,I[3]]+Module[0,I[4]])/2,(Module[1,I[3]]+Module[1,I[4]])/2)
        x5,y5 = ((Module[0,I[4]]+Module[0,I[0]])/2,(Module[1,I[4]]+Module[1,I[0]])/2)
        X1,Y1 = ((Module[0,I[0]]+X0)/2,(Module[1,I[0]]+Y0)/2)
        X2,Y2 = ((X0+Module[0,I[1]])/2,(Y0+Module[1,I[1]])/2)
        L.append([[Module[0,I[0]],X1,xp2,x5],[Module[1,I[0]],Y1,yp2,y5]])
        L.append([[X1,X0,xp2],[Y1,Y0,yp2]])
        L.append([[x3,xp2,X0,x],[y3,yp2,Y0,y]])
        L.append([[Module[0,I[1]],x9,xp3,X2],[Module[1,I[1]],y9,yp3,Y2]])
        L.append([[X0,X2,xp3],[Y0,Y2,yp3]])
        L.append([[X0,xp3,x4,x],[Y0,yp3,y4,y]])
        L.append([[Module[0,I[2]],x4,xp3,x9],[Module[1,I[2]],y4,yp3,y9]])
        L.append([[Module[0,I[2]],x1,xp1,x4],[Module[1,I[2]],y1,yp1,y4]])
        L.append([[x3,x,x4,xp1],[y3,y,y4,yp1]])
        L.append([[Module[0,I[3]],x2,xp1,x1],[Module[1,I[3]],y2,yp1,y1]])
        L.append([[Module[0,I[4]],x3,xp1,x2],[Module[1,I[4]],y3,yp1,y2]])
        L.append([[Module[0,I[4]],x5,xp2,x3],[Module[1,I[4]],y5,yp2,y3]])
    return L

def STC5smallLD(Module,Layer,marker_i):  #Return the STCs of a single small LD module with 5 vertices
    z = Z[Layer-1]
    L = []
    xmin = Module[0,0]
    ymin = Module[1,0]
    xmax = Module[0,0]
    ymax = Module[1,0]
    ixmin = 0
    ixmax = 0
    iymin=0
    iymax = 0
    for i in range(5):
        x = Module[0,i]
        y = Module[1,i]
        if  x < xmin:
            ixmin = i
            xmin = x
        if  x > xmax:
            ixmax = i
            xmax = x
        if  y < ymin:
            iymin = i
            ymin = y
        if  y > ymax:
            iymax = i
            ymax = y
    type = 0
    subtype = 0
    if Module[0,marker_i] == xmax and Module[1,marker_i] == ymax:
        type = 'first'
        subtype = 1
    if Module[0,marker_i] == xmin and Module[1,marker_i] == ymin:
        type = 'second'
        subtype = 1
    if Module[0,marker_i] == xmin and Module[1,marker_i] != ymin and Module[1,marker_i] != ymax:
        type = 'first'
        subtype = 0
    if Module[0,marker_i] == xmax and Module[1,marker_i] != ymin and Module[1,marker_i] != ymax:
        type = 'second'
        subtype = 2
    if Module[0,marker_i] != xmin and Module[0,marker_i] != xmax and Module[1,marker_i] == ymin:
        type = 'first'
        subtype = 1
    if Module[0,marker_i] != xmin and Module[0,marker_i] != xmax and Module[1,marker_i] == ymax:
        type = 'second'
        subtype = 0
    x,y = ((Module[0,marker_i]+Module[0,(marker_i+1)%5])/2,(Module[1,marker_i]+Module[1,(marker_i+1)%5])/2)
    I  = np.array([(marker_i + j)  for j in range(5)])%5
    if type == orientation:
        first = [[Module[0,I[0]],x,Module[0,I[3]],Module[0,I[4]]],[Module[1,I[0]],y,Module[1,I[3]],Module[1,I[4]]]]
        second = [[Module[0,I[1]],Module[0,I[2]],Module[0,I[3]],x],[Module[1,I[1]],Module[1,I[2]],Module[1,I[3]],y]]
        if subtype ==0:
            L.append(first)
            L.append(second)
        if subtype ==1:
            L.append(second)
            L.append(first)
    if type == antiorientation:
        small1 = [[Module[0,I[0]],x,Module[0,I[4]]],[Module[1,I[0]],y,Module[1,I[4]]]]
        small2 = [[Module[0,I[1]],Module[0,I[2]],x],[Module[1,I[1]],Module[1,I[2]],y]]
        big = [[Module[0,I[2]],Module[0,I[3]],Module[0,I[4]],x],[Module[1,I[2]],Module[1,I[3]],Module[1,I[4]],y]]
        if subtype == 0:
            L.append(small1)
            L.append(small2)
            L.append(big)
        if subtype == 2:
            L.append(small2)
            L.append(big)
            L.append(small1)
        if subtype == 1:
            L.append(big)
            L.append(small1)
            L.append(small2)
    return L


def STC5smallHD(Module,Layer,marker_i):  #Return the STCs of a single small HD module with 5 vertices
    z = Z[Layer-1]
    L = []
    xmin = Module[0,0]
    ymin = Module[1,0]
    xmax = Module[0,0]
    ymax = Module[1,0]
    ixmin = 0
    ixmax = 0
    iymin=0
    iymax = 0
    for i in range(5):
        x = Module[0,i]
        y = Module[1,i]
        if  x < xmin:
            ixmin = i
            xmin = x
        if  x > xmax:
            ixmax = i
            xmax = x
        if  y < ymin:
            iymin = i
            ymin = y
        if  y > ymax:
            iymax = i
            ymax = y
    type = 0
    if Module[0,marker_i] == xmax and Module[1,marker_i] == ymax:
        type = 'first'
    if Module[0,marker_i] == xmin and Module[1,marker_i] == ymin:
        type = 'second'
    if Module[0,marker_i] == xmin and Module[1,marker_i] != ymin and Module[1,marker_i] != ymax:
        type = 'first'
    if Module[0,marker_i] == xmax and Module[1,marker_i] != ymin and Module[1,marker_i] != ymax:
        type = 'second'
    if Module[0,marker_i] != xmin and Module[0,marker_i] != xmax and Module[1,marker_i] == ymin:
        type = 'first'
    if Module[0,marker_i] != xmin and Module[0,marker_i] != xmax and Module[1,marker_i] == ymax:
        type = 'second'
    x,y = ((Module[0,marker_i]+Module[0,(marker_i+1)%5])/2,(Module[1,marker_i]+Module[1,(marker_i+1)%5])/2)
    I  = np.array([(marker_i + j)  for j in range(5)])%5
    if type == orientation:
        X1,Y1 = ((Module[0,I[0]]+x)/2,(Module[1,I[0]]+y)/2)
        X2,Y2 = ((Module[0,I[1]]+x)/2,(Module[1,I[1]]+y)/2)
        x7, y7 = ((x+Module[0,I[3]])/2,(y+Module[1,I[3]])/2)
        xp2,yp2 = ((x7+Module[0,I[1]])/2,(y7+Module[1,I[1]])/2)
        xp3,yp3 = ((Module[0,I[0]]+x7)/2,(Module[1,I[0]]+y7)/2)
        x6,y6 = ((Module[0,I[2]]+Module[0,I[3]])/2,(Module[1,I[2]]+Module[1,I[3]])/2)
        x8,y8 = ((Module[0,I[3]]+Module[0,I[4]])/2,(Module[1,I[3]]+Module[1,I[4]])/2)
        L.append([[Module[0,I[0]],X1,xp3],[Module[1,I[0]],Y1,yp3]])
        L.append([[X1,x,x7,xp3],[Y1,y,y7,yp3]])
        L.append([[x,X2,xp2,x7],[y,Y2,yp2,y7]])
        L.append([[Module[0,I[1]],xp2,X2],[Module[1,I[1]],yp2,Y2]])
        L.append([[Module[0,I[2]],x6,xp2,Module[0,I[1]]],[Module[1,I[2]],y6,yp2,Module[1,I[1]]]])
        L.append([[x6,Module[0,I[3]],x7,xp2],[y6,Module[1,I[3]],y7,yp2]])
        L.append([[Module[0,I[3]],x8,xp3,x7],[Module[1,I[3]],y8,yp3,y7]])
        L.append([[Module[0,I[4]],Module[0,I[0]],xp3,x8],[Module[1,I[4]],Module[1,I[0]],yp3,y8]])
    if type == antiorientation:
        X1,Y1 = ((Module[0,I[0]]+x)/2,(Module[1,I[0]]+y)/2)
        X2,Y2 = ((Module[0,I[1]]+x)/2,(Module[1,I[1]]+y)/2)
        x4, y4 = ((x+Module[0,I[2]])/2,(y+Module[1,I[2]])/2)
        xp1,yp1 = ((x+Module[0,I[3]])/2,(y+Module[1,I[3]])/2)
        x3,y3 = ((Module[0,I[4]]+x)/2,(Module[1,I[4]]+y)/2)
        x1,y1 = ((Module[0,I[2]]+Module[0,I[3]])/2,(Module[1,I[2]]+Module[1,I[3]])/2)
        x2,y2 = ((Module[0,I[3]]+Module[0,I[4]])/2,(Module[1,I[3]]+Module[1,I[4]])/2)
        L.append([[Module[0,I[0]],X1,x3,Module[0,I[4]]],[Module[1,I[0]],Y1,y3,Module[1,I[4]]]])
        L.append([[X1,x,x3],[Y1,y,y3]])
        L.append([[x,X2,x4],[y,Y2,y4]])
        L.append([[Module[0,I[1]],Module[0,I[2]],x4,X2],[Module[1,I[1]],Module[1,I[2]],y4,Y2]])
        L.append([[Module[0,I[2]],x1,xp1,x4],[Module[1,I[2]],y1,yp1,y4]])
        L.append([[x1,Module[0,I[3]],x2,xp1],[y1,Module[1,I[3]],y2,yp1]])
        L.append([[xp1,x3,x,x4],[yp1,y3,y,y4]])
        L.append([[Module[0,I[4]],x3,xp1,x2],[Module[1,I[4]],y3,yp1,y2]])
    return L



################################################################################################################################
#Record STCs


os.chdir("../Ressources")
STCLD3447 = STCLayersLD(G,34,47)
STCHD2733 = STCLayersHD(G,27,33)
np.save('STCHD.npy',STCHD2733)
np.save('STCLD.npy',STCLD3447)
os.chdir("../../ProgrammesRessources")
np.save('STCHD.npy',STCHD2733)
np.save('STCLD.npy',STCLD3447)



