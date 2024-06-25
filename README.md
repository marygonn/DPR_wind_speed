# DPR_wind_speed
The code performs calculation of wind speed from normalized radar cross-section data of Dual-Frequency Precipitation Radar onboard Global Precipitation Measurement satellite.

## Getting started

1. Download / copy the HDF5 files to the current directory. You can get test data (10 pairs of HDF5 files) [here](https://cloud.mail.ru/public/1nYa/M7Er1LA8h). You will have a directory structure that may look like this:

```
./
└── hdf5/
    ├── raw_DPR/
    │   └── 201701/
    │       ├── GPMCOR_DPR_1701010208_0341_016156_L2S_DD2_05A.h5
    │       ├── GPMCOR_DPR_1701010208_0341_016157_L2S_DD2_05A.h5
    │       ├── ...
    │       └── GPMCOR_DPR_1701011602_1734_016165_L2S_DD2_05A.h5
    └── raw_GMI/
        └── 201701/
            ├── 1C-R.GPM.GMI.XCAL2016-C.20170101-S020858-E034131.016156.V05A.HDF5
            ├── 1C-R.GPM.GMI.XCAL2016-C.20170101-S034132-E051405.016157.V05A.HDF5
            ├── ...
            └── 1C-R.GPM.GMI.XCAL2016-C.20170101-S160206-E173440.016165.V05A.HDF5
```

2. Specify the corresponding file path (file name) patterns in the [config file](configs/default.yaml):

```yaml
input_HDF5_files:
  DPR:
    fpaths_pattern: "./hdf5/raw_DPR/201701/GPMCOR_DPR*"
    ...
  GMI:
    fpaths_pattern: "./hdf5/raw_GMI/201701/1C-R*"
    ...
```

3. Build and start the docker container if needed:

```bash
docker build -t dpr_wind_speed .
docker run --init -it --rm -v $(pwd):/root/dpr_wind_speed --name dpr_wind_speed dpr_wind_speed
```

4. Run the script `main.py` (inside the container):
```bash
python -m bin.main
```

