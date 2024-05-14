import numpy as np
import matplotlib.pyplot as plt
import os
from functions  import etaphitoXY
from functions  import etaphiRADtoXY
from functions  import XYtoetaphi
from functions  import polygontopoints
from functions  import pointtopolygon
from functions  import binetaphitoXY
from functions  import binetaphiRADtoXY
from functions  import etaphicentre
from functions import ModulestoVertices
from functions import STCtoSTCVertices


os.chdir("../../ProgrammesRessources")
Z = np.load("Z.npy")
G = np.load('ModulesGeometry.npy')
UV = np.load('UVModules.npy')
STCLD = np.load('STCLD.npy')
STCHD = np.load('STCHD.npy')

min_numberingmod = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 146, 198, 0, 52, 72, 95, 72, 95]
min_numberingscint = [132, 109, 136, 109, 104, 122, 110, 132, 118, 250, 114, 114, 95, 95]
IndminScint = [95,95,95,95,72,72,52,52,52,52,37,37,37,37]
Boards = [['0x64000000', 3, 34], ['0x64010000', 1, 36, 47], ['0x64020000', 33, 40, 41], ['0x64030000', 9, 39, 44], ['0x64040000', 7, 42, 43], ['0x64050000', 13, 38, 46], ['0x64060000', 17, 27], ['0x64070000', 25, 31], ['0x64080000', 23, 30], ['0x64090000', 15, 32], ['0x640A0000', 19, 29], ['0x640B0000', 21, 28], ['0x640C0000', 5, 35], ['0x640D0000', 11, 37, 45]]
Boards_scintillators = [['0x64000000', 47], ['0x64010000',41], ['0x64020000',43], ['0x64030000', 37], ['0x64040000', 38], ['0x64050000', 35], ['0x64060000', 40], ['0x64070000', 39], ['0x64080000',42], ['0x64090000', 36], ['0x640A0000', 44], ['0x640B0000',45], ['0x640C0000', 46], ['0x640D0000', 34]]

#Board to record
Board = 13

os.chdir("../Input_S1/Ressources")
plt.figure(figsize = (34,16))  #need to adjust the size of the picture

#Look at the SI modules layers
res = 0
multiple = 1
for lay in range(1,len(Boards[Board])):
    Layer = Boards[Board][lay]
    zlay = Z[Layer-1]
    Modules = G[Layer-1]
    ModuleVertices = ModulestoVertices(Modules)
    uv = UV[Layer-1]
    if Layer < 27:
        plt.annotate('LayerCEE '+str(Layer),(80+res,1650))
    else :
        plt.annotate('LayerCEH '+str(Layer),(80+res,1650))
    for i in range(len(ModuleVertices)):
        eta,phi = etaphicentre(Modules[i],zlay)
        x,y = etaphitoXY(eta,phi,zlay)
        if Layer > 33:
            if i < IndminScint[Layer-34]:
                N = min_numberingmod[Layer-14]
                plt.annotate(str(N + i),((x - 60)*multiple  + res ,(y -10)*multiple) ,size =  '8')
                plt.plot( np.array((ModuleVertices[i][0] + [ModuleVertices[i][0][0]])) *multiple + res,np.array(ModuleVertices[i][1]+ [ModuleVertices[i][1][0]]) *multiple , color = 'black')
                plt.plot(np.array((ModuleVertices[i][0] + [ModuleVertices[i][0][0]])) *multiple  + res,np.array(ModuleVertices[i][1]+ [ModuleVertices[i][1][0]])*multiple -2500, color = 'black')
                plt.annotate('(' + str(uv[i][0]) +','+str(uv[i][1])+')',((x - 60)*multiple  + res ,(y -10)*multiple  -2500),size =  '7')
        else :
            if Layer >26:
                N = min_numberingmod[Layer-14]
            if Layer < 26:
                N = min_numberingmod[Layer//2]
            plt.annotate(str(N+i),((x - 60)*multiple  + res,(y -10)*multiple) ,size =  '8')
            plt.plot( np.array((ModuleVertices[i][0] + [ModuleVertices[i][0][0]])) *multiple + res,np.array(ModuleVertices[i][1]+ [ModuleVertices[i][1][0]]) *multiple , color = 'black')
            plt.plot(np.array((ModuleVertices[i][0] + [ModuleVertices[i][0][0]])) *multiple  + res,np.array(ModuleVertices[i][1]+ [ModuleVertices[i][1][0]])*multiple -2500, color = 'black')
            plt.annotate('(' + str(uv[i][0]) +','+str(uv[i][1])+')',((x - 60)*multiple  + res ,(y -10)*multiple  -2500),size =  '7')

    res +=2500
    multiple = multiple-0.2

#Look at the scintillator layers

Layer = Boards_scintillators[Board][1]
zlay = Z[Layer-1]
Modules = G[Layer-1]
ModuleVertices = ModulestoVertices(Modules)
uv = UV[Layer-1]
plt.annotate('LayerCEH '+str(Layer),(80+res,1650))
for i in range(len(ModuleVertices)):
    eta,phi = etaphicentre(Modules[i],zlay)
    x,y = etaphitoXY(eta,phi,zlay)
    if i >= IndminScint[Layer-34]:
        plt.plot(np.array((ModuleVertices[i][0] + [ModuleVertices[i][0][0]]))*multiple   + res,np.array(ModuleVertices[i][1]+ [ModuleVertices[i][1][0]])*multiple , color = 'black')
        plt.plot(np.array((ModuleVertices[i][0] + [ModuleVertices[i][0][0]]))*multiple  + res,np.array(ModuleVertices[i][1]+ [ModuleVertices[i][1][0]])*multiple -2500, color = 'black')
        N = min_numberingscint[Layer -34]
        plt.annotate(str(N + i - IndminScint[Layer-34]),((x - 60)*multiple  +res,(y -10)*multiple) ,size =  '8')
        plt.annotate('(' + str(uv[i][0]) +','+str(uv[i][1])+')',((x - 60)*multiple  + res ,(y -10)*multiple -2500),size =  '7')

plt.xticks([])
plt.yticks([])
plt.title('Input of Boards '+str(Board))
plt.show()


plt.savefig('Input of Boards '+str(Board)+'.png')
