import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path+'/../Ressources')

parser = argparse.ArgumentParser()
parser.add_argument("Sector", help="Layer to display",type=int)
parser.add_argument("S2Board", help="Layer to display",type = int)
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
        text +=  ''
        for j in range(4):
            for k in range(2):
                res = 0
                for eta in range(10*(k%2),10*(k%2 + 1)):
                    for phi in range(9 * (1-j//2+1) +5, 9* (1-j//2) +5,-1):
                        if j%2 == 0:
                            t = 'S1_Board='+str(int(i))+', eta='+str(eta)+', phi='+str(phi)+ ', CE-E'
                        if j%2 == 1 :
                            t = 'S1_Board='+str(int(i))+', eta='+str(eta)+', phi='+str(phi)+ ', CE-H'
                        if res < 10:
                            nbzeros = '00'
                        if  res > 9:
                            nbzeros = '0'
                        text += 'Sector='+str(Sector)+', S2_board='+str(S2Board)+', Frame id = "'+nbzeros +str( res)+'", Link='+str(j)+', Word='+str(k)+', pTT : '+ t +'\n'
                        
                        res +=1
                    if res < 10:
                        nbzeros = '00'
                    if  res > 9:
                        nbzeros = '0'
                    if res > 99:
                        nbzeros = ''
                    text += 'Sector='+str(Sector)+', S2_board='+str(S2Board)+', Frame id = "'+nbzeros +str( res)+'", Link='+str(j)+', Word='+str(k) +'\n'
                    res +=1
                for f in range(res,108):
                    if f < 100:
                        nbzeros = '0'
                    else:
                        nbzeros = ''
                    text += 'Sector='+str(Sector)+', S2_board='+str(S2Board)+', Frame id = "'+nbzeros +str( res)+'", Link='+str(j)+', Word='+str(k) +'\n'
    return text

def allocation4linksEdges(Sector,S2Board):
    Boards = [S1ID(Sector,board) for board in range(14)]
    text = ''
    for i in range(len(Boards)):
        for j in range(4):
            for k in range(2):
                res = 0
                for eta in range(10*(k%2),10*(k%2 + 1)):
                    if j//2 != 1:
                        if j%2 == 0:
                            t = 'S1_Board='+str(int(i))+', eta='+str(eta)+', phi='+str(27)+ ', CE-E'
                        if j%2 ==1 :
                            t = 'S1_Board='+str(int(i))+', eta='+str(eta)+', phi='+str(27)+ ', CE-H'
                        if res < 10:
                            nbzeros = '00'
                        if  res > 9:
                            nbzeros = '0'
                        if res > 99:
                            nbzeros = ''
                        text += 'Sector='+str(Sector)+', S2_board='+str(S2Board)+', Frame id = "'+nbzeros +str( res)+'", Link='+str(j)+', Word='+str(k)+', pTT : '+ t +'\n'
                        res +=1
                    for phi in range(9 * (1-j//2+1) +8, 9* (1-j//2) +8,-1):
                        if j%2 == 0:
                            t = 'S1_Board='+str(int(i))+', eta='+str(eta)+', phi='+str(phi)+ ', CE-E'
                        if j%2 ==1 :
                            t = 'S1_Board='+str(int(i))+', eta='+str(eta)+', phi='+str(phi)+ ', CE-H'
                        if res < 10:
                            nbzeros = '00'
                        if  res > 9:
                            nbzeros = '0'
                        if res > 99:
                            nbzeros = ''
                        text += 'Sector='+str(Sector)+', S2_board='+str(S2Board)+', Frame id = "'+nbzeros +str( res)+'", Link='+str(j)+', Word='+str(k)+', pTT : '+ t +'\n'
                        res +=1
                    if res < 10:
                        nbzeros = '00'
                    if  res > 9:
                        nbzeros = '0'
                    if res > 99:
                        nbzeros = ''
                    if j//2 == 1 or res < 97:
                        text += 'Sector='+str(Sector)+', S2_board='+str(S2Board)+', Frame id = "'+nbzeros +str( res)+'", Link='+str(j)+', Word='+str(k) +'\n'
                        res +=1
                for f in range(res,108):
                    if f < 100:
                        nbzeros = '0'
                    else:
                        nbzeros = ''
                    text += 'Sector='+str(Sector)+', S2_board='+str(S2Board)+', Frame id = "'+nbzeros +str( res)+'", Link='+str(j)+', Word='+str(k) +'\n'

    return text





def allocation2linksNoEdges(Sector,S2Board):
    Boards = [S1ID(Sector+1,board) for board in range(14)]
    text = ''
    for i in range(len(Boards)):
        for j in range(2):
            for k in range(2):
                res = 0
                for eta in range(10*(k%2),10*(k%2 + 1)):
                    for phi in range(5, -1,-1):
                        if j%2 == 0:
                            t = 'S1_Board='+str(int(i))+', eta='+str(eta)+', phi='+str(phi)+ ', CE-E'
                        if j%2 == 1 :
                            t = 'S1_Board='+str(int(i))+', eta='+str(eta)+', phi='+str(phi)+ ', CE-H'
                        if res < 10:
                            nbzeros = '00'
                        if  res > 9:
                            nbzeros = '0'
                        text += 'Sector='+str(Sector)+', S2_board='+str(S2Board)+', Frame id = "'+nbzeros +str( res)+'", Link='+str(j)+', Word='+str(k)+', pTT : '+ t +'\n'
                        res +=1
                    if res < 10:
                        nbzeros = '00'
                    if  res > 9:
                        nbzeros = '0'
                    if res > 99:
                        nbzeros = ''
                    text += 'Sector='+str(Sector)+', S2_board='+str(S2Board)+', Frame id = "'+nbzeros +str( res)+'", Link='+str(j)+', Word='+str(k) +'\n'
                    res +=1
                for f in range(res,108):
                    if f < 100:
                        nbzeros = '0'
                    else:
                        nbzeros = ''
                    text += 'Sector='+str(Sector)+', S2_board='+str(S2Board)+', Frame id = "'+nbzeros +str( res)+'", Link='+str(j)+', Word='+str(k) +'\n'

    return text

def allocation2linksEdges(Sector,S2Board):
    Boards = [S1ID(Sector+1,board) for board in range(14)]
    text = ''
    for i in range(len(Boards)):
        for j in range(2):
            for k in range(2):
                res = 0
                for eta in range(10*(k%2),10*(k%2 + 1)):
                    for phi in range(8, -1,-1):
                        if j%2 == 0:
                            t = 'S1_Board='+str(int(i))+', eta='+str(eta)+', phi='+str(phi)+ ', CE-E'
                        if j%2 ==1 :
                            t = 'S1_Board='+str(int(i))+', eta='+str(eta)+', phi='+str(phi)+ ', CE-H'
                        if res < 10:
                            nbzeros = '00'
                        if  res > 9:
                            nbzeros = '0'
                        if res > 99:
                            nbzeros = ''
                        text += 'Sector='+str(Sector)+', S2_board='+str(S2Board)+', Frame id = "'+nbzeros +str( res)+'", Link='+str(j)+', Word='+str(k)+', pTT : '+ t +'\n'
                        res +=1
                    if res < 10:
                        nbzeros = '00'
                    if  res > 9:
                        nbzeros = '0'
                    if res > 99:
                        nbzeros = ''
                    if j//2 == 1 or res < 97:
                        text += 'Sector='+str(Sector)+', S2_board='+str(S2Board)+', Frame id = "'+nbzeros +str( res)+'", Link='+str(j)+', Word='+str(k) +'\n'
                        res +=1
                for f in range(res,108):
                    if f < 100:
                        nbzeros = '0'
                    else:
                        nbzeros = ''
                    text += 'Sector='+str(Sector)+', S2_board='+str(S2Board)+', Frame id = "'+nbzeros +str( res)+'", Link='+str(j)+', Word='+str(k) +'\n'

    return text



def channel(board,link,word):
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
    binary += decimaltobinary(5,S2)
    binary += decimaltobinary(3,link)
    binary += decimaltobinary(2,word)
    binary += '000000'
    return('0x'+ binarytohexa(8,binary))


def tower(board,i,j,CEECEH):
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
    file = open("AllocationpTTsEdges_Readable.txt", "w")
    file.write(allocation4linksEdges(Sector,S2))
if args.Edges == 'no':
    file = open("AllocationpTTsNoEdges_Readable.txt", "w")
    file.write(allocation4linksNoEdges(Sector,S2))
file.close()

if args.Edges == 'yes':
    file = open("DuplicationpTTsEdges_Readable.txt", "w")
    file.write(allocation2linksEdges(Sector,S2))
if args.Edges == 'no':
    file = open("DuplicationpTTsNoEdges_Readable.txt", "w")
    file.write(allocation2linksNoEdges(Sector,S2))
file.close()


