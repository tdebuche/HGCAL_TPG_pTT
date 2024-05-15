ModuleSumtoPTT and STCtoPTT are programmes which share energies into PTTs. They return an array (for one layer) in which each module  (or STC) energy is divided in several PTTs. You don't have to run them, they will be called by the programme PTT.

The programme PTT changes the sense of the previous array. It returns an array (24,20) or (28,20) according to the scenario, and each array cell is filled with several module energy fractions. You don't have to run this programme.

The pogrammes PTTtoText_readable and PPTtoText_vhfile records (text or vh) two files the PTTs for each board . They call the previous porgramme "PTT". The "readable" version  gives for each module, its layer, its u,v coordinates (with the STC index if we work with STCs) and the fraction of energy. The "vhfile" version records the same files, but the numbering of modules in each board (this numbering has to match with the output of the S1 unpacker) replaces the (Layer,u,v) numbering.
There are several options : Board, with or without STCs, with or wihtout edges. If thhe last option "--Record" is yes, the programme will record the two files for each board (so 28 files) in the good directory (in this case, the option board becomes irrelevant). 



