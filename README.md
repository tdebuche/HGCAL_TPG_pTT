# HGCAL_TPG_pTT

This recovery is splitted in few parts : 
- Geometry : allows to build the bins of each layer and make plots
- PTTs : create files used to build the pTTs in the S1 boards (== energy sharing)
- S1_Input: create the numbering of modules/STCs in each board (it has to match with the S1 unpacker). The same numbering is used in the PTTs files
- S1-S2 Mapping : map the pTTs into links between S1 and S2 boards


Each part is divided into two folders : the first one gathers programmes, and the second one, gathers files produced by the programmes.

src gathers files used by programs (geometry of modules, STCs, bins)

