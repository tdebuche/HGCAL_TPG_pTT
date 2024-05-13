import numpy as np
import matplotlib.pyplot as plt
import os
from shapely.geometry import Polygon
from functions import etaphitoXY
from functions import etaphiRADtoXY
from functions import XYtoetaphi
from functions import polygontopoints
from functions import pointtopolygon
from functions import binetaphitoXY
from functions import binetaphiRADtoXY
from functions import etaphicentre
from functions import ModulestoVertices
from functions import BintoBinVertices
from functions import STCtoSTCVertices
from STCtoPTT import pTTSTCs
from ModuleSumtoPTT import pTTModules
from PTT import PTTarray

os.chdir("../../ProgrammesRessources")

UV = np.load('UVModules.npy')
Binetaphi = np.load('Binetaphi2024.npy')
#Binetaphi = np.load('Binetaphi2028.npy')
G = np.load('ModulesGeometry.npy')
Z = np.load('Z.npy')
STCLD = np.load('STCLD.npy')
STCHD = np.load('STCHD.npy')
etamin = 1.305
N = 16


Boards = [['0x64000000', 3, 34], ['0x64010000', 1, 36, 47], ['0x64020000', 33, 40, 41], ['0x64030000', 9, 39, 44], ['0x64040000', 7, 42, 43], ['0x64050000', 13, 38, 46], ['0x64060000', 17, 27], ['0x64070000', 25, 31], ['0x64080000', 23, 30], ['0x64090000', 15, 32], ['0x640A0000', 19, 29], ['0x640B0000', 21, 28], ['0x640C0000', 5, 35], ['0x640D0000', 11, 37, 45]]
Boards_scintillators = [['0x64000000', 47], ['0x64010000',41], ['0x64020000',43], ['0x64030000', 37], ['0x64040000', 38], ['0x64050000', 35], ['0x64060000', 40], ['0x64070000', 39], ['0x64080000',42], ['0x64090000', 36], ['0x640A0000', 44], ['0x640B0000',45], ['0x640C0000', 46], ['0x640D0000', 34]]
Layer_Scintillator = [95,95,95,95,72,72,52,52,52,52,37,37,37,37]

##########################################        Write the text for Split    #######################################
def PTTmodulestoText(Geometry,Board):
    Layers = Boards[Board]
    Layers_Scint = Boards_scintillators[Board][1]
    tCEE = 'Board id="' +Boards[Board][0]+ '",  Board number = ' + str(Board) +'\n' + 'CE-E' + '\n'
    tCEH = 'Board id="' +Boards[Board][0]+ '",  Board number = ' + str(Board) +'\n'+ 'CE-H' + '\n'
    tCEE += 'Layers = '
    tCEH += 'Layers = '
    pTTCEE = [[[]for j in range(20)]for i in range(24)]
    pTTCEH = [[[]for j in range(20)]for i in range(24)]
    nb_moduleCEE = 0
    nb_moduleCEH = 0
    nb_scint = 0
    for i in range(1,len(Layers)):
        Layer = Layers[i]
        Modules = Geometry[Layer-1]
        for k in range(len(Modules)):
            M = Modules[k]
            a = 0
            for j in range(len(M[0])):
                if M[0,j] !=0 or M[1,j] != 0:
                    a +=1
            if a >0:
                if Layer <27:
                    nb_moduleCEE +=1
                if Layer > 26:
                    if Layer >33:
                        if k < Layer_Scintillator[Layer-34]:
                            nb_moduleCEH +=1
                    if Layer < 34:
                        nb_moduleCEH += 1
        pTTlay = PTTarray(Layer)
        if Layer < 27:
            tCEE += str(Layer) +' region 0, '
            for i in range(24):
                for j in range(20):
                    pTTCEE[i][j].append([Layer,pTTlay[i,j]])
        if Layer > 26:
            tCEH += str(Layer) +' region 1, '
            for i in range(24):
                for j in range(20):
                    pTTCEH[i][j].append([Layer,pTTlay[i,j]])

    Layer = Layers_Scint
    Modules = Geometry[Layer-1]
    for i in range(len(Modules)):
        M = Modules[i]
        a = 0
        for j in range(len(M[0])):
            if M[0,j] !=0 or M[1,j] != 0:
                a +=1
        if a >0:
            if i >= Layer_Scintillator[Layer-34]:
                nb_scint += 1
    pTTscint = PTTarray(Layer)
    tCEH += str(Layer) +' region 2, '
    for i in range(24):
        for j in range(20):
            sc = []
            for k in range(len(pTTscint[i,j])):
                if not np.array_equal(pTTscint[i,j,k],np.zeros(5)):
                    indice = pTTscint[i,j,k,0]
                    if indice >= Layer_Scintillator[Layer-34] :
                        sc.append(pTTscint[i,j,k])
            pTTCEH[i][j].append([Layer,sc])

    tCEE += '\n' + 'nb_modules =  ' +str(nb_moduleCEE) +'\n'
    tCEH += '\n' + 'nb_Simodules =  ' +str(nb_moduleCEH) +'\n'
    tCEH +=  'nb_scintillators =  ' +str(nb_scint) +'\n'

    tCEH += ' Sillicon modules and scintillors treated as Modules, no STCs' + '\n' #without STCs
    #tCEH += 'Modules with STCs and scintillors wihout STCs ' + '\n'       #with STCs
    tCEE += 'Energies divided by ' + str(N)  + '\n'
    tCEH += 'Energies divided by ' + str(N)  + '\n'
    tCEE += 'nb_pTTs = ' + str(len(pTTCEE)*len(pTTCEE[0])) + '\n'
    tCEE += 'format Module -> (Layer,u_module,v_module)' + '\n'+ '\n'
    tCEH += 'nb_pTTs = ' + str(len(pTTCEH)*len(pTTCEH[0])) + '\n'
    #tCEH += 'format STC -> (Layer,u_module,v_module,index_STC)' + '\n'+ '\n' #with STCs
    tCEH += 'format Module -> (Layer,u_module,v_module)' + '\n'+ '\n' #without STCs
    for i in range(24):
        for j in range(20):
            nbmodintower = 0
            for lay in range(len(pTTCEE[i][j])):
                for k  in range(len(pTTCEE[i][j][lay][1])):
                    if not np.array_equal(pTTCEE[i][j][lay][1][k],np.zeros(4)):
                        nbmodintower += 1
            tCEE += 'eta' +str(j)+'phi'+str(i)+'\t\t\t'+  str(int(nbmodintower))+', '
            for lay in range(len(pTTCEE[i][j])):
                for k  in range(len(pTTCEE[i][j][lay][1])):
                    if not np.array_equal(pTTCEE[i][j][lay][1][k],np.zeros(4)):
                        mod = pTTCEE[i][j][lay][1][k]
                        tCEE +='(Si, '+str(pTTCEE[i][j][lay][0])+','+str(int(mod[1]))+','+str(int(mod[2]))+'), '+str(int(mod[3]))+', '
            tCEE+= '\n'
    for i in range(24):
        for j in range(20):
            nbmodintower = 0
            for lay in range(len(pTTCEH[i][j])):
                for k  in range(len(pTTCEH[i][j][lay][1])):
                    #if not np.array_equal(pTTCEH[i][j][lay][1][k],np.zeros(5)): #with STCs
                    if not np.array_equal(pTTCEH[i][j][lay][1][k],np.zeros(4)):  #without STCs
                        mod = pTTCEH[i][j][lay][1][k]
                        Layer = pTTCEH[i][j][lay][0]
                        if Layer  == Layers_Scint and mod[0] >= Layer_Scintillator[Layer-34]:
                            nbmodintower += 1
                        if Layer  != Layers_Scint and mod[0] < Layer_Scintillator[Layer-34]:
                            nbmodintower += 1
            tCEH += 'eta' +str(j)+'phi'+str(i)+'\t\t\t'+  str(int(nbmodintower))+', '
            for lay in range(len(pTTCEH[i][j])):
                for k  in range(len(pTTCEH[i][j][lay][1])):
                    #if not np.array_equal(pTTCEH[i][j][lay][1][k],np.zeros(5)): #with STCs
                    if not np.array_equal(pTTCEH[i][j][lay][1][k],np.zeros(4)): #without STCs
                        mod = pTTCEH[i][j][lay][1][k]
                        Layer = pTTCEH[i][j][lay][0]
                        if Layer  == Layers_Scint and mod[0] >= Layer_Scintillator[Layer-34]:
                            #tCEH +='(Scint, '+str(pTTCEH[i][j][lay][0])+','+str(int(mod[1]))+','+str(int(mod[2]))+', '+str(int(mod[3]))+'), '+str(int(mod[4]))+', ' #with STCs
                            tCEH +='(Scint, '+str(pTTCEH[i][j][lay][0])+','+str(int(mod[1]))+','+str(int(mod[2])) +'), '+str(int(mod[3]))+', '#without STCs
                        if Layer  != Layers_Scint and mod[0] < Layer_Scintillator[Layer-34]:
                            #tCEH +='(Si, '+str(pTTCEH[i][j][lay][0])+','+str(int(mod[1]))+','+str(int(mod[2]))+', '+str(int(mod[3]))+'), '+str(int(mod[4]))+', ' #with STCs
                            tCEH +='(Si, '+str(pTTCEH[i][j][lay][0])+','+str(int(mod[1]))+','+str(int(mod[2]))+'), '+str(int(mod[3]))+', ' #without STCs
            tCEH += '\n'

    return (tCEE,tCEH)


##################################################################################################################################
"""
Board = 1
os.chdir("../PTTs/Ressources")
textCEE,textCEH = PTTmodulestoText(G,Board)
name = "PTTs_Board"+  str(Board)
file = open(name+"CEE"+".txt", "w")
file.write(textCEE)
file.close()
name += "withSTCs"
file = open(name+"CEH"+".txt", "w")
file.write(textCEH)
file.close()"""

#with STCs
"""
for Board in range(14):
    os.chdir("../PTTs/Ressources/PTTswithSTCs")
    textCEE,textCEH = PTTmodulestoText(G,Board)
    name = "PTTs_Board"+  str(Board)
    file = open(name+"CEE"+".txt", "w")
    file.write(textCEE)
    file.close()
    name += "withSTCs"
    file = open(name+"CEH"+".txt", "w")
    file.write(textCEH)
    file.close()"""

#without STCs
"""
for Board in range(14):
    os.chdir("../PTTs/Ressources/PTTswithoutSTCs")
    textCEE,textCEH = PTTmodulestoText(G,Board)
    name = "PTTs_Board"+  str(Board)
    file = open(name+"CEE"+".txt", "w")
    file.write(textCEE)
    file.close()
    name += "withoutSTCs"
    file = open(name+"CEH"+".txt", "w")
    file.write(textCEH)
    file.close()"""
