import json
from collections import defaultdict

#upload Modules and STCs 
with open('src/v13.1/Modules.json','r') as file:
    Modules = json.load(file)
with open('src/v13.1/STCs.json','r') as file:
    STCs = json.load(file)

#Board IDs with their layers (the fisrt list for the Si module, the second for the scintillators)
Boards = [['0x64000000', 3, 34], ['0x64010000', 1, 36, 47], ['0x64020000', 33, 40, 41], ['0x64030000', 9, 39, 44], ['0x64040000', 7, 42, 43], ['0x64050000', 13, 38, 46], ['0x64060000', 17, 27], ['0x64070000', 25, 31], ['0x64080000', 23, 30], ['0x64090000', 15, 32], ['0x640A0000', 19, 29], ['0x640B0000', 21, 28], ['0x640C0000', 5, 35], ['0x640D0000', 11, 37, 45]]
Boards_scintillators = [['0x64000000', 47], ['0x64010000',41], ['0x64020000',43], ['0x64030000', 37], ['0x64040000', 38], ['0x64050000', 35], ['0x64060000', 40], ['0x64070000', 39], ['0x64080000',42], ['0x64090000', 36], ['0x640A0000', 44], ['0x640B0000',45], ['0x640C0000', 46], ['0x640D0000', 34]]



#create CE-E and CE-H numbering for modules only 
def create_module_numbering(args):
  #upload Module
  with open('src/'+args.Modmap_version+'/Modules.json','r') as file:
    Modules = json.load(file)
  CEE_numbering = defaultdict(list)
  CEH_numbering = defaultdict(list)
  #to count the number of modules in CEE and CEH of eadch board
  CEE_count,CEH_count = 0,0
  #to store the counts 
  nb_modules_per_board = []
  #look at each board
  for Board_number in range(14):
    #take the layers treated by this board
    Layers = Boards[Board_number][1:]
    Layers.append(Boards_scintillators[Board_number][1])
    #look at each layer treated by the board
    for lay in range(len(Layers)):
      Layer = Layers[lay]
      #look at each module
      for module_idx in range(len(Modules[Layer-1])):
        module = Modules[Layer-1][module_idx]
        module_type = module['type']
        #check if it is a module treated by this board
        if (module_type=='silicon' and lay!=len(Layers)-1) or (module_type=='scintillator' and lay==len(Layers)-1):
          module_u = module['u']
          module_v = module['v']
          if Layer < 27:
            #add the module in the CEE_numbering
            CEE_numbering[(Layer,module_type,module_u,module_v)].append(CEE_count)
            CEE_count +=1
          if Layer > 26:
            #add the module in the CEH_numbering
            CEH_numbering[(Layer,module_type,module_u,module_v)].append(CEH_count)
            CEH_count +=1
    #store the counts 
    nb_modules_per_board.append({'Board':Board_number,'CEE_count':CEE_count,'CEH_count':CEH_count})
    CEE_count,CEH_count = 0,0
  return(CEE_numbering,CEH_numbering,nb_modules_per_board)
    

#create the CE-H numbering for STCs
def create_STC_numbering(args):
  #upload STCs
  with open('src/'+args.Modmap_version+'/STCs.json','r') as file:
    STCs = json.load(file)
  STC_numbering = defaultdict(list)
  #channel count and STC inside a channel count
  channel_count,STC_count = 0,0
  #number of channel per board
  STC_channels_per_board = []
  #look at each board
  for Board_number in range(14):
    #take the layers treated by this board
    Layers = Boards[Board_number][1:]
    Layers.append(Boards_scintillators[Board_number][1])
    #look at each layer 
    for lay in range(len(Layers)):
      Layer = Layers[lay]
      #check if it is a CE-H layer
      if Layer >26:
        #look at each STC
        for STC_idx in range(len(STCs[Layer-1])):
          stc = STCs[Layer-1][STC_idx]
          stc_type = stc['type']
          #check if it is a STC treated by this board
          if (stc_type=='silicon' and lay!=len(Layers)-1) or (stc_type=='scintillator' and lay==len(Layers)-1):
            #module u,v coordinates and the STC index
            stc_u = stc['u']
            stc_v = stc['v']
            stc_idx = stc['index']
            #if it is the first STC of this module treated (equivalent to first channel of this module is not created)
            if STC_numbering[(Layer,stc_type,stc_u,stc_v,0)] == []:
              #create a new channel and add it to the numbering 
              STC_numbering[(Layer,stc_type,stc_u,stc_v,0)].append(channel_count)
              STC_numbering[(Layer,stc_type,stc_u,stc_v,0)].append(defaultdict(list))
              #increase the number of channels already created
              channel_count += 1
            #if the first (index 0 (Layer,stc_type,stc_u,stc_v,0) ) channel of this module is not filled (there are 6 places)
            if len(STC_numbering[(Layer,stc_type,stc_u,stc_v,0)][1]) < 6:
              #look at the number of STCs already put in this channel
              STC_count = len(STC_numbering[(Layer,stc_type,stc_u,stc_v,0)][1])
              #add the new one with its numbering
              STC_numbering[(Layer,stc_type,stc_u,stc_v,0)][1][stc_idx].append(STC_count)

            #if the fisrt channel of this module is filled (there are 6 places)
            elif len(STC_numbering[(Layer,stc_type,stc_u,stc_v,0)][1]) == 6:
              #if the second channel is not created (index 1)
              if STC_numbering[(Layer,stc_type,stc_u,stc_v,1)] == []:
                #create the channel
                STC_numbering[(Layer,stc_type,stc_u,stc_v,1)].append(channel_count)
                STC_numbering[(Layer,stc_type,stc_u,stc_v,1)].append(defaultdict(list))
                channel_count += 1
                #put the STC count to 0
                STC_count = len(STC_numbering[(Layer,stc_type,stc_u,stc_v,1)][1])
                #add the STC
                STC_numbering[(Layer,stc_type,stc_u,stc_v,1)][1][stc_idx].append(STC_count)
              else: 
                #look at the number of STCs already put in this channel
                STC_count = len(STC_numbering[(Layer,stc_type,stc_u,stc_v,1)][1])
                #add the new one with its numbering
                STC_numbering[(Layer,stc_type,stc_u,stc_v,1)][1][stc_idx].append(STC_count)
            #if the second channel is not yet created, create it
            if STC_numbering[(Layer,stc_type,stc_u,stc_v,1)] == []:
              STC_numbering[(Layer,stc_type,stc_u,stc_v,1)].append(channel_count)
              STC_numbering[(Layer,stc_type,stc_u,stc_v,1)].append(defaultdict(list))
              channel_count += 1
    #store the counts
    STC_channels_per_board.append({'Board':Board_number,'STCs_count':channel_count})
    channel_count,STC_count = 0,0
  return(STC_numbering,STC_channels_per_board)



#return the number of inputs in the CE-E and CE-H part for a given board
def nb_inputs(args,Board_number,nb_modules_per_board,STC_channels_per_board):
  if args.STCs == "no":
    return(nb_modules_per_board[Board_number]['CEE_count'],nb_modules_per_board[Board_number]['CEH_count'])
  if args.STCs == "yes":
    return(nb_modules_per_board[Board_number]['CEE_count'],STC_channels_per_board[Board_number]['STCs_count'])


#get the numbering of a given module     
def get_module_channel(Layer,type,module_u,module_v,CEE_numbering,CEH_numbering):
    if Layer < 27:
        return(CEE_numbering[(Layer,type,module_u,module_v)][0])
    if  Layer >26 :
        return(CEH_numbering[(Layer,type,module_u,module_v)][0])


#get the numbering of a given STC
def get_STC_channel(Layer,type,module_u,module_v,index,STC_numbering):
  #check if the STC is in the first channel of its module
  if STC_numbering[(Layer,type,module_u,module_v,0)][1][index] != []:
    STC_channel = STC_numbering[(Layer,type,module_u,module_v,0)][0]
    STC_word = STC_numbering[(Layer,type,module_u,module_v,0)][1][index][0]
    return(STC_channel,STC_word)
  #check if the STC is in the second channel of its module
  if STC_numbering[(Layer,type,module_u,module_v,1)][1][index] != []:
    STC_channel = STC_numbering[(Layer,type,module_u,module_v,1)][0]
    STC_word = STC_numbering[(Layer,type,module_u,module_v,1)][1][index][0]
    return(STC_channel,STC_word)
