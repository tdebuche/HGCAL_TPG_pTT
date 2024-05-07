import numpy as np
import matplotlib.pyplot as plt
import os

#données
etamin = 1.305
etamax = etamin + np.pi *20/36

phimin = 0
phimax = 120

nb_binphi = 24
nb_bineta = 20

############### BUILD THE VERTICES OF EACH BIN, THE FORMAT IS  array (480,2,4), [phi0,eta0....eta19,phi2,eta0....] ###############

def positions(emin,nbeta,nbphi): #sommets des bins, array (480,2,4), [phi0,eta0....eta19,phi2,eta0....]
    L = np.zeros((480,2,4))
    phirun = 0
    etarun = 0
    poly = 0
    for i in range(nbphi):
        for j in range(nbeta):
            L[poly] = np.array([[j * np.pi/36 + emin,(j+1) * np.pi/36 + emin,(j+1) * np.pi/36 + emin,j * np.pi/36 + emin],[i * np.pi/36,i * np.pi/36,(i+1) * np.pi/36,(i+1) * np.pi/36]])
            poly+=1
    return(L)


def bineta(emin,nbeta):
    return(np.array([etatorad(j * np.pi/36 + emin) for j in range(nbeta+1)]))

def binphi(nphi):
    return(np.array([i * np.pi/36 for i in range(nphi +1)]))


def etatorad(eta):
    return(2*np.arctan(np.exp(-eta)))

def radtodegré(rad):
    return(rad/np.pi * 180)


#fichier à enregistrer
BIN = positions(etamin,nb_bineta,nb_binphi)
os.chdir("C:/Users/Thomas de L'Epinois/Desktop/StageCMS/Mapping/pTT/Ressources")
np.save('Binetaphi',BIN)

plt.show()