from pathlib import Path

ROOT = Path(__file__).absolute().parent.parent

MIN_DPR_HDF5_FILE_SIZE_BYTES = 2 * (10 ** 6)

EXTRACT_HDF5_DATA_NAME_MAPPING = {
    "latitude": "Latitude",
    "longitude": "Longitude",
    "sigma": "VER/sigmaZeroNPCorrected",
    "second_of_day": "ScanTime/SecondOfDay",
    "precipitation_rate": "SLV/precipRateESurface",
    "incidence_angle": "PRE/localZenithAngle",
    "surface_type": "PRE/landSurfaceType",
}

