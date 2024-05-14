# HGCAL_TPG_pTT

This recovery is splitted in few parts : 
- Geometry : allows to build the geometry of the layers (Modules, STCs, bins)
- PTTs : allows to fill the partial trigger towers with the energies of modules or STCs
- Input_S1 : create the numbering of mdoules in each board. The same numbering is used in the PTTs files
- MappingStage1Stage2 : maps the PTTs into links between S1 and S2 boards


Each part is divided in two folders : the first one gathers programmes, and the second one, named "ressources", gathers files produced by the programmes.
As some results are used by every programmes (like the geometry of modules), I create  a folder named "ProgrammesRessources" which stores some useful files.



Finally, some results are stored in "Results".
