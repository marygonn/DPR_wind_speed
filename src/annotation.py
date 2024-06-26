from pathlib import Path
from typing import NamedTuple, Optional
import numpy as np


class DprGmiFilePair(NamedTuple):
    dpr_fpath: Path
    gmi_fpath: Path


class OneBandData(NamedTuple):
    latitude: np.ndarray
    longitude: np.ndarray
    sigma: np.ndarray
    second_of_day: np.ndarray
    precipitation_rate: np.ndarray
    incidence_angle: np.ndarray
    surface_type: np.ndarray


class ExtractedHDF5Data(NamedTuple):
    latitude_GMI: np.ndarray
    longitude_GMI: np.ndarray
    ice_concentration_GMI: np.ndarray
    Ka: Optional[OneBandData] = None
    Ku: Optional[OneBandData] = None
