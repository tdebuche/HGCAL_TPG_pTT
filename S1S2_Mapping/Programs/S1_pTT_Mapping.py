
from S1S2_Mapping.Programs.tools  import *
Endcap = 0



def create_4_links_allocation(args):
    S1_Sector = args.Sector
    S2_Sector = args.Sector
    S1_Board = args.S1_Board
    mapping = '<pTT_Allocation S1_Sector="'+str(S1_Sector)+'" S1_Board="'+str(S1_Board)+'">'+'\n'
    Boards = [get_S2Board_id(S2_Sector,board_idx) for board_idx in range(18)]
    for S2_Board in range(len(Boards)):
        S2_Board_id = Boards[S2_Board]
        mapping +=  '\t'+ '<S2 id="'+S2_Board_id+'">'+'\n'
        for link in range(1,5):
            for word in range(2):
                mapping += '\t'+'\t' +'<Channel id="'+ get_channel_id(S1_Sector,S2_Sector,S1_Board,S2_Board,link,word)+'" aux-id="'+ str(link*2+word)+'">'+'\n'
                eta_min,eta_max = 10*(word%2),10*(word%2 + 1) -1
                if (link-1) // 2 == 0 and args.Edges == "yes":
                    phi_min,phi_max = 18,27
                if (link-1) // 2 == 1 and args.Edges == "yes":
                   phi_min,phi_max= 9,17
                if (link-1) // 2 == 0 and args.Edges == "no":
                    phi_min,phi_max = 15,23
                if (link-1) // 2 == 1 and args.Edges == "no":
                    phi_min,phi_max = 6,14
                mapping += fill_channel(args,S1_Sector,S1_Board,1-link%2,phi_min,phi_max,eta_min,eta_max)
                mapping +=  '\t\t'+'</Channel>'+'\n'
        mapping +=  '\t'+'</S2>'+'\n'
    mapping += '</pTT_Allocation>'+'\n'
    return mapping

def create_2_links_allocation(args):
    S1_Sector = args.Sector
    S2_Sector = (args.Sector-1)%3
    S1_Board = args.S1_Board
    mapping = '<pTT_Duplication S1_Sector="'+str(S1_Sector)+'" S1_Board="'+str(S1_Board)+'">'+'\n'
    Boards = [get_S2Board_id(S2_Sector,board_idx) for board_idx in range(18)]
    for S2_Board in range(len(Boards)):
        S2_Board_id = Boards[S2_Board]
        mapping +=  '\t'+ '<S2 id="'+S2_Board_id+'">'+'\n'
        for link in range(0,6,5):
            for word in range(2):
                mapping += '\t'+'\t' +'<Channel id="'+ get_channel_id(S1_Sector,S2_Sector,S1_Board,S2_Board,link,word)+'" aux-id="'+ str(link*2+word)+'">'+'\n'
                eta_min,eta_max = 10*(word%2),10*(word%2 + 1) -1
                if args.Edges == "yes":
                   phi_min,phi_max= 0,8
                if args.Edges == "no":
                    phi_min,phi_max = 0,5
                mapping += fill_channel(args,S1_Sector,S1_Board,link % 2,phi_min,phi_max,eta_min,eta_max)
                mapping +=  '\t\t'+'</Channel>'+'\n'
        mapping +=  '\t'+'</S2>'+'\n'
    mapping += '</pTT_Duplication>'+'\n'
    return mapping
    
def fill_channel(args,S1_Sector,S1_Board,CEECEH,phi_min,phi_max,eta_min,eta_max):
    channel = ''
    frame = 0 
    for eta in range(eta_min,eta_max+1):
        for phi in range(phi_max,phi_min-1,-1):
            t = get_pTT_id(S1_Sector,S1_Board,eta,phi,CEECEH)
            channel += '\t\t\t'+'<Frame id="'+str(frame).zfill(3)+'"  pTT="'+ t+'" />' +'\n'
            frame +=1
        if args.Edges == "no" or frame < 97:
            channel += '\t\t\t'+'<Frame id="'+str(frame).zfill(3)+'" />'+'\n'
            frame +=1
    for empty_frame in range(frame,108):
        channel += '\t\t\t'+'<Frame id="'+str(empty_frame).zfill(3)+'" />'+'\n'
    return channel
    
def record_S1_mapping(args):
    path = 'S1S2_Mapping/Results/S1_Mapping'
    if args.Edges == 'yes':
        path += '/28_Phi_Bins/Sector'+str(args.Sector) +'/'
    if args.Edges == 'no':
        path += '/24_Phi_Bins/Sector'+str(args.Sector) +'/'
    file = open(path+"/Allocation.xml", "w")
    text = create_4_links_allocation(args)
    file.write(text)
    file.close()
    file = open(path+"/Duplication.xml", "w")
    text = create_2_links_allocation(args)
    file.write(text)
    file.close()
