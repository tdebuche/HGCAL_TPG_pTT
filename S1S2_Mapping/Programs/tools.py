#some functions on the ids of TPG elements. IDs are calculated thanks to the IDs_v2 excel file from Andy.



def get_pTT_numbers(pTT): #get pTT information from the pTT id
    S1Board = int(pTT[4:6],16) & 0x3F
    phi = int(pTT,16) & 0x1F
    eta = (int(pTT,16) & 0x3E0) //(16 * 2)
    CEECEH = (int(pTT,16) & 0x400) //(16*16*4)
    S1_Sector = (int(pTT[2],16) &  0x6)//2
    return(S1_Sector,S1Board,eta,phi,CEECEH)



def get_channel_id(S1_Sector,S2_Sector,S1_Board,S2_Board,link,word):
    Endcap = 0
    Sector = S1_Sector
    Subsector = 0 
    Subsystem  = 1
    Obj_type = 5
    S1ID = S1_Board
    TM = S2_Board
    ID = link
    Channel = word
    return hex(0x00000000 |((Endcap & 0x1) << 31) | ((Sector & 0x3) << 29) | ((Subsector & 0x1) << 28) | ((Subsystem & 0x3) << 26) | ((Obj_type & 0xF) << 22)  | ((S1ID & 0x3F) << 16) |  ((TM & 0x1F) << 11) | ((ID & 0xF) << 8) | ((Channel & 0xF) << 6))


def get_pTT_id(S1_Sector,S1_Board,eta,phi,CEECEH): # CEECEH is 0 for CEE 1 for CEH
    Endcap = 0
    Sector = S1_Sector
    Subsector = 0 
    Subsystem  = 1
    Obj_type = 6
    S1ID = S1_board
    return hex(0x00000000 |((Endcap & 0x1) << 31) | ((Sector & 0x3) << 29) | ((Subsector & 0x1) << 28) | ((Subsystem & 0x3) << 26) | ((Obj_type & 0xF) << 22)  | ((S1ID & 0x3F) << 16) |  ((CEECEH & 0x1) << 10) | ((eta & 0x1F) << 5) | ((phi & 0x1F) << 0))


def get_S1Board_id(S1_Sector,S1_board):
    Endcap = 0
    Sector = S1_Sector
    Subsector = 0 
    Subsystem  = 1
    Obj_type = 0
    S1ID = S1_board
    return hex(0x00000000 |((Endcap & 0x1) << 31) | ((Sector & 0x3) << 29) | ((Subsector & 0x1) << 28) | ((Subsystem & 0x3) << 26) | ((Obj_type & 0xF) << 22)  | ((S1ID & 0x3F) << 16))


def get_S2Board_id(S2_Sector,S2_Board):
    Endcap = 0
    Sector = S2_Sector
    Subsector = 0 
    Subsystem  = 2
    Obj_type = 0
    TM = S2_Board
    return hex(0x00000000 |((Endcap & 0x1) << 31) | ((Sector & 0x3) << 29) | ((Subsector & 0x1) << 28) | ((Subsystem & 0x3) << 26) | ((Obj_type & 0xF) << 22)  |  ((TM & 0x1F) << 11))

