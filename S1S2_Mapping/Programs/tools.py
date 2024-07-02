
Endcap = 0
Subsector = 0
def get_pTT_numbers(pTT):
    S1Board = int(pTT[4:6],16) & 0x3F
    phi = int(pTT,16) & 0x1F
    eta = (int(pTT,16) & 0x3E0) //(16 * 2)
    CEECEH = (int(pTT,16) & 0x400) //(16*16*4)
    Sector = (int(pTT[2],16) &  0x6)//2
    return(Sector,S1Board,eta,phi,CEECEH)

def channel(board,link,word,args):
    Sector,S2Board = args.Sector,args.S2_Board
    subsystem  = 1
    obj_type = 5
    t = ''
    binary = ''
    binary += decimaltobinary(1,Endcap)
    binary += decimaltobinary(2,Sector)
    binary += decimaltobinary(1,Subsector)
    binary += decimaltobinary(2,subsystem)
    binary += decimaltobinary(4,obj_type)
    S1_ID =  board_6ID(board)
    binary +=  S1_ID
    binary += decimaltobinary(5,S2Board)
    binary += decimaltobinary(3,link)
    binary += decimaltobinary(2,word)
    binary += '000000'
    return('0x'+ binarytohexa(8,binary))


def tower(board,i,j,CEECEH,Sector):
    subsystem  = 1
    obj_type = 6
    t = ''
    binary = ''
    binary += decimaltobinary(1,Endcap)
    binary += decimaltobinary(2,Sector)
    binary += decimaltobinary(1,Subsector)
    binary += decimaltobinary(2,subsystem)
    binary += decimaltobinary(4,obj_type)
    S1_ID =  board_6ID(board)
    binary +=  S1_ID
    binary += '00000'
    binary += str(int(CEECEH))
    binary += decimaltobinary(5,i)   #eta
    binary += decimaltobinary(5,j)   #phi
    return('0x'+ binarytohexa(8,binary))

def board_6ID(board):
    doublehexa = board[4:6]
    return(hexatobinary(8,doublehexa)[2:8])


def S1ID(Sector,board):
    subsystem  = 1
    obj_type = 0
    binary = decimaltobinary(1,Endcap)+decimaltobinary(2,Sector)+decimaltobinary(1,Subsector)
    binary += decimaltobinary(2,subsystem)
    binary += decimaltobinary(4,obj_type)
    binary += decimaltobinary(6,board)
    binary += decimaltobinary(16,0)
    return('0x'+ binarytohexa(8,binary))


def decimaltobinary(nbbits,number):
    t =''
    res = 0
    reste = number
    for i in range(nbbits):
        res = reste//(2**(nbbits-1-i))
        reste = reste - res *2**(nbbits-1-i)
        t+= str(res)
    return(t)

def decimaltohexa(nbhexa,number):
    t =''
    res = 0
    reste = number
    hexa = ['A','B','C','D','E','F']
    for i in range(nbhexa):
        res = reste//(16**(nbhexa-1-i))
        reste = reste - res *16**(nbhexa-1-i)
        if res <10:
            t+= str(res)
        else:
            t += hexa[res-10]
    return(t)

def binarytodecimal(binary):
    t = 0
    for i in range(len(binary)):
            t+= int(binary[i]) * 2**(len(binary)-1-i)
    return t


def hexatodecimal(hexanumber):
    t = 0
    hexa = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    for i in range(len(hexanumber)):
        for j in range(16):
            if hexanumber[i] == hexa[j]:
                t+= j * 16**(len(hexanumber)-1-i)
    return t

def hexatobinary(nbbits,hexanumber):
    return(decimaltobinary(nbbits,hexatodecimal(hexanumber)))

def binarytohexa(nbhexa,binary):
    return(decimaltohexa(nbhexa,binarytodecimal(binary)))


