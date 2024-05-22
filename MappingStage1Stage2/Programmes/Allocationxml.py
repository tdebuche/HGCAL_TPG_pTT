import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path+'/../Ressources')

parser = argparse.ArgumentParser()
parser.add_argument("Sector", help="Layer to display",type=int)
parser.add_argument("S2Board", help="S2 Board to record",type = int)
parser.add_argument("Edges", default = 'yes', help="Layer to display")
args = parser.parse_args()




Endcap = 0
Sector = args.Sector
Subsector = 0
S2 = args.S2Board

def allocation4linksNoEdges(Sector,S2Board):
    Boards = [S1ID(Sector,board) for board in range(14)]
    text = ''
    for i in range(len(Boards)):
        text +=  '\t'+ '<S1 id="'+Boards[i]+'">'+'\n'
        for j in range(4):
            for k in range(2):
                res = 0
                text += '\t'+'\t' +'<Channel id="'+ channel(Boards[i],j,k,Sector,S2Board)+'" aux-id="'+ str(j*2+k)+'">'+'\n'
                for eta in range(10*(k%2),10*(k%2 + 1)):
                    for phi in range(9 * (1-j//2+1) +5, 9* (1-j//2) +5,-1):
                        if j%2 == 0:
                            t = tower(Boards[i],eta,phi,0,Sector)
                        if j%2 == 1 :
                            t = tower(Boards[i],eta,phi,1,Sector)
                        if res < 10:
                            nbzeros = '00'
                        if  res > 9:
                            nbzeros = '0'
                        text += '\t\t\t'+'<Frame id = "'+nbzeros +str( res)+'"  pTT="'+ t+'" />' +'\n'
                        res +=1
                    if res < 10:
                        nbzeros = '00'
                    if  res > 9:
                        nbzeros = '0'
                    if res > 99:
                        nbzeros = ''
                    text += '\t\t\t'+'<Frame id = "'+nbzeros +str( res)+'" />'+'\n'
                    res +=1
                for f in range(res,108):
                    if f < 100:
                        nbzeros = '0'
                    else:
                        nbzeros = ''
                    text += '\t\t\t'+'<Frame id = "'+nbzeros +str(f)+'" />'+'\n'
                text +=  '\t\t'+'</Channel>'+'\n'
        text +=  '\t'+'</S1>'+'\n'



    return text

def allocation4linksEdges(Sector,S2Board):
    Boards = [S1ID(Sector,board) for board in range(14)]
    text = ''
    for i in range(len(Boards)):
        text +=  '\t'+ '<S1 id="'+Boards[i]+'">'+'\n'
        for j in range(4):
            for k in range(2):
                res = 0
                text +=  '\t'+'\t' +'<Channel id="'+ channel(Boards[i],j,k,Sector,S2Board)+'" aux-id="'+ str(j*2+k)+'"'+'\n'
                for eta in range(10*(k%2),10*(k%2 + 1)):
                    if j//2 != 1:
                        if j%2 == 0:
                            t = tower(Boards[i],eta,27,0,Sector)
                        if j%2 ==1 :
                            t = tower(Boards[i],eta,27,1,Sector)
                        if res < 10:
                            nbzeros = '00'
                        if  res > 9:
                            nbzeros = '0'
                        if res > 99:
                            nbzeros = ''
                        text += '\t\t\t'+'<Frame id = "'+nbzeros +str( res)+'"  pTT="'+ t+'" />' + '\n'
                        res +=1
                    for phi in range(9 * (1-j//2+1) +8, 9* (1-j//2) +8,-1):
                        if j%2 == 0:
                            t = tower(Boards[i],eta,phi,0,Sector)
                        if j%2 ==1 :
                            t = tower(Boards[i],eta,phi,1,Sector)
                        if res < 10:
                            nbzeros = '00'
                        if  res > 9:
                            nbzeros = '0'
                        if res > 99:
                            nbzeros = ''
                        text += '\t\t\t'+'<Frame id = "'+nbzeros +str( res)+'"  pTT="'+ t+'" />' + '\n'
                        res +=1
                    if res < 10:
                        nbzeros = '00'
                    if  res > 9:
                        nbzeros = '0'
                    if res > 99:
                        nbzeros = ''
                    if j//2 == 1 or res < 97:
                        text += '\t\t\t'+'<Frame id = "'+nbzeros +str( res)+'" />'+'\n'
                        res +=1
                for f in range(res,108):
                    if f < 100:
                        nbzeros = '0'
                    else:
                        nbzeros = ''
                    text += '\t\t\t'+'<Frame id = "'+nbzeros +str(f)+'" />' + '\n'
                text += '\t\t'+'</Channel>' + '\n'
        text += '\t'+'</S1>'+'\n'

    return text

def allocation2linksNoEdges(Sector,S2Board):
    Boards = [S1ID(Sector+1,board) for board in range(14)]
    text = ''
    for i in range(len(Boards)):
        text +=  '\t'+ '<S1 id="'+Boards[i]+'">'+'\n'
        for j in range(2):
            for k in range(2):
                res = 0
                text +=  '\t'+'\t' +'<Channel id="'+ channel(Boards[i],j+4,k,Sector + 1,S2Board)+'" aux-id="'+ str((j+4)*2+k)+'"'+'\n'
                for eta in range(10*(k%2),10*(k%2 + 1)):
                    for phi in range(5, -1,-1):
                        if j%2 == 0:
                            t = tower(Boards[i],eta,phi,0,Sector+1)
                        if j%2 == 1 :
                            t = tower(Boards[i],eta,phi,1,Sector+1)
                        if res < 10:
                            nbzeros = '00'
                        if  res > 9:
                            nbzeros = '0'
                        text += '\t\t\t'+'<Frame id = "'+nbzeros +str( res)+'"  pTT="'+ t+'" />' + '\n'
                        res +=1
                    if res < 10:
                        nbzeros = '00'
                    if  res > 9:
                        nbzeros = '0'
                    if res > 99:
                        nbzeros = ''
                    text += '\t\t\t'+'<Frame id = "'+nbzeros +str( res)+'" />'+'\n'
                    res +=1
                for f in range(res,108):
                    if f < 100:
                        nbzeros = '0'
                    else:
                        nbzeros = ''
                    text += '\t\t\t'+'<Frame id = "'+nbzeros +str(f)+'" />' + '\n'
                text += '\t\t'+'</Channel>' + '\n'
        text += '\t'+'</S1>'+'\n'



    return text


def allocation2linksEdges(Sector,S2Board):
    Boards = [S1ID(Sector+1,board) for board in range(14)]
    text = ''
    for i in range(len(Boards)):
        text +=  '\t'+ '<S1 id="'+Boards[i]+'">'+'\n'
        for j in range(2):
            for k in range(2):
                res = 0
                text +=  '\t'+'\t' +'<Channel id="'+ channel(Boards[i],j+4,k,Sector+1,S2Board)+'" aux-id="'+ str((j+4)*2+k)+'"'+'\n'
                for eta in range(10*(k%2),10*(k%2 + 1)):
                    for phi in range(8,-1,-1):
                        if j%2 == 0:
                            t = tower(Boards[i],eta,phi,0,Sector+1)
                        if j%2 ==1 :
                            t = tower(Boards[i],eta,phi,1,Sector+1)
                        if res < 10:
                            nbzeros = '00'
                        if  res > 9:
                            nbzeros = '0'
                        if res > 99:
                            nbzeros = ''
                        text += '\t\t\t'+'<Frame id = "'+nbzeros +str( res)+'"  pTT="'+ t+'" />' + '\n'
                        res +=1
                    if res < 10:
                        nbzeros = '00'
                    if  res > 9:
                        nbzeros = '0'
                    if res > 99:
                        nbzeros = ''
                    if j//2 == 1 or res < 97:
                        text += '\t\t\t'+'<Frame id = "'+nbzeros +str( res)+'" />'+'\n'
                        res +=1
                for f in range(res,108):
                    if f < 100:
                        nbzeros = '0'
                    else:
                        nbzeros = ''
                    text += '\t\t\t'+'<Frame id = "'+nbzeros +str(f)+'" />' + '\n'
                text += '\t\t'+'</Channel>' + '\n'
        text += '\t'+'</S1>'+'\n'

    return text






def channel(board,link,word,Sector,S2Board):
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


if args.Edges == 'yes':
    file = open("AllocationPPTsEdges.xml", "w")
    text = '<AllocationPPTsEdges>'
    text += allocation4linksEdges(Sector,S2)
    text += '</AllocationPPTsEdges>'
    file.write(text)
if args.Edges == 'no':
    file = open("AllocationPttsNoEdges.xml", "w")
    text = '<AllocationPttsNoEdges>'
    text += allocation4linksNoEdges(Sector,S2)
    text += '</AllocationPttsNoEdges>'
    file.write(text)
file.close()

if args.Edges == 'yes':
    file = open("DuplicationPPTsEdges.xml", "w")
    text = '<DuplicationPPTsEdges>'
    text += allocation2linksEdges(Sector,S2)
    text += '</DuplicationPPTsEdges>'
    file.write(text)
if args.Edges == 'no':
    file = open("DuplicationPttsNoEdges.xml", "w")
    text = '<DuplicationPttsNoEdges>'
    text += allocation2linksNoEdges(Sector,S2)
    text += '</DuplicationPttsNoEdges>'
    file.write(text)
file.close()



