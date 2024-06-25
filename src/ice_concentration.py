import numpy as np
from h5py import Dataset


def asi_hdf(
    channels: Dataset,
    P0: float = 47,
    P1: float = 11.7,
) -> np.ndarray:
    """
    P0 = 47 is the tie-point of open water;
    P1 = 11.7 is the tie-point of ice
    """
    # load channels:
    V187 = channels[:,:,2]
    #H187 = channels[:,:,3]
    V238 = channels[:,:,4]
    V36 = channels[:,:,5]
    #H36 = channels[:,:,6]
    V89 = channels[:,:,7]
    H89 = channels[:,:,8]
    # polarization difference
    P = V89-H89

    Ps = [[P0**3,P0**2,P0,1],
          [P1**3,P1**2,P1,1],
          [3*P0**3,2*P0**2,P0,0],
          [3*P1**3,2*P1**2,P1,0]]
    d = np.linalg.solve(Ps,[0,1,-1.14,-0.14]) 
    concentration = d[0]*P**3 + d[1]*P**2 + d[2]*P + d[3]
    # weather-filters, gradientRatioXY = (Vx-Vy)/(Vx+Vy)
    gradientRatio36187 = (V36-V187)/(V36+V187)
    gradientRatio238187 = (V238-V187)/(V238+V187)
    # filtering
    concentration[P<P1] = 1      
    concentration[P>P0] = 0   
    concentration[gradientRatio36187>=0.045] = 0   
    concentration[gradientRatio238187>=0.04] = 0   
    return concentration
