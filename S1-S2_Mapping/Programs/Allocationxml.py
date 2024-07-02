from S1-S2_Mapping.Programs import *


def fill_channel(args,CEECEH,phi_min,phi_max,eta_min,eta_max):
    channel = ''
    frame = 0 
    for eta in range(eta_min,eta_max+1):
        for phi in range(phi_max,phi_min-1,-1):
            t = tower(Boards[i],eta,phi,CEECEH,args.Sector)
            channel += '\t\t\t'+'<Frame id="'+str(frame).zfill(3)+'"  pTT="'+ t+'" />' +'\n'
            frame +=1
        if args.Edges == "no" or phi < 97:
            channel += '\t\t\t'+'<Frame id="'+str(frame).zfill(3)+'" />'+'\n'
            frame +=1
    for empty_frame in range(frame,108):
        channel += '\t\t\t'+'<Frame id="'+str(empty_frame).zfill(3)+'" />'+'\n'
    return channel

def create_4_links_allocation(args):
    mapping = '<pTT_Allocation S2_Sector='+str(args.Sector)+' S2_Board='+str(args.S2_Board)+'>'+'\n'
    Boards = [S1ID(Sector,board) for board in range(14)]
    for board_idx in range(len(Boards)):
        mapping +=  '\t'+ '<S1 id="'+Boards[i]+'">'+'\n'
        for link in range(4):
            for word in range(2):
                mapping += '\t'+'\t' +'<Channel id="'+ channel(Boards[board_idx],link,word,args)+'" aux-id="'+ str(j*2+k)+'">'+'\n'
                eta_min,eta_max = 10*(k%2),10*(k%2 + 1) -1
                if link // 2 == 0 and args.Edges == "yes":
                    phi_min,phi_max = 18,27
                if link // 2 == 1 and args.Edges == "yes":
                   phi_min,phi_max= 9,17
                if link // 2 == 0 and args.Edges == "no":
                    phi_min,phi_max = 15,23
                if link // 2 == 1 and args.Edges == "no":
                    phi_min,phi_max = 6,14
                mapping += fill_channel(args,link % 2,phi_min,phi_max,eta_min,eta_max)
                mapping +=  '\t\t'+'</Channel>'+'\n'
        mapping +=  '\t'+'</S1>'+'\n'
    mapping += '</pTT_Allocation>'+'\n'
    return mapping

def create_2_links_allocation(args):
    mapping = '<pTT_Duplication S2_Sector='+str(args.Sector)+' S2_Board='+str(args.S2_Board)+'>'+'\n'
    Boards = [S1ID(Sector,board) for board in range(14)]
    mapping = ''
    for board_idx in range(len(Boards)):
        mapping +=  '\t'+ '<S1 id="'+Boards[i]+'">'+'\n'
        for link in range(2):
            for word in range(2):
                mapping += '\t'+'\t' +'<Channel id="'+ channel(Boards[board_idx],link,word,args)+'" aux-id="'+ str(j*2+k)+'">'+'\n'
                eta_min,eta_max = 10*(k%2),10*(k%2 + 1) -1
                if args.Edges == "yes":
                   phi_min,phi_max= 0,8
                if args.Edges == "no":
                    phi_min,phi_max = 0,6
                mapping += fill_channel(args,link % 2,phi_min,phi_max,eta_min,eta_max)
                mapping +=  '\t\t'+'</Channel>'+'\n'
        mapping +=  '\t'+'</S1>'+'\n'
    mapping += '</pTT_Duplication>'+'\n'
    return mapping

def record_mapping(args):
    path = 'S1-S2_Mapping/Results'
    if args.Edges == 'yes':
        path += '/28_Phi_Bins/'
    if args.Edges == 'no':
        path += '/24_Phi_Bins/'
    file = open("AllocationpTTsNoEdges.xml", "w")
    text = create_4_links_allocation(args)
    file.write(text)
    file.close()
    file = open("DuplicationpTTsEdges.xml", "w")
    text = create_2_links_allocation(args)
    file.write(text)
    file.close()







