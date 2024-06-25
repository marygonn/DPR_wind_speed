from pathlib import Path

ROOT = Path(__file__).absolute().parent.parent

MIN_DPR_HDF5_FILE_SIZE_BYTES = 2 * (10 ** 6)

EXTRACT_HDF5_DATA_NAME_MAPPING = {
    "Latitude": "Latitude",
    "Longitude": "Longitude",
    "Sigma": "VER/sigmaZeroNPCorrected",
    "SecondOfDay": "ScanTime/SecondOfDay",
    "PrecipitationRate": "SLV/precipRateESurface",
    "IncidenceAngle": "PRE/localZenithAngle",
    "SurfaceType": "PRE/landSurfaceType",
}

