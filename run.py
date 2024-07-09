
import argparse
from pTTs.Programs.pTTs_to_file import record_all_boards
from S1_Input.Programs.record_text import record_input
from Geometry.Programs.plot import plot_layer
from Geometry.Programs.plot import record_all_layers
from S1S2_Mapping.Programs.S2_pTT_Mapping import record_S2_mapping
from S1S2_Mapping.Programs.S1_pTT_Mapping import record_S1_mapping
from S1S2_Mapping.Programs.S2_XML_to_firmware_format import record_pTT_firmware_mapping,record_TC_firmware_mapping
from Geometry.Programs.Z_coordinate import create_Z_coordinates
from Geometry.Programs.create_Bins import record_20_24_Bins,record_20_28_Bins,record_20_24_Bins_all_endcap,record_20_28_Bins_all_endcap

#record pTTs

parser = argparse.ArgumentParser()

#Modmap version
parser.add_argument("--Modmap_version",default = 'v13.1', help="Geometry version")

#pTT version 
parser.add_argument("--pTT_version",default = 'v3', help="Geometry version")

#Scenario
parser.add_argument("--STCs",default = 'yes', help="With (yes) or without STCs (no)")
parser.add_argument("--Edges",default = 'no', help="With (yes) or without edges(no)")

#Build and record pTTs
parser.add_argument("--pTTs",default = 'no', help="build and record the pTTs")
parser.add_argument("--Format",default = 'readable', help="textfile : readable, vhfile: vh")

#Plot a layer 
parser.add_argument("--Plot",default = 'no', help="plot a layer")
parser.add_argument("--Layer", default = 1 ,help="Layer to display",type=int)
parser.add_argument("--UV",default = 'no', help="With or without UV")
parser.add_argument("--irot",default = 'no', help="With or without rot")
parser.add_argument("--Bins",default = 'no', help="With or without bins")

#Record plots 
parser.add_argument("--Record_plots",default = 'no', help="record all layers")

#S1_Input
parser.add_argument("--S1_Input",default = 'no', help="run and record the S1 numbering")

#S1-S2_Mapping
parser.add_argument("--S1S2_Mapping",default = 'no', help="run and record the S1-S2_Mapping")
parser.add_argument("--Sector", default = 0 ,help="S2 Sector",type=int)
parser.add_argument("--S2_Board", default = 0 ,help="S2 Board input to record",type=int)

#create z coordinates and bins
parser.add_argument("--Create_Bins",default = 'no', help="create z and bins")

args = parser.parse_args()

#create Bins and Z coordinates
if args.Create_Bins == "yes":
  create_Z_coordinates()
  record_20_24_Bins()
  record_20_28_Bins()
  record_20_24_Bins_all_endcap()
  record_20_28_Bins_all_endcap()



  
#Build and record files to build pTTs
if args.pTTs == "yes":
  record_all_boards(args)


#create and record the S1 numbering
if args.S1_Input == "yes":
  record_input(args)

#plot Layer
if args.Plot == "yes":
  plot_layer(args,args.Layer)

#Record plots of all layer
if args.Record_plots == "yes":
  record_all_layers(args)


#S1-S2 mapping
if args.S1S2_Mapping == "yes":
  record_S1_mapping(args)
  record_S2_mapping(args)
  record_pTT_firmware_mapping(args)
  record_TC_firmware_mapping(args)





