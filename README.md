# HGCAL_TPG_pTT

This recovery allows one to produce the mappings used in the pTT part of the Stage 1 : 
- Energy mapping for the pTT building
- Stage 1 input mapping (pTT part)
- pTT mapping into the Stage 1/Stage 2 optical links

This recovery is splitted in few parts : 
- Geometry : build the bins (pTT coordinates) of each layer and make some plots
- pTTs : create mapping files used to build the pTTs in the S1 boards
- S1_Input : to create the numbering of modules/STCs in each board (it has to match with the S1 unpacker). The same numbering is used in the pTTs files
- S1-S2 Mapping : map the pTTs into links between S1 and S2 boards
- src : gather files used by programs (geometry of modules, STCs, bins)

Each folder is divided into two folders : the first one gathers programmes, and the second one gathers the files produced by the programs. In each folder, there is a README to present each program.


The program "run" allows one to run every program of this repository
-

This program has many arguments to know which program has to run with which conditions. 

1) Geometry version and pTT version

  --Modmap_version : Geometry version (default : 'v13.1')
  
  --pTT_version : pTT version depending on the geometry version and some other updates (default : 'v3' which corresponds to the geometry 'v13.1')
  
  
2) Choose the scenario

  --STCs : With (yes) or without STCs (no)
  
  --Edges  : With (yes) or without edges(no) --> choose 20 * 28 or 20 * 24 pTTs per sector
  
  
3) Choose to create and record the energy mapping
   
  --pTTs : "yes" to build and record the pTTs (default : "no")
  
  --Format : choose the format of recorded files : textfile : "readable", vhfile: "vh"
  
  
4) Choose to plot a layer or record the plots of all layers

  --Record_plots : "yes" to record all layers
  
  --Plot : "yes" to plot a layer
  
  --Layer : Layer to display
  
  --UV : With or without UV
  
  --irot : With or without rot
  
  --Bins : With or without bins


5) Choose to create and record the S1_input numbering

  --S1_Input : "yes" to run and record the S1 numbering


6) Choose to create and record the pTT mapping in links between Stage 1 and Stage 2

  --S1S2_Mapping : "yes" to run and record the S1-S2_Mapping
  
  --S1_Board : "yes" to record the S1 Board output mappings
  
  --S2_Board : "yes" to recordd the S2 Board input mappings
  
  --Sector : choose the Sector (Stage 1 sector if S1_Board mapping, Stage 1 sector if S2_Board mapping)
  

7) Choose to create geometry

  --Create_Bins : "yes" to create z coordinates and bins



Geometry version 
-
The results are shared into different folders, corresponding to different geometry versions.

Here are explanations of the versions currently used :


v1 --> modmap v15.5 (CMSSW v????), STCs are arbitrarily defined.

v2 --> modmap v15.5 (CMSSW v?????), STCs are the good ones for the entire modules but not good at all for the partial ones. Scintillator STCs need also some corrections

v3 --> modmap v13.1 (CMSSW 16), without the good partial module STCs and without scintilators. Module rotations are very different from the v15.5, they are the same as CMSSW 16
