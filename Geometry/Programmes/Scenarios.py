import numpy as np
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir('dir_path/../../ProgrammesRessources')


#First scenario : 20 * 24 bins, 0 to 120 degrees

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
