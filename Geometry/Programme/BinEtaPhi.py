import numpy as np
import matplotlib.pyplot as plt
import os

#Entries
etamin = 1.305
etamax = etamin + np.pi *20/36

phimin = 0
phimax = 120

nb_binphi = 24
nb_bineta = 20

#Build an array with the vertices of each bin. Bins are sorted by phi,eta
def Bins(emin,nbeta,nbphi): 
    L = np.zeros((480,2,4))
    phirun = 0
    etarun = 0
    poly = 0
    for i in range(nbphi):
        for j in range(nbeta):
            L[poly] = np.array([[j * np.pi/36 + emin,(j+1) * np.pi/36 + emin,(j+1) * np.pi/36 + emin,j * np.pi/36 + emin],[i * np.pi/36,i * np.pi/36,(i+1) * np.pi/36,(i+1) * np.pi/36]])
            poly+=1
    return(L)



#record the file
BIN = Bins(etamin,nb_bineta,nb_binphi)
os.chdir("../Ressources")
np.save('Binetaphi',BIN)

plt.show()
