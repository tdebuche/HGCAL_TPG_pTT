import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon


####################### Few functions used for the conversion XY/EtaPhi and the building of list and array for plots #########


def item_list(jsonfile,item,layer):
  L = []
  with open(jsonfile,'r') as file:
    data = json.load(file)[layer-1]
  for module_idx in range(len(data)):
    if item =="id":
      L.append(data[module_idx]['id'])
    if item =="irot":
      L.append(data[module_idx]['irot'])
    if item =="TCcount":
      L.append(data[module_idx]['TCcount'])
    if item =="uv":
      L.append([data[module_idx]['u'],data[module_idx]['v']])
    if item =="vertices":
      L.append([data[module_idx]['verticesX'],data[module_idx]['verticesY']])
  return L


def pointtopolygon(L):
    points = []
    for i in range(len(L[0])):
        if L[0][i]!= 0 or L[1][i] != 0:
            points.append((L[0][i],L[1][i]))
    return(Polygon(points))

def polygontopoints(poly):
    p = poly.exterior.coords.xy
    L = [[],[]]
    for i in range(len(p[0])):
        L[0].append(p[0][i])
        L[1].append(p[1][i])
    return(L)

def XYtoetaphi(x,y,z):
    if x == 0:
        if np.sign(y)<0:
            phi = 3*np.pi/2
        else:
            phi = np.pi/2
        return((-np.log(np.tan(0.5*np.arctan(y/(z * np.sin(phi)))))),phi)
    elif x >0:
        phi = np.arctan(y/x)
        return((-np.log(np.tan(0.5*np.arctan(x/(z * np.cos(phi)))))),phi)
    elif x < 0 :
        phi = np.arctan(np.abs(x)/y) + np.pi/2
        return((-np.log(np.tan(0.5*np.arctan(x/(z * np.cos(phi)))))),phi)


def etaphitoXY(eta,phi,z):
    x = z * np.tan(2*np.arctan(np.exp(-eta))) * np.cos(phi)
    y = z * np.tan(2*np.arctan(np.exp(-eta))) * np.sin(phi)
    return(x,y)

def etaphiRADtoXY(eta,phi,z):
    x = z * np.tan(eta) * np.cos(phi)
    y = z * np.tan(eta) * np.sin(phi)
    return(x,y)


def binetaphitoXY(B,z):
    XY = np.zeros(np.shape(B))
    for i in range(len(B)):
        for j in range(4):
            eta = B[i,0,j]
            phi = B[i,1,j]
            x,y = etaphitoXY(eta,phi,z)
            XY[i,0,j] = x
            XY[i,1,j] = y
    return XY


def binetaphiRADtoXY(B,z):
    XY = np.zeros(np.shape(B))
    for i in range(len(B)):
        for j in range(4):
            eta = B[i,0,j]
            phi = B[i,1,j]
            x,y = etaphiRADtoXY(eta,phi,z)
            XY[i,0,j] = x
            XY[i,1,j] = y
    return XY



def etaphicentre(Module,z):
    nbsommet = 0
    x = 0
    y = 0
    for i in range(len(Module[0])):
        if Module[0,i] != 0 or Module[1,i] !=0:
            nbsommet +=1
            x += Module[0,i]
            y += Module[1,i]
    return(XYtoetaphi(x/nbsommet,y/nbsommet,z))


def ModulestoVertices(M):
    L =[]
    l1 = []
    l2 = []
    for i in range(len(M)):
        j = 0
        while j != 6 and (M[i,0,j] != 0 or M[i,1,j] != 0 )  :
            l1.append(M[i,0,j])
            l2.append(M[i,1,j])
            j = j+1

        if l1 != []:
            L.append([l1,l2])
        l1 = []
        l2 = []
    return(L)

def BintoBinBVertices(M):
    L =[]
    l1 = []
    l2 = []
    for i in range(len(M)):
        j = 0
        while j != 4 and (M[i,0,j] != 0 or M[i,1,j] != 0 )  :
            l1.append(M[i,0,j])
            l2.append(M[i,1,j])
            j = j+1

        if l1 != []:
            L.append([l1,l2])
        l1 = []
        l2 = []
    return(L)

def STCtoSTCVertices(M):
    L =[]
    lmod =[]
    l1 = []
    l2 = []
    for i in range(len(M)):
        for j in range(len(M[i])):
            k = 0
            while k != 5 and (M[i,j,0,k] != 0 or M[i,j,1,k] != 0 )  :
                l1.append(M[i,j,0,k])
                l2.append(M[i,j,1,k])
                k = k+1

            if l1 != []:
                lmod.append([l1,l2])
            l1 = []
            l2 = []
        L.append(lmod)
        lmod = []
    return(L)

