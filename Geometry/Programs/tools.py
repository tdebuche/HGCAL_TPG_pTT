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


def etaphitoXY(eta,phi,z):
    x = z * np.tan(2*np.arctan(np.exp(-eta))) * np.cos(phi)
    y = z * np.tan(2*np.arctan(np.exp(-eta))) * np.sin(phi)
    return(x,y)




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




