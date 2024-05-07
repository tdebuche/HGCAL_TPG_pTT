import numpy as np
import matplotlib.pyplot as plt
import os
import json
import shapely.geometry
from shapely.geometry import Polygon
from prelim import etaphitoXY
from prelim import etaphiRADtoXY
from prelim import XYtoetaphi
from prelim import polygontopoints
from prelim import pointtopolygon
from prelim import binetaphitoXY
from prelim import binetaphiRADtoXY
from prelim import etaphicentre
from prelim import ModulestoSommets
from prelim import BintoBinSommets
from prelim import STCtoSTCSommets
from STCtoPTT import pTTSTCs
from ModuleSumtoPTT import pTTModules
from PTT import PTTarray

os.chdir("C:/Users/Thomas de L'Epinois/Desktop/StageCMS/Mapping/pTT/Ressources")

UV = np.load('uv.npy')
Binetaphi = np.load('Binetaphi.npy')
G = np.load('Geometry.npy')
Z = np.load('Z.npy')
STCLD = np.load('STCLD.npy')
STCHD = np.load('STCHD.npy')
etamin = 1.305
N = 16


def saveModules(title):
    listmodules = []
    for lay in range(34):
        if lay < 13:
            Layer = lay *2 +1
        else :
            Layer = lay + 14
        Modules = G[Layer-1]
        uv = UV[Layer-1]
        z = Z[Layer-1]
        for i in range(len(Modules)):
            mod = Modules[i]
            vertices = []
            for j in range(len(mod[0])):
                if mod[0][j] != 0 or mod[1][j] != 0:
                    vertices.append((mod[0][j],mod[1][j]))
            if vertices != []:
                hexapolygon = Polygon(vertices)
                feature_module = {
                'type': 'Feature',
                'geometry': shapely.geometry.mapping(hexapolygon),  # Convert polygon to GeoJSON geometry
                'properties': {
                    'Layer': Layer,
                    'Z_value': z,
                    'u': int(uv[i,0]),
                    'v': int(uv[i,1]),
                    }
                }
                listmodules.append(feature_module)

    feature_collection_modules = {
            'type': 'FeatureCollection',
            'features': listmodules
        }
        # Write GeoJSON data with bin_polygon geometry to file
    with open(title, 'w') as f_polygon:
        json.dump(feature_collection_modules, f_polygon, indent=4)




def saveBins(title):
    listbins = []
    for lay in range(34):
        if lay < 13:
            Layer = lay *2 +1
        else :
            Layer = lay + 14
        z = Z[Layer-1]
        BinXY= binetaphitoXY(Binetaphi,z)
        for i in range(len(BinXY)):
            bin = BinXY[i]
            vertices = []
            for j in range(len(bin[0])):
                if bin[0][j] != 0 or bin[1][j] != 0:
                    vertices.append((round(bin[0][j],1),round(bin[1][j],1)))
            if vertices != []:
                binpolygon = Polygon(vertices)
                feature_bin = {
                'type': 'Feature',
                'geometry': shapely.geometry.mapping(binpolygon),  # Convert polygon to GeoJSON geometry
                'properties': {
                    'Layer': Layer,
                    'Z_value': z,
                    'Eta': int(i%20),
                    'Phi': int(i//20),
                    }
                }
                listbins.append(feature_bin)

    feature_collection_bins = {
            'type': 'FeatureCollection',
            'features': listbins
        }
        # Write GeoJSON data with bin_polygon geometry to file
    with open(title, 'w') as f_polygon:
        json.dump(feature_collection_bins, f_polygon, indent=4)



def saveSTCs(title):
    listSTCs = []
    for lay in range(34):
        if lay > 12:
            Layer = lay + 14
            z = Z[Layer-1]
            if Layer < 34:
                STCs = STCHD[Layer-27]
            if Layer > 33:
                STCs = STCLD[Layer-34]
            uv = UV[Layer-1]
            for i in range(len(STCs)):
                for k in range(len(STCs[i])):
                    stc = STCs[i,k]
                    vertices = []
                    for j in range(len(stc[0])):
                        if stc[0][j] != 0 or stc[1][j] != 0:
                            vertices.append((round(stc[0][j],1),round(stc[1][j],1)))
                    if vertices != []:
                        stcpolygon = Polygon(vertices)
                        feature_stc = {
                        'type': 'Feature',
                        'geometry': shapely.geometry.mapping(stcpolygon),  # Convert polygon to GeoJSON geometry
                        'properties': {
                            'Layer': Layer,
                            'Z_value': z,
                            'u_module': int(uv[i,0]),
                            'v_module': int(uv[i,1]),
                            'stc_index': int(k),
                            }
                        }
                        listSTCs.append(feature_stc)

    feature_collection_STCs = {
            'type': 'FeatureCollection',
            'features': listSTCs
        }
        # Write GeoJSON data with bin_polygon geometry to file
    with open(title, 'w') as f_polygon:
        json.dump(feature_collection_STCs, f_polygon, indent=4)

saveModules('Geometry_Modules')
saveBins('Geometry_Bins')
saveSTCs('Geometry_STCs')






