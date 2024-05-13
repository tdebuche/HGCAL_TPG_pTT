import numpy as np
import matplotlib.pyplot as plt
import os

from functions import etaphitoXY
from functions import etaphiRADtoXY
from functions import XYtoetaphi
from functions import polygontopoints
from functions import pointtopolygon
from functions import binetaphitoXY
from functions import binetaphiRADtoXY
from functions import etaphicentre
from functions import ModulestoSommets
from functions import BintoBinSommets
from functions import STCtoSTCSommets


os.chdir("../Ressources")
Z = np.load("Z.npy")
G = np.load('Geometry.npy')
UV = np.load('uv.npy')
Binetaphi = np.load('Binetaphi.npy')
STCLD = np.load('STCLD.npy')
STCHD = np.load('STCHD.npy')



#Layer to draw
Layer = 40


zlay = Z[Layer-1]
Modules = G[Layer-1]
BinXY= binetaphitoXY(Binetaphi,zlay)
Sommets = ModulestoSommets(Modules)
BinSommets = BintoBinSommets(BinXY)
uv = UV[Layer-1]


min_numberingmod = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 146, 198, 0, 52, 72, 95, 72, 95]

min_numberingscint = [132, 109, 136, 109, 104, 122, 110, 132, 118, 250, 114, 114, 95, 95]

IndminScint = [95,95,95,95,72,72,52,52,52,52,37,37,37,37]

plt.figure(figsize = (12,8))


#Modules
for i in range(len(Sommets)):
    plt.plot(Sommets[i][0] + [Sommets[i][0][0]],Sommets[i][1]+ [Sommets[i][1][0]], color = 'black')
    eta,phi = etaphicentre(Modules[i],zlay)
    x,y = etaphitoXY(eta,phi,zlay)
    plt.annotate(str(i),(x - 60,y -10),size =  '8')
print(str(i))
#Bins
for i in range(len(BinXY)):
   plt.plot(BinSommets[i][0] + [BinSommets[i][0][0]],BinSommets[i][1]+ [BinSommets[i][1][0]], color = 'red',linewidth = '0.5')

#UV
for i in range(len(Sommets)):
    eta,phi = etaphicentre(Modules[i],zlay)
    x,y = etaphitoXY(eta,phi,zlay)
    #plt.annotate('(' + str(uv[i][0]) +','+str(uv[i][1])+')',(x - 60,y -10),size =  '8')


#Numbering
for i in range(len(Sommets)):
    eta,phi = etaphicentre(Modules[i],zlay)
    x,y = etaphitoXY(eta,phi,zlay)
    if Layer > 33:
        if i < IndminScint[Layer-34]:
            N = min_numberingmod[Layer-14]
            #plt.annotate(str(N + i),(x - 60,y -10),size =  '8')
        else:
            N = min_numberingscint[Layer -34]
            #plt.annotate(str(N + i - IndminScint[Layer-34]),(x - 60,y -10),size =  '8')
    else :
        N = min_numberingmod[Layer//2]
        #plt.annotate(str(N+i),(x - 60,y -10),size =  '8')


plt.title(label =  'pTT of layer '+str(Layer))
plt.xlabel('x (mm)')
plt.ylabel('y (mm)')
plt.show()

"""
#marker phi
for i in range(24):
    x = (BinXY[i *20][0][0] + BinXY[i *20][0][3])/2
    y = (BinXY[i *20][1][0] + BinXY[i *20][1][3])/2
    if i > 14:
        x = x-20
        y = y +20
    if i > 16:
        x = x-20
        y = y +20
    if i > 19:
        x = x-20
    plt.annotate('phi='+str(i),(x,y),size =  '8')

#marker eta
for i in range(20):
    x = (BinXY[460+i][0][2] + BinXY[460+i][0][3])/2-150
    y = (BinXY[460+i][1][3] + BinXY[460+i][1][3])/2 -100
    plt.annotate('eta='+str(i),(x,y),size =  '8')"""

"""
os.chdir("../Ressources")
plt.savefig('pTT of layer '+str(Layer)+'.png')"""

#record  all layers

os.chdir("../Ressources")
"""
for k in range(0,34):
    if k <13:
        Layer = 2 *k+1
    else :
        Layer = k + 14
    zlay = Z[Layer-1]
    Modules = G[Layer-1]
    BinXY= binetaphitoXY(Binetaphi,zlay)
    Sommets = ModulestoSommets(Modules)
    BinSommets = BintoBinSommets(BinXY)
    uv = UV[Layer-1]
    if Layer >33:
        STC = STCLD[Layer-34]
        STCSommets = STCtoSTCSommets(STCLD[Layer-34])
    if Layer <34 and Layer > 26:
        STC = STCHD[Layer-27]
        STCSommets = STCtoSTCSommets(STCHD[Layer-27])
    plt.figure(figsize = (12,8))
    plt.title(label =  'pTT of layer '+str(Layer))
    plt.xlabel('x (mm)')
    plt.ylabel('y (mm)')
    for i in range(len(Sommets)):
        plt.plot(Sommets[i][0] + [Sommets[i][0][0]],Sommets[i][1]+ [Sommets[i][1][0]], color = 'black')
        eta,phi = etaphicentre(Modules[i],zlay)
        x,y = etaphitoXY(eta,phi,zlay)
        if Layer > 33:
            if i < IndminScint[Layer-34]:
                N = min_numberingmod[Layer-14]
                #plt.annotate(str(N + i),(x - 60,y -10),size =  '8')
            else:
                N = min_numberingscint[Layer -34]
                #plt.annotate(str(N + i - IndminScint[Layer-34]),(x - 60,y -10),size =  '8')
        else :
            N = min_numberingmod[Layer//2]
            #plt.annotate(str(N+i),(x - 60,y -10),size =  '8')
        #plt.annotate('(' + str(uv[i][0]) +','+str(uv[i][1])+')',(x - 60,y -10),size =  '8')
    #for i in range(len(BinXY)):
        #plt.plot(BinSommets[i][0] + [BinSommets[i][0][0]],BinSommets[i][1]+ [BinSommets[i][1][0]], color = 'red',linewidth = '0.5')
    if Layer > 26:
        for i in range(len(STC)):
            for j in range(len(STC[i])):
                if i < len(STCSommets):
                    if j< len(STCSommets[i]):
                        stc = STCSommets[i][j]
                        plt.plot(stc[0]+[stc[0][0]],stc[1]+[stc[1][0]],linewidth = 0.2,color  = 'blue') #STC
    plt.savefig('Modules of layer '+str(Layer)+'.png')"""
