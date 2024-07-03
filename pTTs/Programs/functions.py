import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import json

####################### Few functions used for the  XY/EtaPhi conversion  #########


def item_list(jsonfile,item):
  L = []
  res = []
  with open(jsonfile,'r') as file:
    alldata = json.load(file)
  for layer in range(47):
    data = alldata[layer-1]
    for module_idx in range(len(data)):
      if item =="id":
        res.append(data[module_idx]['id'])
      if item =="irot":
        res.append(data[module_idx]['irot'])
      if item =="TCcount":
        res.append(data[module_idx]['TCcount'])
      if item =="index":
        res.append(data[module_idx]['index'])
      if item =="uv":
        res.append([data[module_idx]['u'],data[module_idx]['v']])
      if item =="vertices":
        res.append([data[module_idx]['verticesX'],data[module_idx]['verticesY']])
    L.append(res)
    res = []
  return L


def pointtopolygon(vertices):
    points = []
    for i in range(len(vertices[0])):
        if vertices[0][i]!= 0 or vertices[1][i] != 0:
            points.append((vertices[0][i],vertices[1][i]))
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


def etaphicentre(Module,z):
    nbsommet = 0
    x = 0
    y = 0
    for i in range(len(Module[0])):
        if Module[0][i] != 0 or Module[1][i] !=0:
            nbsommet +=1
            x += Module[0][i]
            y += Module[1][i]
    return(XYtoetaphi(x/nbsommet,y/nbsommet,z))



