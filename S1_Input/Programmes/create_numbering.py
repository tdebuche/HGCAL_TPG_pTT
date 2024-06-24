import json
from collections import defaultdict


with open('ProgrammesRessources/Modules.json','r') as file:
    Modules = json.load(file)
with open('ProgrammesRessources/STCs.json','r') as file:
    STCs = json.load(file)


Boards = [['0x64000000', 3, 34], ['0x64010000', 1, 36, 47], ['0x64020000', 33, 40, 41], ['0x64030000', 9, 39, 44], ['0x64040000', 7, 42, 43], ['0x64050000', 13, 38, 46], ['0x64060000', 17, 27], ['0x64070000', 25, 31], ['0x64080000', 23, 30], ['0x64090000', 15, 32], ['0x640A0000', 19, 29], ['0x640B0000', 21, 28], ['0x640C0000', 5, 35], ['0x640D0000', 11, 37, 45]]
Boards_scintillators = [['0x64000000', 47], ['0x64010000',41], ['0x64020000',43], ['0x64030000', 37], ['0x64040000', 38], ['0x64050000', 35], ['0x64060000', 40], ['0x64070000', 39], ['0x64080000',42], ['0x64090000', 36], ['0x640A0000', 44], ['0x640B0000',45], ['0x640C0000', 46], ['0x640D0000', 34]]

    
def create_module_numbering():
  CEE_numbering = defaultdict()
  CEH_numbering = defaultdict()
  CEE_count,CEH_count = 0,0
  for Board_number in range(14):
    Layers = Boards[Board_number][1:]
    Layers.append(Boards_scintillators[Board_number][1])
    for lay in range(len(Layers)):
      Layer = Layers[lay]
      for module_idx in range(len(Modules[Layer-1])):
        module = Modules[Layer-1][module_idx]
        if module['type'] == 'silicon': module_type = 0 
        if module['type'] == 'scintillator': module_type = 1
        if (module['type']=='silicon' and lay!=len(Layers)-1) or (module['type']=='scintillator' and lay==len(Layers)-1):
          module_u = module['u']
          module_v = module['v']
          if Layer < 27:
            CEE_numbering[(Layer,module_type,module_u,module_v)].append(count)
            CEE_count +=1
          if Layer > 26:
            CEH_numbering[(Layer,module_type,module_u,module_v)].append(count)
            CEH_count +=1
    CEE_count,CEH_count = 0,0
  return(CEE_numbering,CEH_numbering)
    


def create_STC_numbering():
  STC_numbering = defaultdict(list)
  module_count,STC_count = 0,0
  for Board_number in range(14):
    Layers = Boards[Board_number][1:]
    Layers.append(Boards_scintillators[Board_number][1])
    for lay in range(len(Layers)):
      Layer = Layers[lay]
      if Layer >26:
        for STC_idx in range(len(STCs[Layer-1])):
          stc = STCs[Layer-1][STC_idx]
          if stc['type'] == 'silicon': stc_type = 0 
          if stc['type'] == 'scintillator': stc_type = 1
          stc_type = stc['type']
          if (stc_type=='silicon' and lay!=len(Layers)-1) or (stc_type=='scintillator' and lay==len(Layers)-1):
            stc_u = stc['u']
            stc_v = stc['v']
            stc_idx = stc['index']
            if STC_numbering[(Layer,stc_type,stc_u,stc_v,0)] == []:
              STC_numbering[(Layer,stc_type,stc_u,stc_v,0)].append(module_count)
              STC_numbering[(Layer,stc_type,stc_u,stc_v,0)].append(defaultdict(list))
              module_count += 1
            if len(STC_numbering[(Layer,stc_type,stc_u,stc_v,0)]) < 6:
              STC_count = len(STC_numbering[(Layer,stc_type,stc_u,stc_v,0)][1])
              STC_numbering[(Layer,stc_type,stc_u,stc_v,0)][1][stc_idx].append(STC_count)
              
            if len(STC_numbering[(Layer,stc_type,stc_u,stc_v,0)]) == 6:
              if STC_numbering[(Layer,stc_type,stc_u,stc_v,1)] == []:
                STC_numbering[(Layer,stc_type,stc_u,stc_v,1)].append(module_count)
                STC_numbering[(Layer,stc_type,stc_u,stc_v,1)].append(defaultdict(list))
                module_count += 1
              STC_count = len(STC_numbering[(Layer,stc_type,stc_u,stc_v,1)][1])
              STC_numbering[(Layer,stc_type,stc_u,stc_v,1)][1][stc_idx].append(STC_count)
    module_count,STC_count = 0,0
  return(STC_numbering)




  

def nb_inputs(args,Board):
  nb_CEE_inputs,nb_CEH_inputs = 0,0
  return(nb_CEE_inputs,nb_CEH_inputs)

def get_module_channel(Layer,type,module_u,module_v):
  if type == 'silicon': module_type = 0 
  if type == 'scintillator': module_type = 1
  return(module_numbering[(Layer,module_type,module_u,module_v)][0])

def get_STC_channel(Layer,type,module_u,module_v,index):
  if type == 'silicon': module_type = 0 
  if type == 'scintillator': module_type = 1
  if module_numbering[(Layer,module_type,module_u,module_v,0)][1][index] != []:
    STC_channel = module_numbering[(Layer,module_type,module_u,module_v,0)][0]
    STC_word = module_numbering[(Layer,module_type,module_u,module_v,0)][1][index][0]
  if module_numbering[(Layer,module_type,module_u,module_v,1)][1][index] != []:
    STC_channel = module_numbering[(Layer,module_type,module_u,module_v,1)][0]
    STC_word = module_numbering[(Layer,module_type,module_u,module_v,1)][1][index][0]
  return(STC_channel,STC_word)
