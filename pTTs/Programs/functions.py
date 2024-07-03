import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import json
from collections import defaultdict


def import_bins(args,Layer):
	if args.Edges == 'yes':
		path = 'src/2028_Bins.json'
	if args.Edges == 'no':
		path = 'src/2024_Bins.json'
	with open(path,'r') as file:
		Bins = json.load(file)['Bins'][Layer-1]
	with open(path,'r') as file:
		header = json.load(file)['header']
	list_vertices = defaultdict(list)
	for bin_idx in range(len(Bins)):
		X_Vertices,Y_Vertices = Bins[bin_idx]['verticesX'],Bins[bin_idx]['verticesY']
		eta,phi = Bins[bin_idx]['eta_index'],Bins[bin_idx]['phi_index']
		list_vertices[(eta,phi)].append([X_Vertices,Y_Vertices])
	return list_vertices,header
  
def import_header(args):
	if args.Edges == 'yes':
		path = 'src/2028_Bins.json'
	if args.Edges == 'no':
		path = 'src/2024_Bins.json'
	with open(path,'r') as file:
		header = json.load(file)['header']
	return header


def pointtopolygon(vertices):
    points = []
    for i in range(len(vertices[0])):
        if vertices[0][i]!= 0 or vertices[1][i] != 0:
            points.append((vertices[0][i],vertices[1][i]))
    return(Polygon(points))


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



