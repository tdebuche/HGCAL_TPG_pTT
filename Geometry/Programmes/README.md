Z_coordinate : records a numpy array with the z coordinate of each layer

functions : some  usefull functions to convert coordinates (eta,phi,z) <-> (x,y,z), to convert points into shapely polygon, and to create list to plot bins or modules.

Modules : with the file geometrymodules.xml (produced by Pedro), records an arrray with all the modules of all layers.

Scenarios : records two arrays with the values of the two scenarios : 20eta24phi bins and 20eta28phi bins. 
            The values are nb_binphi,nb_bineta,phimin,phimax,etamin,etamax

Binsetaphi : records an array with the bins eta phi for the two scenarios.

STCs : records the STCs of all layers in two arrays : one for low density layers and one for high density layers.

Plot_Geometry : makes the plot of a layer. There are few parameters : Layer number, with our without bins, with our without UV coordinates, with our without Numbering, with our without STCs, with our without Edges (20 24 or 20 28). 


