import numpy as np

def countAngle(x_Coccyx,y_Coccyx,v_Coccyx,x_Head,y_Head,v_Head,x_Tail,y_Tail,v_Tail):
    k_headcocyx = (y_Coccyx - y_Head) / (x_Coccyx - x_Head)
    k_cocyxtail = (y_Tail - y_Coccyx) / (x_Tail - x_Coccyx)
    tanlines = (k_cocyxtail - k_headcocyx) / (1 + k_cocyxtail * k_headcocyx)
    radians = np.arctan(tanlines)
    degrees=np.degrees(radians)
    quality = min(v_Head, v_Coccyx, v_Tail)
    return degrees,quality


def countAngleWrapper(params):
    x_Coccyx=params['x_coccyx']
    y_Coccyx=params['y_coccyx']
    v_Coccyx=params['quality_coccyx']
    x_Head=params['x_head']
    y_Head=params['y_head']
    v_Head=params['quality_head']
    x_Tail=params['x_tail']
    y_Tail=params['y_tail']
    v_Tail=params['quality_tail']
    countAngle(x_Coccyx,y_Coccyx,v_Coccyx,x_Head,y_Head,v_Head,x_Tail,y_Tail,v_Tail)