import xml.etree.ElementTree as ET
from collections import defaultdict
import math
import numpy as np
import awkward as ak
from S1S2_Mapping.Programs.tools  import *

def record_pTT_firmware_mapping(args):
    if args.Edges == 'yes':
        path = 'S1S2_Mapping/Results/28_Phi_Bins/'
    if args.Edges == 'no':
        path = 'S1S2_Mapping/Results/24_Phi_Bins/'
        
    tree = ET.parse(path+'Allocation.xml')
    root = tree.getroot()
    firmware_mapping = ''
    S1_index = 0
    for s1_element in root.findall('.//S1'):
        for channel_element in s1_element.findall('.//Channel'):
            channel = int(channel_element.get('aux-id'))
            for frame_element in channel_element.findall('.//Frame'):
                if all(attr in frame_element.attrib for attr in ['id']):
                    frame  = frame_element.get('id')
                    pTT  = frame_element.get('pTT')
                    if pTT:
                        pTT_Sector,S1Board,eta,phi,CEECEH = get_pTT_numbers(pTT)
                        if CEECEH == 0 : CEECEH = "CE-E"
                        if CEECEH == 1 : CEECEH = "CE-H"
                        firmware_mapping += "Sector="+str(args.Sector)+", S2_board="+str(args.S2_Board)+', Frame id = "'+frame+'", Link='+str(channel//2)+', Word='+str(channel%2)+', pTT : S1_Board='+str(S1Board)+', eta='+str(eta)+', phi='+str(phi)+', '+ CEECEH +'\n'
                        if S1_index != S1Board: print("error")
                    if not pTT:
                        firmware_mapping += "Sector="+str(args.Sector)+", S2_board="+str(args.S2_Board)+', Frame id = "'+frame+'", Link='+str(channel//2)+', Word='+str(channel%2)+', pTT : S1_Board=99, eta=99, phi=99, CE-E' +'\n'
                    
        S1_index += 1
    file = open(path+"For_Toni.txt", "w")
    file.write(firmware_mapping)
    file.close()

def record_TC_firmware_mapping(args):
    tree = ET.parse('src/S1.ChannelAllocation.xml')
    root = tree.getroot()
    firmware_mapping = ''
    S1_index = 0
    for s1_element in root.findall('.//S1'):
        for channel_element in s1_element.findall('.//Channel'):
            channel = int(channel_element.get('aux-id'))
            for frame_element in channel_element.findall('.//Frame'):
                if all(attr in frame_element.attrib for attr in ['id']):
                    frame  = frame_element.get('id')
                    module  = frame_element.get('Module')
                    index  = frame_element.get('index')
                    if module:
                        firmware_mapping += "Sector="+str(args.Sector)+", S2_board="+str(args.S2_Board)+', Frame id = "'+frame+'", Link='+str(channel//3)+', Word='+str(channel%3)+', TC : Module='+module+', index='+index+'\n'
                    if not module:
                        firmware_mapping += "Sector="+str(args.Sector)+", S2_board="+str(args.S2_Board)+', Frame id = "'+frame+'", Link='+str(channel//3)+', Word='+str(channel%3)+', TC : Module='+str(9999)+', index='+str(9999)+'\n'
                    
        S1_index += 1
    file = open("S1S2_Mapping/Results/TC_Mapping.txt", "w")
    file.write(firmware_mapping)
    file.close()
