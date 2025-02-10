
from S1S2_Mapping.Programs.tools  import *
Endcap = 0


def fill_channel(args,S1_Sector,S1_Board,link,CEECEH):
    channel = ''
    frame = 0 
    if link > 1:
        phi_min,phi_max = link *5,link *5 + 4
    if link == 0:
        phi_min,phi_max = 1,5
    if link == 1:
        phi_min,phi_max = 6,9

    for phi in range(phi_min,phi_max+1):
        for eta in range(0,20):
            t = get_pTT_id(S1_Sector,S1_Board,eta,phi,CEECEH)
            channel += '\t\t\t'+'<Frame id="'+str(frame).zfill(3)+'"  pTT="'+ t+'" />' +'\n'
            frame +=1
    if link == 1:
        for eta in range(0,20):
            phi = 0
            t = get_pTT_id(S1_Sector,S1_Board,eta,phi,CEECEH)
            channel += '\t\t\t'+'<Frame id="'+str(frame).zfill(3)+'"  pTT="'+ t+'" />' +'\n'
            frame +=1
    for empty_frame in range(frame,108):
        channel += '\t\t\t'+'<Frame id="'+str(empty_frame).zfill(3)+'" />'+'\n'
    return channel
    

def create_6_links_allocation(args):
    S1_Sector = args.Sector
    S1_Board = args.S1_Board
    mapping = '<pTT_Allocation S1_Sector="'+str(S1_Sector)+'" S1_Board="'+str(S1_Board)+'">'+'\n'

    # Duplication links = links 0 and 1 (to another sector)
    S2_Sector = (args.Sector+2)%3
    Boards = [get_S2Board_id(S2_Sector,board_idx) for board_idx in range(18)]

    for S2_Board in range(len(Boards)):
        S2_Board_id = Boards[S2_Board]
        mapping +=  '\t'+ '<S2 id="'+S2_Board_id+'">'+'\n'
        for link in range(0,2):
            for word in range(2):
                mapping += '\t'+'\t' +'<Channel id="'+ get_channel_id(S1_Sector,S2_Sector,S1_Board,S2_Board,link,word)+'" aux-id="'+ str(link*2+word)+'">'+'\n'
                mapping += fill_channel(args,S1_Sector,S1_Board,link,word % 2)
                mapping +=  '\t\t'+'</Channel>'+'\n'
        mapping +=  '\t'+'</S2>'+'\n'


    # Direct links = links 2 to 5
    S2_Sector = args.Sector
    Boards = [get_S2Board_id(S2_Sector,board_idx) for board_idx in range(18)]

    for S2_Board in range(len(Boards)):
        S2_Board_id = Boards[S2_Board]
        mapping +=  '\t'+ '<S2 id="'+S2_Board_id+'">'+'\n'
        for link in range(2,6):
            for word in range(2):
                mapping += '\t'+'\t' +'<Channel id="'+ get_channel_id(S1_Sector,S2_Sector,S1_Board,S2_Board,link,word)+'" aux-id="'+ str(link*2+word)+'">'+'\n'
                mapping += fill_channel(args,S1_Sector,S1_Board,link,word % 2)
                mapping +=  '\t\t'+'</Channel>'+'\n'
        mapping +=  '\t'+'</S2>'+'\n'

    mapping += '</pTT_Allocation>'+'\n'
    return mapping


#record the mappings

def record_S1_mappingNEW(args):
    path = 'S1S2_Mapping/Results/S1_Mapping'
    if args.nb_bins== 30:
        path += '/30_Phi_Bins/Sector'+str(args.Sector) +'/'
    file = open(path+"Allocation.xml", "w")
    text = create_6_links_allocation(args)
    file.write(text)
    file.close()


