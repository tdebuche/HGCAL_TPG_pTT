import json
from Geometry.Programs.tools import *


    
#record two scenarios : 20*24 bins and 20*28 bins

#First scenario : 20 * 24 bins, 0 to 120 degree
def record_20_24_Bins_all_endcap():
    bin_size = "pi/36"
    nb_phibin = 24
    nb_etabin = 20
    etamin = 1.305
    etamax = etamin + np.pi *20/36
    phimin = 0 * np.pi/180
    phimax = 120 * np.pi/180
    Bins = create_Bins_all_endcap(etamin,phimin,nb_etabin,nb_phibin)
    header = {'nb_etabin' :nb_etabin,'nb_phibin' :nb_phibin,'etamin' : etamin,'etamax' :etamax,'phimin' :phimin,'phimax' :phimax,'bin_size' : bin_size}
    with open('src/all_endcap_2024_Bins.json', 'w') as recordfile:
        json.dump({'header' : header, 'Bins' : Bins }, recordfile)

def record_20_28_Bins_all_endcap():
    bin_size = "pi/36"
    nb_phibin = 28
    nb_etabin = 20
    etamin = 1.305
    etamax = etamin + np.pi *20/36
    phimin = -15 * np.pi/180
    phimax = 125 * np.pi/180
    Bins = create_Bins_all_endcap(etamin,phimin,nb_etabin,nb_phibin)
    header = {'nb_etabin' :nb_etabin,'nb_phibin' :nb_phibin,'etamin' : etamin,'etamax' :etamax,'phimin' :phimin,'phimax' :phimax,'bin_size' : bin_size}
    with open('src/all_endcap_2028_Bins.json', 'w') as recordfile:
        json.dump({'header' : header, 'Bins' : Bins }, recordfile)




    
def record_20_24_Bins():
    bin_size = "pi/36"
    nb_phibin = 24
    nb_etabin = 20
    etamin = 1.305
    etamax = etamin + np.pi *20/36
    phimin = 0 * np.pi/180
    phimax = 120 * np.pi/180
    Bins = create_Bins(etamin,phimin,nb_etabin,nb_phibin)
    header = {'nb_etabin' :nb_etabin,'nb_phibin' :nb_phibin,'etamin' : etamin,'etamax' :etamax,'phimin' :phimin,'phimax' :phimax,'bin_size' : bin_size}
    with open('src/2024_Bins.json', 'w') as recordfile:
        json.dump({'header' : header, 'Bins' : Bins }, recordfile)




#Second scenario: 20 * 28 bins, -15 to 125 degrees
def record_20_28_Bins():
    bin_size = "pi/36"
    nb_phibin = 28
    nb_etabin = 20
    etamin = 1.305
    etamax = etamin + np.pi *20/36
    phimin = -15 * np.pi/180
    phimax = 125 * np.pi/180
    Bins = create_Bins(etamin,phimin,nb_etabin,nb_phibin)
    header = {'nb_etabin' :nb_etabin,'nb_phibin' :nb_phibin,'etamin' : etamin,'etamax' :etamax,'phimin' :phimin,'phimax' :phimax,'bin_size' : bin_size}
    with open('src/2028_Bins.json', 'w') as recordfile:
        json.dump({'header' : header, 'Bins' : Bins }, recordfile)




def create_Bins(etamin,phimin,nbeta,nbphi): 
    with open('src/Z_coordinates.json','r') as file:
        Z_Layers = json.load(file)
    all_layers_Bins = []
    for layer in range(1,48):
        single_layer_Bins = []
        bin_idx = 0 
        z = Z_Layers[layer-1]['Z_coordinate']
        for phi in range(nbphi):
            for eta in range(nbeta):
                Eta_vertices,Phi_vertices = [eta * np.pi/36 + etamin,(eta+1) * np.pi/36 + etamin,(eta+1) * np.pi/36 + etamin,eta * np.pi/36 + etamin],[phi * np.pi/36  + phimin,phi * np.pi/36 + phimin,(phi+1) * np.pi/36 + phimin,(phi+1) * np.pi/36 + phimin]
                verticesX,verticesY = [],[]
                for vertex_idx in range(len(Eta_vertices)):
                    x,y = etaphitoXY(Eta_vertices[vertex_idx],Phi_vertices[vertex_idx],z)
                    verticesX.append(x)
                    verticesY.append(y)
                single_layer_Bins.append({'index' : bin_idx, 'eta_index' : eta, 'phi_index' : phi,'verticesX' : verticesX,'verticesY' : verticesY, 'Eta_vertices' : Eta_vertices,'Phi_vertices' : Phi_vertices,})
                bin_idx +=1
        all_layers_Bins.append(single_layer_Bins)
    return(all_layers_Bins)


def create_Bins_all_endcap(etamin,phimin,nbeta,nbphi):
    Bins = []
    for phi in range(72):
        for eta in range(nbeta):
            Sectors = []
            Eta_vertices,Phi_vertices = [eta * np.pi/36 + etamin,(eta+1) * np.pi/36 + etamin,(eta+1) * np.pi/36 + etamin,eta * np.pi/36 + etamin],[phi * np.pi/36 ,phi * np.pi/36,(phi+1) * np.pi/36,(phi+1) * np.pi/36 ]
            verticesX,verticesY = [],[]
            for vertex_idx in range(len(Eta_vertices)):
                x,y = etaphitoXY(Eta_vertices[vertex_idx],Phi_vertices[vertex_idx],1)
                verticesX.append(x)
                verticesY.append(y)
            S2_sector =  ((phi-6)//24)
            if S2_sector < 0 : S2_sector = 2
            S2_coordinates = {'Sector': S2_sector,  'eta_index' : eta, 'phi_index' : (phi-6)%24}
            if nbphi == 24:
                S1_coordinates =  {'eta_index' : eta, 'phi_index' : phi%24}
                nameS1coordinates  = 'S1_Sector'+str(phi//24)
                Sectors.append(phi//24)
                Bins.append({'S1_Sectors' :Sectors ,'S2_coordinates':S2_coordinates,nameS1coordinates:S1_coordinates,'verticesX' : verticesX,'verticesY' : verticesY, 'Eta_vertices' : Eta_vertices,'Phi_vertices' : Phi_vertices})
            if nbphi == 28 : 
                S1_coordinates =  {'Sector': (phi)//24,  'eta_index' : eta, 'phi_index' : phi%24 + 3}
                nameS1coordinates  = 'S1_Sector'+str(phi//24)
                Sectors.append(phi//24)
                if phi%24 == 0: 
                    nameS1coordinatesbis  = 'S1_Sector'+str((phi//24 -1)%3)
                    S1_coordinatesbis = {'eta_index' : eta, 'phi_index' : 27}
                    Sectors.append((phi//24 -1)%3)
                    Bins.append({'S1_Sectors' :Sectors , 'S2_coordinates':S2_coordinates,nameS1coordinates:S1_coordinates,nameS1coordinatesbis:S1_coordinatesbis,'verticesX' : verticesX,'verticesY' : verticesY, 'Eta_vertices' : Eta_vertices,'Phi_vertices' : Phi_vertices})
                elif phi%24 > 20: 
                    nameS1coordinatesbis  = 'S1_Sector'+str((phi//24 +1)%3)
                    S1_coordinatesbis = {'eta_index' : eta, 'phi_index' : phi%24 -21}
                    Sectors.append((phi//24 +1)%3)
                    Bins.append({'S1_Sectors' :Sectors , 'S2_coordinates':S2_coordinates,nameS1coordinates:S1_coordinates,nameS1coordinatesbis:S1_coordinatesbis,'verticesX' : verticesX,'verticesY' : verticesY, 'Eta_vertices' : Eta_vertices,'Phi_vertices' : Phi_vertices})
                else :
                    Bins.append({'S1_Sectors' :Sectors , 'S2_coordinates':S2_coordinates,nameS1coordinates:S1_coordinates,'verticesX' : verticesX,'verticesY' : verticesY, 'Eta_vertices' : Eta_vertices,'Phi_vertices' : Phi_vertices})
    return(Bins)



