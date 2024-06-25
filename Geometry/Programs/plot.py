import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

from Geometry.Programs.tools import *




def plot_layer(args,Layer):
    Layer = args.Layer
    plt.figure(figsize = (12,8))
    plt.title(label =  'Layer '+str(Layer))
    plt.xlabel('x (mm)')
    plt.ylabel('y (mm)')
    #plot Moddule
    Module_Vertices = item_list('src/Modules.json','vertices',Layer)
    Module_irot = item_list('src/Modules.json','irot',Layer)
    Module_UV = item_list('src/Modules.json','uv',Layer)
    for module_idx in range(len(Module_Vertices)):
	    irot = Module_irot[module_idx]
	    if irot != 999: # no rotations for scintillators
		    vertices = reorganize_vertices(Module_Vertices[module_idx],irot)
	    else :
		    vertices = Module_Vertices[module_idx]
	    Xvertices= vertices[0] +[vertices[0][0]]
	    Yvertices= vertices[1] +[vertices[1][0]]
	    plt.plot(Xvertices,Yvertices,color = "black")
	    if args.UV == "yes":
	        u,v = Module_UV[module_idx][0],Module_UV[module_idx][1]
	        plt.annotate("("+str(u)+","+str(v)+")",(x-60,y-10),size =  '8')
	    if args.irot == "yes":
		    x,y = np.sum(np.array(vertices[0]))/len(vertices[0]),np.sum(np.array(vertices[1]))/len(vertices[0])
		    plt.annotate(str(irot),(x-60,y-10),size =  '8')
		    plt.scatter((x+Xvertices[0])/2,(y+Yvertices[0])/2 ,color ="red")
    if args.STCs == "yes":
        STC_Vertices = item_list('src/STCs.json','vertices',Layer)
        for STC_idx in range(len(STC_Vertices)):
	        vertices = STC_Vertices[STC_idx]
	        Xvertices= vertices[0] +[vertices[0][0]]
	        Yvertices= vertices[1] +[vertices[1][0]]
	        plt.plot(Xvertices,Yvertices,linewidth = 0.2,color  = 'blue')
    if args.Record_plots == 'no':
        plt.show()
    if args.Record_plots == 'yes':
	    path = "Geometry/Plots/v2"
	    if args.STCs == "yes" and args.Bins == "yes" and args.UV == "no" and args.irot == "no":
		    path += "/Layers_with_Bins"
		if args.STCs == "no" and args.Bins == "no" and args.UV == "yes" and args.irot == "no":
			path += "/Layers_with_UV"
		if args.STCs == "no" and args.Bins == "no" and args.UV == "no" and args.irot == "yes":
			path += "/Layers_with_irot"
		os.chdir(path)
		plt.savefig('Layer '+str(Layer)+'.png')
		os.chdir("HGCAL_TPG_pTT")



def record_all_layers(args):
    for Layer in range(1,48):
        if not (Layer < 27 and Layer%2==0):
            plot_layer(args,Layer)


















    
    
