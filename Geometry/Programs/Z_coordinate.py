import json

############################# Return a  list(47) with z for each layers ############################################################

ZlayerCEE = [3210.50,3238.87,3269.44,3300.01,3330.01,3361.15,3391.72,3422.29,3452.86,3483.43,3517.25,3551.07,3584.89,3619.71]
ZlayerCEHfine = [3665.96,3687.51,3729.01,3750.56,3792.01,3813.61,3855.11,3876.66,3918.16,3939.71,3981.21,4002.76,4044.26,4065.81,4107.31,4128.86,4170.36,4191.91,4233.41,4254.96,4296.46,4318.01]
ZlayerCEHcoarse = [4378.71,4400.26,4460.96,4482.51,4543.21,4564.76,4625.46,4647.01,4707.71,4729.26,4789.96,4811.51,4872.21,4893.76,4954.46,4976.01,5036.71,5058.26,5118.96,5140.51]


def create_Z_coordinates():
    L1,L2,L3 = ZlayerCEE,ZlayerCEHfine,ZlayerCEHcoarse
    Z = []
    layer = 1
    for i in range(len(L1)-1):
        z = (L1[i]+L1[i+1])/2
        Z.append({'Layer' : layer, 'Z_coordinate' : z})
        layer += 1
        Z.append({'Layer' : layer, 'Z_coordinate' : z})
        layer += 1
    for i in range(len(L2)//2):
        z = (L2[2*i]+L2[2*i+1])/2
        Z.append({'Layer' : layer, 'Z_coordinate' : z})
        layer += 1
    for i in range(len(L3)//2):
        z = (L3[2*i]+L3[2*i+1])/2
        Z.append({'Layer' : layer, 'Z_coordinate' : z})
        layer += 1
    with open('src/Z_coordinates.json', 'w') as recordfile:
        json.dump(Z, recordfile)
