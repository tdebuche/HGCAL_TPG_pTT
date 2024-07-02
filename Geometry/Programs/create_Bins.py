import numpy as np
from Geometry.Programs.tools import *

with open('src/Z_coordinates.json','r') as file:
    Z_Layers = json.load(file)
    
#record two scenarios : 20*24 bins and 20*28 bins

etamin = 1.305
bin_size = "pi/36"

#First scenario : 20 * 24 bins, 0 to 120 degree

nb_binphi = 24
nb_bineta = 20

etamin = 1.305
etamax = etamin + np.pi *20/36

phimin = 0 * np.pi/180
phimax = 120 * np.pi/180

np.save('ValuesBins2024',np.array([nb_binphi,nb_bineta,phimin,phimax,etamin,etamax]))

#Second scenario: 20 * 28 bins, -15 to 125 degrees

nb_binphi = 28
nb_bineta = 20

etamin = 1.305
etamax = etamin + np.pi *20/36

phimin = -15 * np.pi/180
phimax = 125 * np.pi/180

np.save('ValuesBins2028',np.array([nb_binphi,nb_bineta,phimin,phimax,etamin,etamax]))


def Bins(etamin,phimin,nbeta,nbphi): 
    all_layers_Bins = []
    for layer in range(1,48):
        single_layer_Bins = []
        bin_idx = 0 
        z = Z_Layers[layer-1]['Z_coordinate']
        for phi in range(nbphi):
            for eta in range(nbeta):
                Eta_vertices,Phi_vertices = [eta * np.pi/36 + etamin,(eta+1) * np.pi/36 + etamin,(eta+1) * np.pi/36 + etamin,eta * np.pi/36 + etamin],[phi * np.pi/36  + phimin,phi * np.pi/36 + phimin,(phi+1) * np.pi/36 + phimin,(phi+1) * np.pi/36 + phimin]
                for vertex_idx in range(len(Eta_vertices)):
                    x,y = etaphitoXY(Eta_vertices[vertex_idx],Phi_vertices[vertex_idx],z)
                    verticesX.append(x)
                    verticesY.append(y)
                single_layer_Bins.append({'index' : bin_idx, 'eta_index' : eta, 'phi_index' : phi_index,'verticesX' : verticesX,'verticesY' : verticesY, 'Eta_vertices' : Eta_vertices,'Phi_vertices' : Phi_vertices,})
        all_layers_Bins.append(single_layer_Bins)
    return(all_layers_Bins)



#record the files


#without edges
phimin = 0
phimax = 120
nb_binphi = 24
nb_bineta = 20

BIN = Bins(etamin,phimin,nb_bineta,nb_binphi)
os.chdir(dir_path+"../Ressources")
np.save('Binetaphi'+str(nb_bineta)+str(nb_binphi),BIN)
os.chdir(dir_path+"../../ProgrammesRessources")
np.save('Binetaphi'+str(nb_bineta)+str(nb_binphi),BIN)

#with edges

phimin = -15 * np.pi/180
phimax = 125 * np.pi/18
nb_binphi = 28
nb_bineta = 20

BIN = Bins(etamin,phimin,nb_bineta,nb_binphi)
os.chdir(dir_path + "../Geometry/Ressources")
np.save('Binetaphi'+str(nb_bineta)+str(nb_binphi),BIN)
os.chdir(dir_path+"../../ProgrammesRessources")
np.save('Binetaphi'+str(nb_bineta)+str(nb_binphi),BIN)
