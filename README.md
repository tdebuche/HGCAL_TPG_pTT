# HGCAL_TPG_pTT

This recovery allows one to produce the mappings used in the pTT part of the Stage 1.

This recovery is splitted in few parts : 
- Geometry : build the bins of each layer and make some plots
- pTTs : create mapping files used to build the pTTs in the S1 boards
- S1_Input: to create the numbering of modules/STCs in each board (it has to match with the S1 unpacker). The same numbering is used in the pTTs files
- S1-S2 Mapping : map the pTTs into links between S1 and S2 boards
- src : gather files used by programs (geometry of modules, STCs, bins)

Each folder is divided into two folders : the first one gathers programmes, and the second one gathers the files produced by the programmes.


THE PROGRAM 'RUN' ALLOWS TO RUN EVERY PROGRAM OF THIS REPOSITORY 
-



The results are shared into different folders, corresponding to different geometry versions. Here are explanations of the versions currently used :


v1 --> modmap v15.5 (CMSSW v????), STCs are arbitrarily defined.

v2 --> modmap v15.5 (CMSSW v?????), STCs are the good ones for the entire modules but not good at all for the partial ones. Scintillator STCs need also some corrections

v3 --> modmap v13.1 (CMSSW 16), without the good partial module STCs and without scintilators. Module rotations are very different from the v15.5, they are the same as CMSSW 16
