import numpy as np
import matplotlib.pyplot as plt
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
#Entries
etamin = 1.305

#Create an array with the vertices of each bin. Bins are sorted by phi,eta

def Bins(etamin,phimin,nbeta,nbphi): 
    L = np.zeros((nbeta*nbphi,2,4))
    bin = 0
    for i in range(nbphi):
        for j in range(nbeta):
            L[bin] = np.array([[j * np.pi/36 + etamin,(j+1) * np.pi/36 + etamin,(j+1) * np.pi/36 + etamin,j * np.pi/36 + etamin],[i * np.pi/36  + phimin,i * np.pi/36 + phimin,(i+1) * np.pi/36 + phimin,(i+1) * np.pi/36 + phimin]])
            bin+=1
    return(L)



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
