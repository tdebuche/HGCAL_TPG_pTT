import numpy as np
import os
import argparse

from pTTs.Programmes.ModuleSumtoPTT import reverse_pTTs
import S1_Input.Programmes.create_numbering 

with open('ProgrammesRessources/Modules.json','r') as file:
    Modules = json.load(file)
with open('ProgrammesRessources/STCs.json','r') as file:
    STCs = json.load(file)
    
Values2024 = np.load('ValuesBins2024.npy')
Values2028 = np.load('ValuesBins2028.npy')
Boards = [['0x64000000', 3, 34], ['0x64010000', 1, 36, 47], ['0x64020000', 33, 40, 41], ['0x64030000', 9, 39, 44], ['0x64040000', 7, 42, 43], ['0x64050000', 13, 38, 46], ['0x64060000', 17, 27], ['0x64070000', 25, 31], ['0x64080000', 23, 30], ['0x64090000', 15, 32], ['0x640A0000', 19, 29], ['0x640B0000', 21, 28], ['0x640C0000', 5, 35], ['0x640D0000', 11, 37, 45]]
Boards_scintillators = [['0x64000000', 47], ['0x64010000',41], ['0x64020000',43], ['0x64030000', 37], ['0x64040000', 38], ['0x64050000', 35], ['0x64060000', 40], ['0x64070000', 39], ['0x64080000',42], ['0x64090000', 36], ['0x640A0000', 44], ['0x640B0000',45], ['0x640C0000', 46], ['0x640D0000', 34]]

#Parameters:

parser = argparse.ArgumentParser()
parser.add_argument("--Format",default = 'readable', help="textfile : readable, vhfile: vh")
parser.add_argument("--STCs",default = 'yes', help="With (yes) or without STCs (no)")
parser.add_argument("--Edges",default = 'no', help="With (yes) or without edges(no)")
args = parser.parse_args()


record_all_boards(args)

def record_all_boards(args):
    if args.Format == 'vh': path = "pTTs/Ressources/v2/VH_files"
    if args.Format == 'readable':path = "pTTs/Ressources/v2/Readable_files"
    if args.Edges == 'yes' : path += '/28_Phi_Bins'
    if args.Edges == 'no' : path += '/24_Phi_Bins'
    if args.STCs == 'yes' : path += '/with_STCs'
    if args.STCs == 'no' : path += '/without_STCs'
    os.chdir(path)
    all_boards_CEE,all_boards_CEH = '',''
    for Board in range(14):
        text_CEE,text_CEH = files_single_board(args,Board,Modules,STCs)
        all_boards_CEE += text_CEE
        all_boards_CEH += text_CEH
        name = 'CE_E_'+  str(Board)+ '_v2'
        if args.Format == 'vh': name += '.vh'
        if args.Format == 'readable': name += '.txt'
        file = open(name, "w")
        file.write(text_CEE)
        file.close()
        name = 'CE_H_'+  str(Board)+ '_v2'
        if args.Format == 'vh': name += '.vh'
        if args.Format == 'readable': name += '.txt'
        file = open(name, "w")
        file.write(text_CEH)
        file.close()
    name = CE_E_allBoards
    file = open(name+".txt", "w")
    file.write(all_boards_CEE)
    file.close()
    name = CE_H_allBoards
    file = open(name+".txt", "w")
    file.write(all_boards_CEH)
    file.close()

    
def files_single_board(args,Board,Modules,STCs):
    CEE_pTTs,CEH_pTTs = pTTs_single_board(args,Board_number,Modules,STCs)
    nb_CEE_inputs,nb_CEH_inputs = create_numbering.nb_inputs(args,Board_number)
    if args.Edges: Values = Values2028
    else : Values = Values2024
    nb_binphi,nb_bineta,phimin,phimax,etamin,etamax = Values
    nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
    text_CEE, text_CEH= '',''
    intmatrixE,intmatrixH = -1,-1
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
            if args.Format == 'readable':
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
                    module_channel = create_numbering.get_module_channel(Layer,module[0],module_u,module_v)
                    res +=  str(module_channel)+','+ module_energy +','
                    intmatrix += 2
                if Layer >26 and args.STCs :
                    stc_index = str(module[3])
                    stc_energy = str(module[4])
                    STC_channel,STC_word = create_numbering.get_STC_channel(Layer,module[0],module_u,module_v,stc_index)
                    res +=  str(STC_channel)+','+str(STC_word)+','+ module_energy +','
                    intmatrix += 3
    res ='/* out'+nbzeros+str(int(i*20+j)).zfill(4)+'_em-eta'+str(j)+'-phi'+str(i)+'*/'+'\t'+str(int(nbmodintower))+', ' +res
    adder += nb_module_in_pTT
    return(res,intmatrix,adder,nb_module_in_pTT)





