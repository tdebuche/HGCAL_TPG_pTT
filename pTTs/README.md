Programs :

Energy_sharing --> python tools to create the energy sharing for one layer, for different scenarios (with/without edges, with/without STCs)

pTTs_to_file   --> programs to record 14*2 files for a given scenario. Files can be vh or readable (text) files. 

tools          --> some geometric tools used by the Energy_sharing programs

Results :


In each version, you can create readable/ vh files, in different scenarios.
vh files are used to develop the firmware. Readable files are used for simulations (repository : S1-S2_interface_test)

v1 --> modmap v15.5 (CMSSW v????), STCs are arbitrarily defined. 

v2 --> modmap v15.5 (CMSSW v?????), STCs are the good ones for the  entire modules but not good at all for the partial ones. Scintillator STCs need also some corrections

v3 --> Modmap v13.1 (CMSSW v16), STCs are the good ones for the  entire modules but not good at all for the partial ones. NO SCINTILLATOR in this modmap
