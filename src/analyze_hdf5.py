from pathlib import Path
import h5py
import numpy as np
import glob
from omegaconf import DictConfig
from loguru import logger


from .annotation import DprGmiFilePair
from .defs import MIN_DPR_HDF5_FILE_SIZE_BYTES, EXTRACT_HDF5_DATA_NAME_MAPPING
from .utils import extract_required_fnames_part
from .ice_concentration import asi_hdf


class PreprocessedHDF5:
    """
    A class representing a series of preprocessed HDF5 files (or file pairs).
    """
    def __init__(
        self,
        cfg: DictConfig,
    ) -> None:
        """
        Find the DPR-GMI pairs of files.
        """
        self.cfg = cfg

        DPR_fpaths = glob.glob(cfg.input_HDF5_files.DPR.fpaths_pattern)
        if not DPR_fpaths:
            raise FileNotFoundError("No DPR HDF5 files matching the specified pattern found")
        
        DPR_track_number_to_fpath = extract_required_fnames_part(
            fpaths=DPR_fpaths,
            delimiter=cfg.input_HDF5_files.DPR.fname_parts_delimiter,
            part_name_idx=cfg.input_HDF5_files.DPR.track_number_part_idx,
        )

        GMI_fpaths = glob.glob(cfg.input_HDF5_files.GMI.fpaths_pattern)
        if not GMI_fpaths:
            raise FileNotFoundError("No GMI HDF5 files matching the specified pattern found")

        GMI_track_number_to_fpath = extract_required_fnames_part(
            fpaths=GMI_fpaths,
            delimiter=cfg.input_HDF5_files.GMI.fname_parts_delimiter,
            part_name_idx=cfg.input_HDF5_files.GMI.track_number_part_idx,
        )

        common_track_numbers = sorted(
            set(DPR_track_number_to_fpath) & set(GMI_track_number_to_fpath)
        )
        logger.debug(f"{common_track_numbers=}")
        if not common_track_numbers:
            raise ValueError(
                "No common track numbers between DPR and GMI HDF5 files"
            )

        self._track_number_to_DPR_GMI_fpath_pair = {
            track_number: DprGmiFilePair(
                dpr_fpath=DPR_track_number_to_fpath[track_number],
                gmi_fpath=GMI_track_number_to_fpath[track_number],
            )
            for track_number in common_track_numbers
        }
        # ^ regardless of the file sizes

    def discard_small_files(
        self,
    ) -> None:
        """
        Discard the DPR-GMI HDF5 file pairs for which the DPR file
        is unexpectedly small.
        """
        track_numbers_to_exclude = []

        for track_number, fpath_pair in self._track_number_to_DPR_GMI_fpath_pair.items():
            DPR_fpath = fpath_pair[0]
            if DPR_fpath.stat().st_size < MIN_DPR_HDF5_FILE_SIZE_BYTES:
                track_numbers_to_exclude.append(track_number)
        
        if track_numbers_to_exclude:
            logger.debug(f"{track_numbers_to_exclude=} (filtered out by file size)")
        
        self.track_number_to_DPR_GMI_fpath_pair = {
            track_number: fpath_pair
            for track_number, fpath_pair in self._track_number_to_DPR_GMI_fpath_pair.items()
            if track_number not in track_numbers_to_exclude
        }
        if not self.track_number_to_DPR_GMI_fpath_pair:
            raise ValueError(
                "No DPR-GMI HDF5 file pairs left after filtering by size"
                " (the DPR files are unexpectedly small)"
            )

    def extract_data_from_hdf5_file_pairs(
        self,
    ) -> None:
        self.track_number_to_extracted_data = {
            track_number: self.extract_data_from_one_hdf5_file_pair(fpath_pair)
            for track_number, fpath_pair in self.track_number_to_DPR_GMI_fpath_pair.items()
        }


    def extract_data_from_one_hdf5_file_pair(
        self,
        hdf5_fpath_pair: tuple[Path, Path],
    ) -> None:
        dpr_file_content = h5py.File(hdf5_fpath_pair.dpr_fpath, 'r')
        gmi_file_content = h5py.File(hdf5_fpath_pair.gmi_fpath, 'r')

        self.hdf5_data = {}
        if self.cfg.input_HDF5_files.ice:
            self.hdf5_data['LatitudeGMI'] = np.array(gmi_file_content['S1/Latitude'])
            self.hdf5_data['LongitudeGMI'] = np.array(gmi_file_content['S1/Longitude'])
            self.hdf5_data['IceConcentrationGMI'] = asi_hdf(gmi_file_content['S1/Tc'])
        else:
            self.hdf5_data['LatitudeGMI'] = np.asarray([])
            self.hdf5_data['LongitudeGMI'] = np.asarray([])
            self.hdf5_data['IceConcentrationGMI'] = np.asarray([])

        band_label = (
            'NS'
            if self.cfg.HDF5_data_processing.use_Ka
            else 'MS'
        )
        for short_name, hdf5_name_part in EXTRACT_HDF5_DATA_NAME_MAPPING.items():
            self.hdf5_data[short_name] = np.array(dpr_file_content[f'/{band_label}/{hdf5_name_part}'])
