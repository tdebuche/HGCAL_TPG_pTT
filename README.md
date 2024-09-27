# HGCAL_TPG_pTT

This recovery allows one to produce the mappings used in the pTT part of the Stage 1.

This recovery is splitted in few parts : 
- Geometry : build the bins of each layer and make some plots
- pTTs : create mapping files used to build the pTTs in the S1 boards
- S1_Input: to create the numbering of modules/STCs in each board (it has to match with the S1 unpacker). The same numbering is used in the pTTs files
- S1-S2 Mapping : map the pTTs into links between S1 and S2 boards
- src : gather files used by programs (geometry of modules, STCs, bins)

Each folder is divided into two folders : the first one gathers programmes, and the second one gathers the files produced by the programmes.


The program "run" allows one ot run every program of this repository
-

This program has many arguments to know which program has to run with which conditions. 

1) Geometry version and pTT version

  --Modmap_version : Geometry version (default : 'v13.1')
  
  --pTT_version : pTT version depending on geometry verion and other updates (default : 'v3' whoch corresponds to the geometry 'v13.1')
  
3) Choose the scenario

  --STCs : With (yes) or without STCs (no)
  
  --Edges  : With (yes) or without edges(no) --> choose 20 * 28 or 20 * 24 pTTs per sector
  
5) Choose to create and record the mapping
  --pTTs : "yes" to build and record the pTTs (default : "no")
  --Format : choose the format of recorded files : textfile : "readable", vhfile: "vh"
6) Choose to plot a layer or record the plots of all layers
  --Record_plots : yes to record all layers
                        record all layers
  --Plot PLOT           plot a layer
  --Layer LAYER         Layer to display
  --UV UV               With or without UV
  --irot IROT           With or without rot
  --Bins BINS           With or without bins
  --Record_plots RECORD_PLOTS
                        record all layers
  --S1_Input S1_INPUT   run and record the S1 numbering
  --S1S2_Mapping S1S2_MAPPING
                        run and record the S1-S2_Mapping
  --Sector SECTOR       S2 Sector
  --S1_Board S1_BOARD   S1 Board output to record
  --S2_Board S2_BOARD   S2 Board input to record
  --Create_Bins CREATE_BINS
                        create z and bins



Geometry version 
-
The results are shared into different folders, corresponding to different geometry versions.

Here are explanations of the versions currently used :


v1 --> modmap v15.5 (CMSSW v????), STCs are arbitrarily defined.

v2 --> modmap v15.5 (CMSSW v?????), STCs are the good ones for the entire modules but not good at all for the partial ones. Scintillator STCs need also some corrections

v3 --> modmap v13.1 (CMSSW 16), without the good partial module STCs and without scintilators. Module rotations are very different from the v15.5, they are the same as CMSSW 16
