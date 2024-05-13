import numpy as np
import matplotlib.pyplot as plt
import os

nom_fichier = 'Geometrymodule'

os.chdir("../Ressources")
f = open(nom_fichier + '.xml', 'r')

fichier = f.readlines()
f.close()



#Build an array(47,146,2,6) with (lay,mod-->[[Xvertices],[Yvertices]]) and an array(47,146,2) with (lay,mod-->[[u],[v]])

def geometrymodules(file):
    L =[]
    l = []
    L2 = []
    l2 = []
    lay = 0
    for x in fichier:
        if x[0:11] == '\t<Plane id=':
            l =[]
            l2 = []
            lay +=1
        if x[0:10] == '\t\t\t<Module':
            l.append(module_vertices(x))
            u,v,layer = module_number(x)
            l2.append([u,v])
        if x == '\t</Plane>\n':
            L.append(l)
            L2.append(l2)
    return(L,L2)





def module_number(str) : #u,v,layer of a Module
    code = str[15:25]    # ID du module 0x60013200
    v = hexanumber(code[7])
    u =  hexanumber(code[6])
    layer = hexanumber(code[4:6])
    return (u,v,layer)

def module_vertices(x):  #Vertices of a module
    str = x[:-5]
    j = len(str)-1
    pos = ''
    while str[j] != '"':
        pos = str[j] + pos
        j = j -1
    X = np.zeros((2,6))
    xcourant = ''
    ycourant = ''
    res = 0
    vertex = 0
    for i in range(len(pos)):
        if pos[i] ==';':
            res = 0
            X[0,vertex] = float(xcourant)
            X[1,vertex] = float(ycourant)
            xcourant = ''
            ycourant = ''
            vertex+=1
        elif pos[i] == ',':
            res = 1
        elif res == 0:
            xcourant += pos[i]
        elif res == 1:
            ycourant += pos[i]
    X[0,vertex] = float(xcourant)
    X[1,vertex] = float(ycourant)
    return(X)



def hexanumber(x) :
    n = 0
    l =['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    puissance_max = len(x) - 1
    for i in range(len(x)) :
        for j in range(len(l)) :
            if x[i] == l[j] :
                n += j * 16**(puissance_max - i)
    return(n)



Geometry,L2 = geometrymodules(fichier)
max = 0
for x in Geometry:
    if len(x) >max:
        max = len(x)
G = np.zeros((len(Geometry),max,2,6))

for i in range(len(Geometry)):
    for  j in range(len(Geometry[i])):
        G[i,j] = Geometry[i][j]

UV = np.zeros((47,max,2),dtype = int)
for i in range(47):
    for j in range(len(L2[i])):
        UV[i,j,0] = int(L2[i][j][0])
        UV[i,j,1] = int(L2[i][j][1])


#record the files
os.chdir("../Ressources")
np.save('Geometry',G)
np.save('uv.npy',UV)

os.chdir("../../Ressources")
np.save('Geometry',G)
np.save('uv.npy',UV)




















