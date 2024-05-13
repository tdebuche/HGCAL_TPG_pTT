import numpy as np
import matplotlib.pyplot as plt
import os
from prelim import etaphitoXY
from prelim import etaphiRADtoXY
from prelim import XYtoetaphi
from prelim import polygontopoints
from prelim import pointtopolygon
from prelim import binetaphitoXY
from prelim import binetaphiRADtoXY
from prelim import etaphicentre
from prelim import ModulestoSommets
from prelim import BintoBinSommets
from prelim import STCtoSTCSommets


os.chdir("C:/Users/Thomas de L'Epinois/Desktop/StageCMS/Mapping/pTT/Ressources")
Z = np.load("Z.npy")
G = np.load('Geometry.npy')
UV = np.load('uv.npy')
Binetaphi = np.load('Binetaphi.npy')
STCLD = np.load('STCLD.npy')
STCHD = np.load('STCHD.npy')

min_numberingmod = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 146, 198, 0, 52, 72, 95, 72, 95]

min_numberingscint = [132, 109, 136, 109, 104, 122, 110, 132, 118, 250, 114, 114, 95, 95]

IndminScint = [95,95,95,95,72,72,52,52,52,52,37,37,37,37]

Boards = [['0x64000000', 3, 34], ['0x64010000', 1, 36, 47], ['0x64020000', 33, 40, 41], ['0x64030000', 9, 39, 44], ['0x64040000', 7, 42, 43], ['0x64050000', 13, 38, 46], ['0x64060000', 17, 27], ['0x64070000', 25, 31], ['0x64080000', 23, 30], ['0x64090000', 15, 32], ['0x640A0000', 19, 29], ['0x640B0000', 21, 28], ['0x640C0000', 5, 35], ['0x640D0000', 11, 37, 45]]


Boards_scintillators = [['0x64000000', 47], ['0x64010000',41], ['0x64020000',43], ['0x64030000', 37], ['0x64040000', 38], ['0x64050000', 35], ['0x64060000', 40], ['0x64070000', 39], ['0x64080000',42], ['0x64090000', 36], ['0x640A0000', 44], ['0x640B0000',45], ['0x640C0000', 46], ['0x640D0000', 34]]


def input():
    tCEE = 'Input CEE pTT Stage 1' + '\n\n'
    tCEH = 'Input CEH pTT Stage 1'   '\n\n'
    for board in range(len(Boards)):
        Board = Boards[board]
        tCEE += '\t' + 'Board = ' + Board[0] +'\n'
        tCEH += '\t' + 'Board = ' + Board[0] +'\n'
        for lay in range(1,len(Board)):
            Layer = Board[lay]
            Modules =  G[Layer-1]
            uv = UV[Layer -1]
            if Layer <27:
                for i in range(len(Modules)):
                    if not np.array_equal(Modules[i],np.zeros((2,6))):
                        tCEE +='\t\t Board_' + str(board) + ', Channel_' + str(i)
                        tCEE += ' =  Layer_'+str(Layer)+', ('+str(uv[i][0])+', '+str(uv[i][1])+') ' + 'Si Module \n'
            else:
                if Layer >33:
                    N = min_numberingmod[Layer-14]
                    for i in range(len(Modules)):
                        if i <IndminScint[Layer-34]:
                            if not np.array_equal(Modules[i],np.zeros((2,6))):
                                tCEH +='\t\t Board_' + str(board) + ', Channel_' + str(i+N)
                                tCEH += ' =  Layer_'+str(Layer)+', ('+str(uv[i][0])+', '+str(uv[i][1])+') ' + 'Si Module \n'
                if Layer < 34:
                    N = min_numberingmod[Layer-14]
                    for i in range(len(Modules)):
                        if not np.array_equal(Modules[i],np.zeros((2,6))):
                            tCEH +='\t\t Board_' + str(board) + ', Channel_' + str(i+N)
                            tCEH += ' =  Layer_'+str(Layer)+', ('+str(uv[i][0])+', '+str(uv[i][1])+') ' + 'Si Module \n'

        Layer = Boards_scintillators[board][1]
        Modules =  G[Layer-1]
        uv = UV[Layer -1]
        N = min_numberingscint[Layer-34]
        for i in range(len(Modules)):
            if i >= IndminScint[Layer-34]:
                if not np.array_equal(Modules[i],np.zeros((2,6))):
                    tCEH +='\t\t Board_' + str(board) + ', Channel_' + str(i+N-IndminScint[Layer-34])
                    tCEH += ' =  Layer_'+str(Layer)+', ('+str(uv[i][0])+', '+str(uv[i][1])+') ' + 'Scintillator \n'

    return tCEE,tCEH


os.chdir("C:/Users/Thomas de L'Epinois/Desktop/StageCMS/Mapping/pTT/Ressources/Info_Boards")
textCEE,textCEH = input()
file = open('Input_CEE_pTT.txt', "w")
file.write(textCEE)
file.close()
file = open('Input_CEH_pTT.txt', "w")
file.write(textCEH)
file.close()