
import numpy as np
import argparse
import json
from pTTs.Programs.Energy_Sharing import reverse_pTTs
from S1_Input.Programs.create_numbering import get_STC_channel,get_module_channel,create_module_numbering,create_STC_numbering,nb_inputs
import pTTs.Programs.tools as tools

Boards = [['0x64000000', 3, 34], ['0x64010000', 1, 36, 47], ['0x64020000', 33, 40, 41], ['0x64030000', 9, 39, 44], ['0x64040000', 7, 42, 43], ['0x64050000', 13, 38, 46], ['0x64060000', 17, 27], ['0x64070000', 25, 31], ['0x64080000', 23, 30], ['0x64090000', 15, 32], ['0x640A0000', 19, 29], ['0x640B0000', 21, 28], ['0x640C0000', 5, 35], ['0x640D0000', 11, 37, 45]]
Boards_scintillators = [['0x64000000', 47], ['0x64010000',41], ['0x64020000',43], ['0x64030000', 37], ['0x64040000', 38], ['0x64050000', 35], ['0x64060000', 40], ['0x64070000', 39], ['0x64080000',42], ['0x64090000', 36], ['0x640A0000', 44], ['0x640B0000',45], ['0x640C0000', 46], ['0x640D0000', 34]]



def record_all_boards(args):
    with open('src/'+args.Modmap_version+'/Modules.json','r') as file:
        Modules = json.load(file)
    with open('src/'+args.Modmap_version+'/STCs.json','r') as file:
        STCs = json.load(file)
    CEE_numbering,CEH_numbering,nb_modules_per_board = create_module_numbering(args)
    STC_numbering,STC_channels_per_board = create_STC_numbering(args)
    if args.Format == 'vh': path = "pTTs/Results/"+args.pTT_version+"/VH_files"
    if args.Format == 'readable':path = "pTTs/Results/"+args.pTT_version+"/Readable_files"
    if args.Edges == 'yes' : path += '/28_Phi_Bins'
    if args.Edges == 'no' : path += '/24_Phi_Bins'
    if args.STCs == 'yes' : path += '/with_STCs/'
    if args.STCs == 'no' : path += '/without_STC/s'
    all_boards_CEE,all_boards_CEH = '',''
    for Board in range(14):
        text_CEE,text_CEH = files_single_board(args,Board,Modules,STCs,CEE_numbering,CEH_numbering,STC_numbering,nb_modules_per_board,STC_channels_per_board)
        all_boards_CEE += 'Board '+ Boards[Board][0] + '\n'
        all_boards_CEH += 'Board '+ Boards[Board][0]+ '\n'
        all_boards_CEE += text_CEE  + '\n'
        all_boards_CEH += text_CEH + '\n'
        name = 'CE_E_'+  str(Board)+ '_v2'
        if args.Format == 'vh': name += '.vh'
        if args.Format == 'readable': name += '.txt'
        file = open(path+name, "w")
        file.write(text_CEE)
        file.close()
        name = 'CE_H_'+  str(Board)+ '_v2'
        if args.Format == 'vh': name += '.vh'
        if args.Format == 'readable': name += '.txt'
        file = open(path+name, "w")
        file.write(text_CEH)
        file.close()
    name ="CE_E_allBoards"
    file = open(path+name+".txt", "w")
    file.write(all_boards_CEE)
    file.close()
    name ="CE_H_allBoards"
    file = open(path+name+".txt", "w")
    file.write(all_boards_CEH)
    file.close()

    
def files_single_board(args,Board_number,Modules,STCs,CEE_numbering,CEH_numbering,STC_numbering,nb_modules_per_board,STC_channels_per_board):
    CEE_pTTs,CEH_pTTs = pTTs_single_board(args,Board_number,Modules,STCs)
    nb_CEE_inputs,nb_CEH_inputs = nb_inputs(args,Board_number,nb_modules_per_board,STC_channels_per_board)
    header = tools.import_header(args)
    nb_binphi,nb_bineta = header['nb_phibin'],header['nb_etabin']
    nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
    text_CEE, text_CEH= '',''
    intmatrixE,intmatrixH = -1,-1
    adderE,adderH = 0,0
    maxE,maxH = 0,0
    for phi in range(nb_binphi):
        for eta in range(nb_bineta):
            resE,intmatrixE,adderE,nbmodintowerE = single_pTT_text(args,CEE_pTTs,phi,eta,intmatrixE,adderE,CEE_numbering,CEH_numbering,STC_numbering)
            if nbmodintowerE > maxE:
                maxE = nbmodintowerE
            resH,intmatrixH,adderH,nbmodintowerH = single_pTT_text(args,CEH_pTTs,phi,eta,intmatrixH,adderH,CEE_numbering,CEH_numbering,STC_numbering)
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
    header = functions.import_header(args)
    nb_binphi,nb_bineta = header['nb_phibin'],header['nb_etabin']
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
                if Layer < 27 : 
                    CEE_pTTs[phi][eta].append([Layer,pTT])
                if Layer < 34 and Layer > 26 : 
                    CEH_pTTs[phi][eta].append([Layer,pTT])
                if Layer > 33:
                    selected_Modules = []
                    for module_idx in range(len(pTT)):
                        module_type = pTT[module_idx][0]
                        if module_type == 'silicon' and (lay!=len(Layers)-1) : selected_Modules.append(pTT[module_idx])
                        if module_type == 'scintillator' and (lay==len(Layers)-1) : selected_Modules.append(pTT[module_idx])
                    CEH_pTTs[phi][eta].append([Layer,selected_Modules])

    return(CEE_pTTs,CEH_pTTs)

def single_pTT_text(args,pTT,phi,eta,intmatrix,adder,CEE_numbering,CEH_numbering,STC_numbering):
    res = ''
    nb_module_in_pTT = 0
    intmatrix +=1    #pour le nbmodintower
    pTT  = pTT[phi][eta]
    for lay in range(len(pTT)):
        Layer = pTT[lay][0]
        for module_idx in range(len(pTT[lay][1])):
            nb_module_in_pTT += 1
            module = pTT[lay][1][module_idx]
            module_u,module_v = module[1],module[2]
            if module[0] == 'silicon': module_type = 'Si'
            if module[0] == 'scintillator': module_type = 'Sc'
            if args.Format == 'readable':
                if Layer <27 or args.STCs =='no' :
                    module_energy = str(module[3])
                    res +=  '('+ str(Layer) +','+module_type+',' +str(module_u)+',' +str(module_v)+'),'+ module_energy +','
                    intmatrix += 2
                if Layer >26 and args.STCs =='yes':
                    stc_index = str(module[3])
                    stc_energy = str(module[4])
                    res +=  '('+ str(Layer) +','+module_type+',' +str(module_u)+',' +str(module_v)+','+stc_index+'),'+ stc_energy +','
                    intmatrix += 3
            if args.Format == 'vh':
                if Layer <27 or args.STCs == 'no' :
                    module_energy = str(module[3])
                    module_channel = get_module_channel(Layer,module[0],module_u,module_v,CEE_numbering,CEH_numbering)
                    res +=  str(module_channel)+','+ module_energy +','
                    intmatrix += 2
                if Layer >26 and args.STCs =='yes' :
                    stc_index = module[3]
                    stc_energy = str(module[4])
                    STC_channel,STC_word = get_STC_channel(Layer,module[0],module_u,module_v,stc_index,STC_numbering)
                    res +=  str(STC_channel)+','+str(STC_word)+','+ stc_energy +','
                    intmatrix += 3
    res ='/* out'+str(int(phi*20+eta)).zfill(4)+'_em-eta'+str(eta)+'-phi'+str(phi)+'*/'+'\t'+str(nb_module_in_pTT)+',' + res
    adder += nb_module_in_pTT
    return(res,intmatrix,adder,nb_module_in_pTT)





