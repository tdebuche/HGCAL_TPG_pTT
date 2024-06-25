The input files for the geometry is one json file for the modules and one for the STCs; they are created in another repository named Geometry.
This other repository has as input modmaps files (== modules geometry) and allows to build STCs.

The programs in this folder are :

Z_coordinate : records a numpy array with the z coordinate of each layer

functions : some  usefull functions used to make plots

Bins : create a json file with bins in XY coordinates. You can choose two scenarios : 480 bins or 560 bins (with or without edges). The output is a json file : {header},{bins}. In 'header', you can record the info on the scenario

Plot_Geometry : to plot of a layer. There are few options 

   
