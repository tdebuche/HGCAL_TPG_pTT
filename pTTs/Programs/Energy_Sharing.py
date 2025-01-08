import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import pTTs.Programs.tools as tools
import json

#import z coordinates
with open('src/Z_coordinates.json','r') as file:
	Z_Layers = json.load(file)

N = 16 #energies divided by N (for the sharing)


#create a list for the energy mapping of a singla layer
def reverse_pTTs(args,Layer,Modules,STCs):
	#the Bin list gathers the pTT coordinates, the header list allows to know the number of pTTs (20*24 or 20*28)
	Bins,header = tools.import_bins(args,Layer)
	if Layer < 27 or (Layer>=27 and not args.STCs):
		#compute the module energy sharing for a sector of a single layer
		pTTs = pTT_single_layer(args,Layer,Modules,Bins,header)
	else :
		#compute the STC energy sharing for a sector of a single layer
		pTTs = pTT_single_layer(args,Layer,STCs,Bins,header)
		
	nb_binphi,nb_bineta = header['nb_phibin'],header['nb_etabin']
	nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
	#creation of the list with the energy sharing
	reversed_pTTs = [[[] for j in range(nb_bineta)] for i in range(nb_binphi)]                  
	for module_idx in range(len(pTTs)):
		Module = pTTs[module_idx][0]
		for bin_idx in range(len(pTTs[module_idx][1])):
			phi,eta,ratio = pTTs[module_idx][1][bin_idx]
			if args.STCs and Layer >26 :
				reversed_pTTs[phi][eta].append([Module['type'],Module['u'],Module['v'],Module['index'],ratio])
			if Layer < 27 or (Layer>=27 and not args.STCs) :
				reversed_pTTs[phi][eta].append([Module['type'],Module['u'],Module['v'],ratio])
	return(reversed_pTTs)


#compute the energy sharing of a single layer
def pTT_single_layer(args,Layer,Modules,Bins,header): 
    Modules = Modules[Layer-1]
    #create a list with the enegy sharing
    Bins_per_Modules = []
    for module_idx in range(len(Modules)):
        Module_vertices = [Modules[module_idx]['verticesX'],Modules[module_idx]['verticesY']]
	#compute the area ratio (for the energy sharing) of the overlapping pTTs and the ratio of energy per pTT
        single_module_Bins = areatocoef(pTT_single_Module(Layer,Bins,Module_vertices,header))
        Bins_per_Modules.append([Modules[module_idx],single_module_Bins])
    return(Bins_per_Modules)



#compute the overlapping area of a module by the pTTs 
def pTT_single_Module(Layer,Bins,Module,header): 
	nb_binphi,nb_bineta = header['nb_phibin'],header['nb_etabin']
	phimin,etamin =  header['phimin'],header['etamin']
	nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
	pTTs = []
	Module_Polygon = tools.pointtopolygon(Module)
	area_module = Module_Polygon.area
	eta,phi = tools.etaphicentre(Module,Z_Layers[Layer-1]["Z_coordinate"])
	phi_center = int((phi-phimin) *36 /np.pi)
	eta_center = int((eta -etamin) *36 /np.pi)

	#look at the pTT defined by eta-phi coordinates close to the one of the module center (no need to compute the energy sharing with pTTs which dont overlap)
	for phi in range(-4,5):
		for eta in range(-4,5):
			phi_idx = phi_center + phi
			eta_idx = eta_center + eta
			if phi_idx >= 0 and phi_idx < nb_binphi: #if the pTT is in the right 120° sector 
				if eta_idx >= 0 and eta_idx < nb_bineta:
					#compute the overlapping area
					Area = AireBinModule(Module,Bins[(eta_idx,phi_idx)][0])
					if Area !=0:
						pTTs.append([phi_idx,eta_idx,Area/area_module])
	return(pTTs)


# Return [area(intersection module and bin)] for a given module and a given bin
def AireBinModule(Module,Bin): 
    Module = tools.pointtopolygon(Module)
    Bin = tools.pointtopolygon(Bin)
    if Module.intersects(Bin):
        return(Module.intersection(Bin).area)
    else :
        return(0)


# Convert overlap area into fraction of N (N = 16 for now)
def areatocoef(Areas): 
    L =[]
    reste = []
    coef = 0
    total = 0
    sum = 0
    if Areas == []:
        return([])
    for i in range(len(Areas)):
        coef = int(N *Areas[i][2])
        L.append([Areas[i][0],Areas[i][1],coef])
        total += coef
        reste.append((Areas[i][2] - coef/N))
        sum += coef
    x = 0
    indicex = 0
    while sum != N:
        x = 0
        for i in range(len(Areas)):
            if reste[i] > x:
                indicex = i
                x = reste[i]
        L[indicex][2] += 1
        reste[indicex] = reste[indicex] - 1/N
        sum +=1
    COEF = []
    for i in range(len(Areas)):
        if  L[i][2] != 0:
            COEF.append(L[i])
    return COEF


