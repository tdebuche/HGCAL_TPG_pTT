import numpy as np
import matplotlib.pyplot as plt
import os
from shapely.geometry import Polygon
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
from STCtoPTT import pTTSTCs
from ModuleSumtoPTT import pTTModules
from PTT import PTTarray

os.chdir("../../Ressources")

UV = np.load('uv.npy')
Binetaphi = np.load('Binetaphi.npy')
G = np.load('Geometry.npy')
Z = np.load('Z.npy')
STCLD = np.load('STCLD.npy')
STCHD = np.load('STCHD.npy')
etamin = 1.305
N = 16



nb_modules=[96,96,96,96,102,102,102,102,102,102,104,104,108,110,114,114,118,122,136,146,95,95,95,95,72,72,52,52,52,52,37,37,37,37]

min_numberingmod = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 146, 198, 0, 52, 72, 95, 72, 95]

min_numberingscint = [132, 109, 136, 109, 104, 122, 110, 132, 118, 250, 114, 114, 95, 95]

IndminScint = [95,95,95,95,72,72,52,52,52,52,37,37,37,37]


Boards = [['0x64000000', 3, 34], ['0x64010000', 1, 36, 47], ['0x64020000', 33, 40, 41], ['0x64030000', 9, 39, 44], ['0x64040000', 7, 42, 43], ['0x64050000', 13, 38, 46], ['0x64060000', 17, 27], ['0x64070000', 25, 31], ['0x64080000', 23, 30], ['0x64090000', 15, 32], ['0x640A0000', 19, 29], ['0x640B0000', 21, 28], ['0x640C0000', 5, 35], ['0x640D0000', 11, 37, 45]]
Boards_scintillators = [['0x64000000', 47], ['0x64010000',41], ['0x64020000',43], ['0x64030000', 37], ['0x64040000', 38], ['0x64050000', 35], ['0x64060000', 40], ['0x64070000', 39], ['0x64080000',42], ['0x64090000', 36], ['0x640A0000', 44], ['0x640B0000',45], ['0x640C0000', 46], ['0x640D0000', 34]]

##########################################        Write the text for Split    #######################################


def PTTmodulestoTextnoSTC(Geometry,Board):
    Layers = Boards[Board]
    Layers_Scint = Boards_scintillators[Board][1]

    pTTCEE,pTTCEH = PTTarraytoPTTboardnoSTC(Geometry,Board)
    nb_moduleCEE,nb_moduleCEH = nombreSiModules(Geometry,Board)
    nb_scint = nombreScintillators(Geometry,Board)

    tCEE = ''
    tCEH = ''
    intmatrixE = 0
    intmatrixH = 0
    adderE = 0
    adderH = 0
    maxE = 0
    maxH = 0
    for i in range(24):
        for j in range(20):
            resE,intmatrixE,adderE,nbmodintowerE = OnepTTCEEnoSTC(pTTCEE,i,j,intmatrixE,adderE)
            if nbmodintowerE > maxE:
                maxE = nbmodintowerE
            resH,intmatrixH,adderH,nbmodintowerH = OnepTTCEHnoSTC(pTTCEH,i,j,intmatrixH,adderH,Layers_Scint)
            if nbmodintowerH > maxH:
                maxH = nbmodintowerH
            tCEE += resE + '\n'
            tCEH += resH + '\n'
    tCEE = '//* total number of input in adders '+str(int(adderE))+' */' + '\n' + '\n' +tCEE
    tCEE = '//* max inputs per outputs = '+str(int(maxE))+' */'+ '\n' +tCEE
    tCEE = '/* num outputs = 480(out0-out479) */' + '\n' +tCEE
    tCEE = '/* num inputs = ' +str(int(nb_moduleCEE))+ '(in0-in' + str(int(nb_moduleCEE-1)) + ') */' + '\n' + tCEE
    tCEE = 'parameter integer matrixE [0:'+str(int(intmatrixE))+'] = {' + '\n' + tCEE
    tCEE += '};'

    tCEH = '//* total number of input in adders '+str(int(adderH))+' */' + '\n' + '\n' +tCEH
    tCEH = '//* max inputs per outputs = '+str(int(maxH))+' */'+ '\n' +tCEH
    tCEH = '/* num outputs = 480(out0-out479) */' + '\n' +tCEH
    tCEH = '/* num inputs = ' +str(int(nb_moduleCEH+nb_scint))+ '(in0-in' + str(int(nb_moduleCEH+nb_scint-1)) + ') */' + '\n' + tCEH
    tCEH = 'parameter integer matrixH [0:'+str(int(intmatrixH))+'] = {' + '\n' + tCEH
    tCEH += '};'

    return (tCEE,tCEH)


def PTTarraytoPTTboardnoSTC(Geometry,Board):
    Layers = Boards[Board]
    Layers_Scint = Boards_scintillators[Board][1]
    pTTCEE = [[[]for j in range(20)]for i in range(24)]
    pTTCEH = [[[]for j in range(20)]for i in range(24)]

    for i in range(1,len(Layers)):
        Layer = Layers[i]
        if Layer < 27:
            pTTlay = PTTarray(Layer,False)
            for i in range(24):
                for j in range(20):
                    pTTCEE[i][j].append([Layer,pTTlay[i,j]])
        if Layer > 26:
            pTTlay = PTTarray(Layer,False)
            for i in range(24):
                for j in range(20):
                    mods = []
                    for k in range(len(pTTlay[i,j])):
                        if not np.array_equal(pTTlay[i,j,k],np.zeros(4)):
                            indice = pTTlay[i,j,k,0]
                            if Layer > 33:
                                if indice < IndminScint[Layer-34] :
                                    mods.append(pTTlay[i,j,k])
                            else :
                                mods.append(pTTlay[i,j,k])
                    if mods != []:
                        pTTCEH[i][j].append([Layer,mods])

    Layer = Layers_Scint
    pTTscint = PTTarray(Layer,False)
    for i in range(24):
        for j in range(20):
            sc = []
            for k in range(len(pTTscint[i,j])):
                if not np.array_equal(pTTscint[i,j,k],np.zeros(4)):
                    indice = pTTscint[i,j,k,0]
                    if indice >= IndminScint[Layer-34] :
                        sc.append(pTTscint[i,j,k])
            if sc != []:
                pTTCEH[i][j].append([Layer,sc])

    return(pTTCEE,pTTCEH)

def OnepTTCEEnoSTC(pTTCEE,i,j,intmatrixE,adderE):
    res = ''
    nbmodintower = 0
    intmatrixE +=1    #pour le nbmodintower
    for lay in range(len(pTTCEE[i][j])):
        Layer = pTTCEE[i][j][lay][0]
        for k  in range(len(pTTCEE[i][j][lay][1])):
            if not np.array_equal(pTTCEE[i][j][lay][1][k],np.zeros(4)):
                nbmodintower += 1
                mod = pTTCEE[i][j][lay][1][k]
                res +=  str(int(mod[0]))+', '+str(int(mod[3]))+', '
                intmatrixE += 2
    if i*20+j<10:
        nbzeros= '000'
    if i*20+j>9 and i*20+j<100:
        nbzeros='00'
    if i*20+j>=100:
        nbzeros= '0'
    res ='/* out'+nbzeros+str(int(i*20+j))+'_em-eta'+str(j)+'-phi'+str(i)+'*/'+'\t'+str(int(nbmodintower))+', ' +res
    adderE += nbmodintower
    return(res,intmatrixE,adderE,nbmodintower)


def OnepTTCEHnoSTC(pTTCEH,i,j,intmatrixH,adderH,Layers_Scint):
    res = ''
    intmatrixH +=1 #pour le nbmodintower
    nbmodintower = 0
    for lay in range(len(pTTCEH[i][j])):
        Layer = pTTCEH[i][j][lay][0]
        for k  in range(len(pTTCEH[i][j][lay][1])):
            if not np.array_equal(pTTCEH[i][j][lay][1][k],np.zeros(4)):
                mod = pTTCEH[i][j][lay][1][k]
                if Layer == Layers_Scint and mod[0] >= IndminScint[Layer-34]:
                    nbl = min_numberingscint[Layer - 34]
                    nbmodintower += 1
                    res +=str(int(nbl+mod[0]-IndminScint[Layer-34]))+', '+str(int(mod[3]))+', '
                    intmatrixH += 2
                if Layer <34:
                    nbl = min_numberingmod[Layer - 14]
                    res += str(int(nbl+mod[0]))+', '+str(int(mod[3]))+', '
                    intmatrixH += 2
                    nbmodintower += 1
                if  Layer >33 and Layer != Layers_Scint and mod[0] < IndminScint[Layer-34]:
                    nbl = min_numberingmod[Layer - 14]
                    res += str(int(nbl+mod[0]))+', '+str(int(mod[3]))+', '
                    intmatrixH += 2
                    nbmodintower += 1
    if i*20+j<10:
        nbzeros= '000'
    if i*20+j>9 and i*20+j<100:
        nbzeros='00'
    if i*20+j>=100:
        nbzeros= '0'
    res ='/* out'+nbzeros+str(int(i*20+j))+'_had-eta'+str(j)+'-phi'+str(i)+'*/'+'\t'+str(int(nbmodintower))+', ' + res
    adderH += nbmodintower
    return(res,intmatrixH,adderH,nbmodintower)


def nombreSiModules(Geometry,Board):
    Layers = Boards[Board]
    nb_moduleCEE = 0
    nb_moduleCEH = 0
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
                        if k < IndminScint[Layer-34]:
                            nb_moduleCEH +=1
                    if Layer < 34:
                        nb_moduleCEH += 1

    return(nb_moduleCEE,nb_moduleCEH)


def nombreScintillators(Geometry,Board):
    Layers_Scint = Boards_scintillators[Board][1]
    nb_scint = 0
    Layer = Layers_Scint
    Modules = Geometry[Layer-1]
    for i in range(len(Modules)):
        M = Modules[i]
        a = 0
        for j in range(len(M[0])):
            if M[0,j] !=0 or M[1,j] != 0:
                a +=1
        if a >0:
            if i >= IndminScint[Layer-34]:
                nb_scint += 1
    return(nb_scint)

#########################################################          WITH STCs        ###############################################


def PTTmodulestoTextwithSTC(Geometry,Board):
    Layers = Boards[Board]
    Layers_Scint = Boards_scintillators[Board][1]

    pTTCEE,pTTCEH = PTTarraytoPTTboardwithSTC(Geometry,Board)
    nb_moduleCEE,nb_moduleCEH = nombreSiModules(Geometry,Board)
    nb_scint = nombreScintillators(Geometry,Board)

    tCEE = ''
    tCEH = ''
    intmatrixE = 0
    intmatrixH = 0
    adderE = 0
    adderH = 0
    maxE = 0
    maxH = 0
    for i in range(24):
        for j in range(20):
            resE,intmatrixE,adderE,nbmodintowerE = OnepTTCEEwithSTC(pTTCEE,i,j,intmatrixE,adderE)
            if nbmodintowerE > maxE:
                maxE = nbmodintowerE
            resH,intmatrixH,adderH,nbmodintowerH = OnepTTCEHwithSTC(pTTCEH,i,j,intmatrixH,adderH,Layers_Scint)
            if nbmodintowerH > maxH:
                maxH = nbmodintowerH
            tCEE += resE + '\n'
            tCEH += resH + '\n'
    tCEE = '//* total number of input in adders '+str(int(adderE))+' */' + '\n' + '\n' +tCEE
    tCEE = '//* max inputs per outputs = '+str(int(maxE))+' */'+ '\n' +tCEE
    tCEE = '/* num outputs = 480(out0-out479) */' + '\n' +tCEE
    tCEE = '/* num inputs = ' +str(int(nb_moduleCEE))+ '(in0-in' + str(int(nb_moduleCEE-1)) + ') */' + '\n' + tCEE
    tCEE = 'parameter integer matrixE [0:'+str(int(intmatrixE))+'] = {' + '\n' + tCEE
    tCEE += '};'

    tCEH = '//* total number of input in adders '+str(int(adderH))+' */' + '\n' + '\n' +tCEH
    tCEH = '//* max inputs per outputs = '+str(int(maxH))+' */'+ '\n' +tCEH
    tCEH = '/* num outputs = 480(out0-out479) */' + '\n' +tCEH
    tCEH = '/* num inputs = ' +str(int(nb_moduleCEH+nb_scint))+ '(in0-in' + str(int(nb_moduleCEH+nb_scint-1)) + ') */' + '\n' + tCEH
    tCEH = 'parameter integer matrixH [0:'+str(int(intmatrixH))+'] = {' + '\n' + tCEH
    tCEH += '};'

    return (tCEE,tCEH)

def PTTarraytoPTTboardwithSTC(Geometry,Board):
    Layers = Boards[Board]
    Layers_Scint = Boards_scintillators[Board][1]
    pTTCEE = [[[]for j in range(20)]for i in range(24)]
    pTTCEH = [[[]for j in range(20)]for i in range(24)]

    for i in range(1,len(Layers)):
        Layer = Layers[i]
        if Layer < 27:
            pTTlay = PTTarray(Layer,True)
            for i in range(24):
                for j in range(20):
                    pTTCEE[i][j].append([Layer,pTTlay[i,j]])
        if Layer > 26:
            pTTlay = PTTarray(Layer,True)
            for i in range(24):
                for j in range(20):
                    stc = []
                    for k in range(len(pTTlay[i,j])):
                        if not np.array_equal(pTTlay[i,j,k],np.zeros(5)):
                            indice = pTTlay[i,j,k,0]
                            if Layer > 33:
                                if indice < IndminScint[Layer-34] :
                                    stc.append(pTTlay[i,j,k])
                            else :
                                stc.append(pTTlay[i,j,k])
                    if stc != []:
                        pTTCEH[i][j].append([Layer,stc])

    Layer = Layers_Scint
    pTTscint = PTTarray(Layer,True)
    for i in range(24):
        for j in range(20):
            sc = []
            for k in range(len(pTTscint[i,j])):
                if not np.array_equal(pTTscint[i,j,k],np.zeros(4)):
                    indice = pTTscint[i,j,k,0]
                    if indice >= IndminScint[Layer-34] :
                        sc.append(pTTscint[i,j,k])
            if sc != []:
                pTTCEH[i][j].append([Layer,sc])

    return(pTTCEE,pTTCEH)

def OnepTTCEEwithSTC(pTTCEE,i,j,intmatrixE,adderE):
    res = ''
    nbmodintower = 0
    intmatrixE +=1    #pour le nbmodintower
    for lay in range(len(pTTCEE[i][j])):
        Layer = pTTCEE[i][j][lay][0]
        for k  in range(len(pTTCEE[i][j][lay][1])):
            if not np.array_equal(pTTCEE[i][j][lay][1][k],np.zeros(4)):
                nbmodintower += 1
                mod = pTTCEE[i][j][lay][1][k]
                res +=  str(int(mod[0]))+', '+str(int(mod[3]))+', '
                intmatrixE += 2
    if i*20+j<10:
        nbzeros= '000'
    if i*20+j>9 and i*20+j<100:
        nbzeros='00'
    if i*20+j>=100:
        nbzeros= '0'
    res ='/* out'+nbzeros+str(int(i*20+j))+'_em-eta'+str(j)+'-phi'+str(i)+'*/'+'\t'+str(int(nbmodintower))+', ' +res
    adderE += nbmodintower
    return(res,intmatrixE,adderE,nbmodintower)


def OnepTTCEHwithSTC(pTTCEH,i,j,intmatrixH,adderH,Layers_Scint):
    res = ''
    intmatrixH +=1 #pour le nbmodintower
    nbmodintower = 0
    for lay in range(len(pTTCEH[i][j])):
        Layer = pTTCEH[i][j][lay][0]
        for k  in range(len(pTTCEH[i][j][lay][1])):
            #if not np.array_equal(pTTCEH[i][j][lay][1][k],np.zeros(4)):  #Useless ??
            mod = pTTCEH[i][j][lay][1][k]
            if Layer == Layers_Scint and mod[0] >= IndminScint[Layer-34]:
                nbl = min_numberingscint[Layer - 34]
                nbmodintower += 1
                res +=str(int(nbl+mod[0]-IndminScint[Layer-34]))+ ', ' + str(int(mod[3]))+', '+str(int(mod[4]))+', '
                intmatrixH += 3
            if Layer <34:
                nbl = min_numberingmod[Layer - 14]
                res += str(int(nbl+mod[0]))+', '+ str(int(mod[3]))+', '+str(int(mod[4]))+', '
                intmatrixH += 3
                nbmodintower += 1
            if  Layer >33 and Layer != Layers_Scint and mod[0] < IndminScint[Layer-34]:
                nbl = min_numberingmod[Layer - 14]
                res += str(int(nbl+mod[0]))+', '+ str(int(mod[3]))+', '+str(int(mod[4]))+', '
                intmatrixH += 3
                nbmodintower += 1
    if i*20+j<10:
        nbzeros= '000'
    if i*20+j>9 and i*20+j<100:
        nbzeros='00'
    if i*20+j>=100:
        nbzeros= '0'
    res ='/* out'+nbzeros+str(int(i*20+j))+'_had-eta'+str(j)+'-phi'+str(i)+'*/'+'\t'+str(int(nbmodintower))+', ' + res
    adderH += nbmodintower
    return(res,intmatrixH,adderH,nbmodintower)





"""
def PTTmodulestoTextwithSTC(Geometry,Board):
    Layers = Boards[Board]
    Layers_Scint = Boards_scintillators[Board][1]
    pTTCEE = [[[]for j in range(20)]for i in range(24)]
    pTTCEH = [[[]for j in range(20)]for i in range(24)]
    nb_moduleCEE = 0
    nb_moduleCEH = 0
    nb_scint = 0
    nb_stc = 0
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
            for i in range(24):
                for j in range(20):
                    pTTCEE[i][j].append([Layer,pTTlay[i,j]])
        if Layer > 26:
            for i in range(24):
                for j in range(20):
                    pTTCEH[i][j].append([Layer,pTTlay[i,j]])


    for i in range(1,len(Layers)):
        Layer = Layers[i]
        if Layer > 26:
            if Layer < 34:
                STC = STCHD[Layer-27]
            else:
                STC = STCLD[Layer-34]
            for j in range(len(STC)):
                if j < IndminScint[Layer-34]
                for k in range(len(STC[j])):
                    stc = STC[j,k]
                    a = 0
                    for j in range(len(stc[0])):
                        if stc[0,j] !=0 or stc[1,j] != 0:
                            a +=1
                    if a>0:
                        nb_stc +=1


    Layer = Layers_Scint
    Modules = Geometry[Layer-1]
    for i in range(len(Modules)):
        M = Modules[i]
        a = 0
        for j in range(len(M[0])):
            if M[0,j] !=0 or M[1,j] != 0:
                a +=1
        if a >0:
            if i >= IndminScint[Layer-34]:
                nb_scint += 1
    pTTscint = PTTarray(Layer)
    for i in range(24):
        for j in range(20):
            sc = []
            for k in range(len(pTTscint[i,j])):
                if not np.array_equal(pTTscint[i,j,k],np.zeros(5)):
                    indice = pTTscint[i,j,k,0]
                    if indice >= IndminScint[Layer-34] :
                        sc.append(pTTscint[i,j,k])
            pTTCEH[i][j].append([Layer,sc])


    Layer = Layers_Scint
    if Layer > 26:
        if Layer < 34:
            STC = STCHD[Layer-27]
        else:
            STC = STCLD[Layer-34]
        for j in range(len(STC)):
            for k in range(len(STC[j])):
                stc = STC[j,k]
                a = 0
                for j in range(len(stc[0])):
                    if stc[0,j] !=0 or stc[1,j] != 0:
                        a +=1
                if a>0:
                    nb_stc +=1 ################################################################################################

    tCEE = ''
    tCEH = ''
    intmatrixE = 0
    intmatrixH = 0
    adderE = 0
    adderH = 0
    maxE = 0
    maxH = 0
    for i in range(24):
        for j in range(20):
            nbmodintower = 0
            for lay in range(len(pTTCEE[i][j])):
                for k  in range(len(pTTCEE[i][j][lay][1])):
                    if not np.array_equal(pTTCEE[i][j][lay][1][k],np.zeros(4)):
                        nbmodintower += 1
                    if nbmodintower > maxE:
                        maxE = nbmodintower
            if i*20+j<10:
                nbzeros= '000'
            if i*20+j>9 and i*20+j<100:
                nbzeros='00'
            if i*20+j>100:
                nbzeros= '0'
            tCEE+='/* out'+nbzeros+str(int(i*20+j))+'_em-eta'+str(j)+'-phi'+str(i)+'*/'+'\t'+str(int(nbmodintower))+', '
            intmatrixE +=1
            adderE += nbmodintower
            for lay in range(len(pTTCEE[i][j])):
                for k  in range(len(pTTCEE[i][j][lay][1])):
                    Layer = pTTCEE[i][j][lay][0]
                    if not np.array_equal(pTTCEE[i][j][lay][1][k],np.zeros(4)):
                        mod = pTTCEE[i][j][lay][1][k]
                        tCEE +=  str(int(mod[0]))+', '+str(int(mod[3]))+', '
                        intmatrixE += 2
            tCEE+= '\n'
    for i in range(24):
        for j in range(20):
            nbmodintower = 0
            for lay in range(len(pTTCEH[i][j])):
                Layer = pTTCEH[i][j][lay][0]
                for k  in range(len(pTTCEH[i][j][lay][1])):
                    if not np.array_equal(pTTCEH[i][j][lay][1][k],np.zeros(5)): #with STCs
                        mod = pTTCEH[i][j][lay][1][k]
                        if Layer  == Layers_Scint and mod[0] >= IndminScint[Layer-34]:
                            nbmodintower += 1
                        if Layer  != Layers_Scint and mod[0] < IndminScint[Layer-34]:
                            nbmodintower += 1
                    if nbmodintower > maxH:
                        maxH = nbmodintower
            intmatrixH +=1
            adderH += nbmodintower
            if i*20+j<10:
                nbzeros= '000'
            if i*20+j>9 and i*20+j<100:
                nbzeros='00'
            if i*20+j>100:
                nbzeros= '0'
            tCEH+='/* out'+nbzeros+str(int(i*20+j))+'_had-eta'+str(j)+'-phi'+str(i)+'*/'+'\t'+str(int(nbmodintower))+', '
            for lay in range(len(pTTCEH[i][j])):
                Layer = pTTCEH[i][j][lay][0]
                for k  in range(len(pTTCEH[i][j][lay][1])):
                    if not np.array_equal(pTTCEH[i][j][lay][1][k],np.zeros(5)): #with STCs
                        mod = pTTCEH[i][j][lay][1][k]
                        if Layer  == Layers_Scint and mod[0] >= IndminScint[Layer-34]:
                            tCEH += str(int(nbl+mod[0]-IndminScint[Layer-34]))+', '+ str(int(mod[3]))+', '+str(int(mod[4]))+', '#with STCs
                            intmatrixH += 3 #with STCs
                        if Layer  != Layers_Scint and mod[0] < IndminScint[Layer-34]:
                            nbl = nb_mod_beforelayer[Layer - 14]
                            tCEH += str(int(nbl+mod[0]))+', '+ str(int(mod[3]))+', '+str(int(mod[4]))+', ' #with STCs
                            intmatrixH += 3 #with STCs
            tCEH += '\n'
    tCEE = '//* total number of input in adders '+str(int(adderE))+' */' + '\n' + '\n' +tCEE
    tCEE = '//* max inputs per outputs = '+str(int(maxE))+' */'+ '\n' +tCEE
    tCEE = '/* num outputs = 480(out0-out479) */' + '\n' +tCEE
    tCEE = '/* num inputs = ' +str(int(nb_moduleCEE))+ '(in0-in' + str(int(nb_moduleCEE-1)) + ') */' + '\n' + tCEE
    tCEE = 'parameter integer matrixE [0:'+str(int(intmatrixE))+'] = {' + '\n' + tCEE

    tCEH = '//* total number of input in adders '+str(int(adderH))+' */' + '\n' + '\n' +tCEH
    tCEH = '//* max inputs per outputs = '+str(int(maxH))+' */'+ '\n' +tCEH
    tCEH = '/* num outputs = 480(out0-out479) */' + '\n' +tCEH
    tCEH = '/* num inputs = ' +str(int(nb_stc+nb_scint))+ '(in0-in' + str(int(nb_stc+nb_scint-1)) + ') */' + '\n' + tCEH #with STCs
    tCEH = 'parameter integer matrixH [0:'+str(int(intmatrixH))+'] = {' + '\n' + tCEH
    tCEE += '};'
    tCEH += '};'
    return (tCEE,tCEH)"""


##################################################################################################################################

# to test
"""
Board = 0
os.chdir("../../Ressources")
textCEE,textCEH = PTTmodulestoTextwithSTC(G,Board)
name = "PTTs_Board"+  str(Board)
file = open(name+"CEE"+".txt", "w")
file.write(textCEE)
file.close()
name += "withSTCs"
file = open(name+"CEH"+".txt", "w")
file.write(textCEH)
file.close()"""

# Record with STCs
"""
for Board in range(14):
    os.chdir("../../Ressources")
    textCEE,textCEH = PTTmodulestoTextwithSTC(G,Board)
    name = 'CE_E_'+  str(Board)+ '_v1'
    file = open(name+".vh", "w")
    file.write(textCEE)
    file.close()
    name = 'CE_H_'+  str(Board)+ '_v1'
    file = open(name+".vh", "w")
    file.write(textCEH)
    file.close()"""


# Record without STCs
"""
for Board in range(14):
    os.chdir("../../Ressources")
    textCEE,textCEH = PTTmodulestoTextnoSTC(G,Board)
    name = 'CE_E_'+  str(Board)+ '_v1'
    file = open(name+".vh", "w")
    file.write(textCEE)
    file.close()
    name = 'CE_H_'+  str(Board)+ '_v1'
    file = open(name+".vh", "w")
    file.write(textCEH)
    file.close()
"""
