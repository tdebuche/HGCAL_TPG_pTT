
import numpy as np
import matplotlib.pyplot as plt
import os
from shapely.geometry import Polygon
import functions
import argparse
from ModuleSumtoPTT import reverse_pTTs
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path + '/../../ProgrammesRessources')

with open('Modules.json','r') as file:
    Modules = json.load(file)
with open('STCs.json','r') as file:
    STCs = json.load(file)

Values2024 = np.load('ValuesBins2024.npy')
Values2028 = np.load('ValuesBins2028.npy')

Boards = [['0x64000000', 3, 34], ['0x64010000', 1, 36, 47], ['0x64020000', 33, 40, 41], ['0x64030000', 9, 39, 44], ['0x64040000', 7, 42, 43], ['0x64050000', 13, 38, 46], ['0x64060000', 17, 27], ['0x64070000', 25, 31], ['0x64080000', 23, 30], ['0x64090000', 15, 32], ['0x640A0000', 19, 29], ['0x640B0000', 21, 28], ['0x640C0000', 5, 35], ['0x640D0000', 11, 37, 45]]
Boards_scintillators = [['0x64000000', 47], ['0x64010000',41], ['0x64020000',43], ['0x64030000', 37], ['0x64040000', 38], ['0x64050000', 35], ['0x64060000', 40], ['0x64070000', 39], ['0x64080000',42], ['0x64090000', 36], ['0x640A0000', 44], ['0x640B0000',45], ['0x640C0000', 46], ['0x640D0000', 34]]
##########################################        Without STCs   #######################################


def files_single_board(args,Board,Modules,STCs):
    CEE_pTTs,CEH_pTTs = pTTs_single_board(args,Board_number,Modules,STCs)
    nb_CEE_inputs,nb_CEH_inputs = nb_inputs(args,Board_number)
    if args.Edges: Values = Values2028
    else : Values = Values2024
    nb_binphi,nb_bineta,phimin,phimax,etamin,etamax = Values
    nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
    text_CEE, text_CEH= '',''
    intmatrixE,intmatrixH = 0,0
    adderE,adderH = 0,0
    maxE,maxH = 0,0
    for phi in range(nb_binphi):
        for eta in range(nb_bineta):
            resE,intmatrixE,adderE,nbmodintowerE = single_pTT_text(CEE_pTTs,phi,eta,intmatrixE,adderE)
            if nbmodintowerE > maxE:
                maxE = nbmodintowerE
            resH,intmatrixH,adderH,nbmodintowerH = single_pTT_text(CEH_pTTs,phi,eta,intmatrixH,adderH)
            if nbmodintowerH > maxH:
                maxH = nbmodintowerH
            if (phi == nb_binphi-1) and (eta == nb_bineta-1): 
                resE = resE[0:-1]
                resH = resH[0:-1]
            text_CEE += resE + '\n'
            text_CEH += resH + '\n'
    text_CEE = '//* total number of input in adders '+str(int(adderE-1))+' */' + '\n' + '\n' + text_CEE
    text_CEE = '//* max inputs per outputs = '+str(int(maxE))+' */'+ '\n' + text_CEE
    text_CEE = '/* num outputs = '+str(int(nb_binphi*nb_bineta))+'(out0-out'+str(int(nb_binphi*nb_bineta-1))+') */' + '\n' + text_CEE
    text_CEE = '/* num inputs = ' +str(int(nb_CEE_inputs))+ '(in0-in' + str(int(nb_CEE_inputs-1)) + ') */' + '\n' + text_CEE
    text_CEE = 'parameter integer matrixE [0:'+str(int(intmatrixE))+'] = {' + '\n' + text_CEE
    text_CEE += '};'

    text_CEH = '//* total number of input in adders '+str(int(adderH-1))+' */' + '\n' + '\n' + text_CEH
    text_CEH = '//* max inputs per outputs = '+str(int(maxH))+' */'+ '\n' + text_CEH
    text_CEH = '/* num outputs = '+str(int(nb_binphi*nb_bineta))+'(out0-out'+str(int(nb_binphi*nb_bineta-1))+') */' + '\n' + text_CEH
    text_CEH = '/* num inputs = ' +str(int(nb_CEH_inputs))+ '(in0-in' + str(int(nb_CEH_inputs-1)) + ') */' + '\n' + text_CEH
    text_CEH = 'parameter integer matrixH [0:'+str(int(intmatrixH))+'] = {' + '\n' + text_CEH
    text_CEH += '};'

    return (text_CEE,text_CEH)


def pTTs_single_board(args,Board_number,Modules,STCs):
    if args.Edges: Values = Values2028
    else : Values = Values2024
    nb_binphi,nb_bineta,phimin,phimax,etamin,etamax = Values
    nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
    Layers = Boards[Board_number]
    Layers.append(Boards_scintillators[Board_number][1])
    CEE_pTTs,CEH_pTTs = [[[]for j in range(nb_bineta)]for i in range(nb_binphi)],[[[]for j in range(nb_bineta)]for i in range(nb_binphi)]

    for lay in range(1,len(Layers)):
        Layer = Layers[lay]
        pTTs_one_layer = reverse_pTTs(args,Layer,Modules,STCs)
        for phi in range(nb_binphi):
            for eta in range(nb_bineta):
                pTT = pTTs_one_layer[phi][eta]
                if Layer < 34 : 
                    CEE_pTTs[phi][eta].append([Layer,pTT])
                if Layer > 33:
                    Si_Modules = []
                    for module_idx in range(len(pTT)):
                        module_type = pTT[module_idx][0]
                        if module_type == 'silicon' and (lay!=len(Layers)) : Si_Modules.append(pTT[module_idx])
                        if module_type == 'scintillator' and (lay==len(Layers)-1) : Si_Modules.append(pTT[module_idx])
                    CEH_pTTs[phi][eta].append([Layer,Si_Modules])

    return(pTTCEE,pTTCEH)

def single_pTT_text(pTT,phi,eta,intmatrix,adder):
    res = ''
    nb_module_in_pTT = 0
    intmatrix +=1    #pour le nbmodintower
    pTT  = pTT[phi][eta]
    for lay in range(len(pTT)):
        Layer = pTT[lay][0]
        for module_idx in range(len(pTT[lay][1])):
            nb_module_in_pTT += 1
            module = pTT[lay][1][module_idx]
            module_u,module_v = str(module[1]),str(module[2])
            if module[0] == 'silicon': module_type = 'Si'
            if module[0] == 'scintillator': module_type = 'Sc'
            if args.Format == 'text':
                if Layer <27 or not args.STCs :
                    module_energy = str(module[3])
                    res +=  '('+ str(Layer) +','+module_type+',' +module_u+',' +module_v+'),'+ module_energy +','
                    intmatrix += 2
                 if Layer >26 and args.STCs :
                    stc_index = str(module[3])
                    stc_energy = str(module[4])
                    res +=  '('+ str(Layer) +','+module_type+',' +module_u+',' +module_v+','+stc_index+'),'+ module_energy +','
                    intmatrix += 3
            if args.Format == 'vh':
                if Layer <27 or not args.STCs :
                    module_energy = str(module[3])
                    module_channel = get_module_channel(Layer,module[0],module_u,module_v)
                    res +=  str(module_channel)+','+ module_energy +','
                    intmatrix += 2
                 if Layer >26 and args.STCs :
                    stc_index = str(module[3])
                    stc_energy = str(module[4])
                    STC_channel,STC_word = get_STC_channel(Layer,module[0],module_u,module_v,stc_index)
                    res +=  str(STC_channel)+','+str(STC_word)+','+ module_energy +','
                    intmatrix += 3
    res ='/* out'+nbzeros+str(int(i*20+j)).zfill(4)+'_em-eta'+str(j)+'-phi'+str(i)+'*/'+'\t'+str(int(nbmodintower))+', ' +res
    adder += nb_module_in_pTT
    return(res,intmatrix,adder,nb_module_in_pTT)


##################################################################################################################################
#Parameters:

parser = argparse.ArgumentParser()
parser.add_argument("Board", help="Layer to display",type=int)
parser.add_argument("--STCs",default = 'yes', help="With (yes) or without STCs (no)")
parser.add_argument("--Edges",default = 'no', help="With (yes) or without edges(no)")
parser.add_argument("--Record",default = 'no', help="Record all boards")
args = parser.parse_args()

# to test
os.chdir(dir_path+"/../Ressources/test")

Board = args.Board
if args.Edges == 'yes' and args.STCs == 'yes':
    textCEE,textCEH = PTTmodulestoTextwithSTC(G,Board,True)
    name ="PTTs_Board"+  str(Board) + 'Edges'+'STCs'
if args.Edges == 'no'and args.STCs == 'yes':
    name ="PTTs_Board"+  str(Board) + 'NoEdges'+'STCs'
    textCEE,textCEH = PTTmodulestoTextwithSTC(G,Board,False)
if args.Edges == 'yes' and args.STCs == 'no':
    name ="PTTs_Board"+  str(Board) + 'Edges'+'NoSTCs'
    textCEE,textCEH = PTTmodulestoTextnoSTC(G,Board,True)
if args.Edges == 'no'and args.STCs == 'no':
    name ="PTTs_Board"+  str(Board) + 'NoEdges'+'NoSTCs'
    textCEE,textCEH = PTTmodulestoTextnoSTC(G,Board,False)
    
file = open(name+"CEE"+".txt", "w")
file.write(textCEE)
file.close()
file = open(name+"CEH"+".txt", "w")
file.write(textCEH)
file.close()

# Record
if args.Record == 'yes':
    if args.Edges == 'yes' and args.STCs == 'yes':
        os.chdir(dir_path+"/../Ressources/Readable_files/28_Phi_Bins/with_STCs")
        for Board in range(14):
            textCEE,textCEH = PTTmodulestoTextwithSTC(G,Board,True)
            name = 'CE_E_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEE)
            file.close()
            name = 'CE_H_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEH)
            file.close()
    if args.Edges == 'yes' and args.STCs == 'no':
        os.chdir(dir_path+"/../Ressources/Readable_files/28_Phi_Bins/without_STCs")
        for Board in range(14):
            textCEE,textCEH = PTTmodulestoTextnoSTC(G,Board,True)
            name = 'CE_E_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEE)
            file.close()
            name = 'CE_H_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEH)
            file.close()
    if args.Edges == 'no' and args.STCs == 'yes':
        os.chdir(dir_path+"/../Ressources/Readable_files/24_Phi_Bins/with_STCs")
        for Board in range(14):
            textCEE,textCEH = PTTmodulestoTextwithSTC(G,Board,False)
            name = 'CE_E_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEE)
            file.close()
            name = 'CE_H_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEH)
            file.close()
    
    if args.Edges == 'no' and args.STCs == 'no':
        os.chdir(dir_path+"/../Ressources/Readable_files/24_Phi_Bins/without_STCs")
        for Board in range(14):
            textCEE,textCEH = PTTmodulestoTextnoSTC(G,Board,False)
            name = 'CE_E_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEE)
            file.close()
            name = 'CE_H_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEH)
            file.close()



if args.Edges == 'yes' and args.STCs == 'yes':
    os.chdir(dir_path+"/../Ressources/Readable_files")
    textCEE,textCEH ='',''
    print('ok')
    for Board in range(14):
        print(Board)
        res1,res2 = PTTmodulestoTextwithSTC(G,Board,True)
        textCEE += res1
        textCEH += res2
    name = 'CE_E_allBoards_Edges'
    file = open(name+".txt", "w")
    file.write(textCEE)
    file.close()
    name = 'CE_H_allBoards_Edges'
    file = open(name+".txt", "w")
    file.write(textCEH)
    file.close()

if args.Edges == 'no' and args.STCs == 'yes':
    os.chdir(dir_path+"/../Ressources/Readable_files")
    textCEE,textCEH ='',''        
    for Board in range(14):
        print(Board)
        res1,res2 = PTTmodulestoTextwithSTC(G,Board,False)
        textCEE += res1
        textCEH += res2
    name = 'CE_E_allBoards_NoEdges'
    file = open(name+".txt", "w")
    file.write(textCEE)
    file.close()
    name = 'CE_H_allBoards_NoEdges'
    file = open(name+".txt", "w")
    file.write(textCEH)
    file.close()


if args.Edges == 'yes' and args.STCs == 'no':
    os.chdir(dir_path+"/../Ressources/Readable_files")
    textCEE,textCEH ='',''
    print('ok')
    for Board in range(14):
        print(Board)
        res1,res2 = PTTmodulestoTextnoSTC(G,Board,True)
        textCEE += res1
        textCEH += res2
    name = 'CE_E_allBoards_EdgesNoSTCs'
    file = open(name+".txt", "w")
    file.write(textCEE)
    file.close()
    name = 'CE_H_allBoards_EdgesNoSTCs'
    file = open(name+".txt", "w")
    file.write(textCEH)
    file.close()

if args.Edges == 'no' and args.STCs == 'no':
    os.chdir(dir_path+"/../Ressources/Readable_files")
    textCEE,textCEH ='',''        
    for Board in range(14):
        print(Board)
        res1,res2 = PTTmodulestoTextnoSTC(G,Board,False)
        textCEE += res1
        textCEH += res2
    name = 'CE_E_allBoards_NoEdgesNoSTCs'
    file = open(name+".txt", "w")
    file.write(textCEE)
    file.close()
    name = 'CE_H_allBoards_NoEdgesNoSTCs'
    file = open(name+".txt", "w")
    file.write(textCEH)
    file.close()




