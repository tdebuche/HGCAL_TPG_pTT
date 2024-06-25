import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import json

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


def reorganize_vertices(vertices,irot):
  #find the vertex 0
  y_min = vertices[1][0]
  idx_min = 0
  for vertex_idx in range(len(vertices[1])):
    if vertices[1][vertex_idx] < y_min :
      y_min = vertices[1][vertex_idx]
      idx_min = vertex_idx
  vertices[0] = [vertices[0][(vertex_idx+idx_min)%len(vertices[0])] for vertex_idx in range(len(vertices[0]))]
  vertices[1] = [vertices[1][(vertex_idx+idx_min)%len(vertices[0])]for vertex_idx in range(len(vertices[0]))]
  
  #rotate
  vertices[0] = [vertices[0][(vertex_idx+irot)%len(vertices[0])]for vertex_idx in range(len(vertices[0]))]
  vertices[1] = [vertices[1][(vertex_idx+irot)%len(vertices[0])]for vertex_idx in range(len(vertices[0]))]
  
  return vertices

####################### Few function used for the conversion XY/EtaPhi  #########

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
    if np.abs(y) < 0.00001:
        if np.sign(x)<0:
            phi = 0
        else :
            phi = np.pi
        return((-np.log(np.tan(0.5*np.arctan(np.abs(x)/(z * np.abs(np.cos(phi))))))),phi)
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




