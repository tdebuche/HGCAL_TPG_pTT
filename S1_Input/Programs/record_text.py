from S1_Input.Programs.create_numbering import get_STC_channel,get_module_channel,create_module_numbering,create_STC_numbering
import json



Boards = [['0x64000000', 3, 34], ['0x64010000', 1, 36, 47], ['0x64020000', 33, 40, 41], ['0x64030000', 9, 39, 44], ['0x64040000', 7, 42, 43], ['0x64050000', 13, 38, 46], ['0x64060000', 17, 27], ['0x64070000', 25, 31], ['0x64080000', 23, 30], ['0x64090000', 15, 32], ['0x640A0000', 19, 29], ['0x640B0000', 21, 28], ['0x640C0000', 5, 35], ['0x640D0000', 11, 37, 45]]
Boards_scintillators = [['0x64000000', 47], ['0x64010000',41], ['0x64020000',43], ['0x64030000', 37], ['0x64040000', 38], ['0x64050000', 35], ['0x64060000', 40], ['0x64070000', 39], ['0x64080000',42], ['0x64090000', 36], ['0x640A0000', 44], ['0x640B0000',45], ['0x640C0000', 46], ['0x640D0000', 34]]


def record_input(args):
    with open('src/'+args.Modmap_version+'/Modules.json','r') as file:
        Modules = json.load(file)
    with open('src/'+args.Modmap_version+'/STCs.json','r') as file:
        STCs = json.load(file)
    CEE_numbering,CEH_numbering,nb_modules_per_board = create_module_numbering(args)
    STC_numbering,STC_channels_per_board = create_STC_numbering(args)
    text_CEE = 'Input CEE pTT Stage 1' + '\n\n'
    text_CEH = 'Input CEH pTT Stage 1'   '\n\n'
    for Board_number in range(14):
        Layers = Boards[Board_number][1:]
        Layers.append(Boards_scintillators[Board_number][1])
        text_CEE += '\t' + 'Board = ' + Boards[Board_number][0] +'\n'
        text_CEH += '\t' + 'Board = ' + Boards[Board_number][0] +'\n'
        for lay in range(len(Layers)):
            Layer = Layers[lay]
            if Layer > 26 and args.STCs =='yes': single_layer_modules =  STCs[Layer-1]
            else : single_layer_modules =  Modules[Layer-1]
                
            for module_idx in range(len(single_layer_modules)):
                module = single_layer_modules[module_idx]
                module_type,module_u,module_v = module['type'],module['u'], module['v']
                if Layer <27:
                    channel =get_module_channel(Layer,module_type,module_u,module_v,CEE_numbering,CEH_numbering)
                    text_CEE +='\t\t Board_' + str(Board_number) + ', Channel_' + str(channel)
                    text_CEE += ' =  Layer_'+str(Layer)+', ('+str(module_u)+','+str(module_v)+') ' + module_type +' \n'
                if Layer > 26 and ((lay!=len(Layers)-1 and module_type=='silicon') or (lay==len(Layers)-1 and module_type=='scintillator')):
                    if args.STCs == 'no':
                        channel =get_module_channel(Layer,module_type,module_u,module_v,CEE_numbering,CEH_numbering)
                        text_CEH +='\t\t Board_' + str(Board_number) + ', Channel_' + str(channel)
                        text_CEH += ' =  Layer_'+str(Layer)+', ('+str(module_u)+','+str(module_v)+') ' + module_type +' \n'
                    if args.STCs == 'yes':
                        stc_idx = module['index']
                        channel,word =get_STC_channel(Layer,module_type,module_u,module_v,stc_idx,STC_numbering)
                        text_CEH +='\t\t Board_' + str(Board_number) + ', Channel_' + str(channel) + ', Word_' + str(word) 
                        text_CEH += ' =  Layer_'+str(Layer)+', ('+str(module_u)+','+str(module_v)+','+str(stc_idx)+') '+ module_type +' \n'
    file = open('S1_Input/Results/txt_files/'+args.pTT_version+'/Input_CEE.txt', "w")
    file.write(text_CEE)
    file.close()
    file = open('S1_Input/Results/txt_files/'+args.pTT_version+'/Input_CEH.txt', "w")
    file.write(text_CEH)
    file.close()
    return text_CEE,text_CEH

