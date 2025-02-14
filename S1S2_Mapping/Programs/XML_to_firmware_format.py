import xml.etree.ElementTree as ET
from collections import defaultdict
import math
import numpy as np
import awkward as ak
from S1S2_Mapping.Programs.tools  import *

# convert the xml files to txt files used by the ingeniors of Split to build the firmware

def read_S2_xml_mapping(args,file,S1_Sector):
    tree = ET.parse(file)
    root = tree.getroot()
    firmware_mapping = ''
    S1_index = 0
    #look line by line (specific xml functions to do it)
    for s1_element in root.findall('.//S1'): 
        for channel_element in s1_element.findall('.//Channel'):
            channel = int(channel_element.get('aux-id'))
            for frame_element in channel_element.findall('.//Frame'):
                if all(attr in frame_element.attrib for attr in ['id']):
                    frame  = frame_element.get('id')
                    pTT  = frame_element.get('pTT')
                    link = channel//2
                    if link == 0 or link == 1 :
                        Sector_link = (S1_Sector + 2)%3
                    else :
                        Sector_link = S1_Sector
                    if pTT:
                        pTT_Sector,S1Board,eta,phi,CEECEH = get_pTT_numbers(pTT) #find the info on pTT
                        if CEECEH == 0 : CEECEH = "CE-E"
                        if CEECEH == 1 : CEECEH = "CE-H"
                        #if S1_index != S1Board: print("error in stage 1 board : from pTT board "+str(S1Board)+"from xml board "+str(S1_index)+'pTT '+pTT) #check if the pTT S1board matches with the link S1Board 
                        #add the line with all the info
                        firmware_mapping += "S1_Sector="+str(Sector_link)+", S2_board="+str(args.S2_Board)+', Frame id = "'+frame+'", Link='+str(channel//2)+', Word='+str(channel%2)+', pTT : S1_Board='+str(S1Board)+', eta='+str(eta)+', phi='+str(phi)+', '+ CEECEH +'\n'
                    if not pTT:
                        #when the frame is empty, we fill the line with S1Board=99, eta=99 and phi=99
                        if (channel > 1 and channel < 10 and ((channel//2-1)%2 ==0)) or (channel < 2): CEECEH = "CE-E"
                        if (channel > 1 and channel < 10 and ((channel//2-1)%2 ==1)) or (channel > 9): CEECEH = "CE-H"
                        firmware_mapping += "S1_Sector="+str(Sector_link)+", S2_board="+str(args.S2_Board)+', Frame id = "'+frame+'", Link='+str(channel//2)+', Word='+str(channel%2)+', pTT : S1_Board=99, eta=99, phi=99, '+CEECEH +'\n'
        S1_index += 1
    return firmware_mapping


def read_S1_xml_mapping(args,file,S2_Sector):
    tree = ET.parse(file)
    root = tree.getroot()
    firmware_mapping = ''
    S2_index = 0
    #look line by line (specific xml functions to do it)
    for s2_element in root.findall('.//S2'):
        S2_index = int(s2_element.get('id'),16) >> 16 & 0x3F

        for channel_element in s2_element.findall('.//Channel'):
            channel = int(channel_element.get('aux-id'))
            for frame_element in channel_element.findall('.//Frame'):
                if all(attr in frame_element.attrib for attr in ['id']):
                    frame  = frame_element.get('id')
                    pTT  = frame_element.get('pTT')
                    link = channel//2
                    if link == 0 or link == 1 :
                        Sector_link = (S2_Sector + 2)%3
                    else :
                        Sector_link = S2_Sector
                    if pTT:
                        pTT_Sector,S1Board,eta,phi,CEECEH = get_pTT_numbers(pTT) #find the info on pTT
                        if args.S1_Board != S1Board: print("error in stage 1 board : from pTT board "+str(S1Board)+"from args "+str(args.S1_Board)+'pTT '+pTT) #check if the pTT S1board matches with the link S1Board 
                        if CEECEH == 0 : CEECEH = "CE-E"
                        if CEECEH == 1 : CEECEH = "CE-H"
                        #add the line with all the info
                        firmware_mapping += "S2_Sector="+str(Sector_link)+", S2_board="+str(S2_index)+', Frame id = "'+frame+'", Link='+str(channel//2)+', Word='+str(channel%2)+', pTT : S1_Board='+str(S1Board)+', eta='+str(eta)+', phi='+str(phi)+', '+ CEECEH +'\n'
                    if not pTT:
                        #when the frame is empty, we fill the line with S1Board=99, eta=99 and phi=99
                        if (channel > 1 and channel < 10 and ((channel//2-1)%2 ==0)) or (channel < 2): CEECEH = "CE-E"
                        if (channel > 1 and channel < 10 and ((channel//2-1)%2 ==1)) or (channel > 9): CEECEH = "CE-H"
                        firmware_mapping += "S2_Sector="+str(Sector_link)+", S2_board="+str(S2_index)+', Frame id = "'+frame+'", Link='+str(channel//2)+', Word='+str(channel%2)+', pTT : S1_Board='+str(args.S1_Board)+', eta=99, phi=99, '+CEECEH +'\n'
    return firmware_mapping

def record_pTT_firmware_mapping(args):
    S2_firmware_mapping = ""
    if args.nb_bins== 30:
        path = 'S1S2_Mapping/Results/S2_Mapping/30_Phi_Bins/Sector'+str(args.Sector)
    if args.nb_bins== 28:
        path = 'S1S2_Mapping/Results/S2_Mapping/28_Phi_Bins/Sector'+str(args.Sector)
    if args.nb_bins== 24:
        path = 'S1S2_Mapping/Results/S2_Mapping/24_Phi_Bins/Sector'+str(args.Sector)
    S1_Sector = args.Sector
    S2_firmware_mapping += read_S2_xml_mapping(args,path+'/Allocation.xml',S1_Sector)

    S1_Sector = (args.Sector+1)%3  
    if args.nb_bins== 28:
        path = 'S1S2_Mapping/Results/S2_Mapping/28_Phi_Bins/Sector'+str(args.Sector) 
        S2_firmware_mapping += read_S2_xml_mapping(args,path+'/Duplication.xml',S1_Sector)
    if args.nb_bins== 24:
        path = 'S1S2_Mapping/Results/S2_Mapping/24_Phi_Bins/Sector'+str(args.Sector)
        S2_firmware_mapping += read_S2_xml_mapping(args,path+'/Duplication.xml',S1_Sector)

    
    
    file = open(path+"/S2_Sector"+str(args.Sector)+"_S2_Board"+str(args.S2_Board)+".txt", "w")
    file.write(S2_firmware_mapping)
    file.close()

    S1_firmware_mapping = ""
    if args.nb_bins== 30:
        path = 'S1S2_Mapping/Results/S1_Mapping/30_Phi_Bins/Sector'+str(args.Sector)
    if args.nb_bins== 28:
        path = 'S1S2_Mapping/Results/S1_Mapping/28_Phi_Bins/Sector'+str(args.Sector)
    if args.nb_bins== 24:
        path = 'S1S2_Mapping/Results/S1_Mapping/24_Phi_Bins/Sector'+str(args.Sector)
    S2_Sector = args.Sector
    S1_firmware_mapping += read_S1_xml_mapping(args,path+'/Allocation.xml',S2_Sector)
    
    S2_Sector = (args.Sector-1)%3
    if args.nb_bins== 28:
        path = 'S1S2_Mapping/Results/S1_Mapping/28_Phi_Bins/Sector'+str(args.Sector) 
        S1_firmware_mapping += read_S1_xml_mapping(args,path+'/Duplication.xml',S1_Sector)
    if args.nb_bins== 24:
        path = 'S1S2_Mapping/Results/S1_Mapping/24_Phi_Bins/Sector'+str(args.Sector)
        S1_firmware_mapping += read_S1_xml_mapping(args,path+'/Duplication.xml',S2_Sector)

    
    file = open(path+"/S1_Sector"+str(args.Sector)+"_S1_Board"+str(args.S1_Board)+".txt", "w")
    file.write(S1_firmware_mapping)
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
