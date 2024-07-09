import sys
from pathlib import Path
import hydra
import numpy as np
from omegaconf import DictConfig

from src.defs import ROOT
from src.analyze_hdf5 import PreprocessedHDF5
from src.swath_processing import Swath
from src.window_processing import Window

np.set_printoptions(linewidth=400)
np.set_printoptions(threshold=sys.maxsize)


@hydra.main(config_path=f"{ROOT}/configs", config_name="default", version_base=None)
def main(cfg: DictConfig) -> None:
    hydra_cfg = hydra.core.hydra_config.HydraConfig.get()
    out_dir = Path(hydra_cfg.runtime.output_dir)  # noqa: F841

    preprocessed_hdf5 = PreprocessedHDF5(cfg)
    track_numbers = preprocessed_hdf5.discard_small_files()
    selected_track_number = track_numbers[0]  # noqa: F841
    track_number_to_hdf5_data = (
        preprocessed_hdf5.extract_data_from_hdf5_file_pairs()
    )  # noqa: F841

    # the swath class constructor should take `cfg` and one track data like `track_number_to_hdf5_data['016156']`
    swath = Swath(
        cfg=cfg,
        one_track_data=track_number_to_hdf5_data["016156"],
        band_label="Ka",
    )
    swath.resample_ice_concentration_DPR()
    swath.create_mask()

    for window_center in swath.index_mask:
        window = Window(
            cfg=cfg,
            window_center=window_center,
            incidence_angle=[],
            sigma=[],
            mask=[],
        )

        # window = swath.select_window(window_center)
        # ^ 'numpy.ndarray' object has no attribute 'along_flight_direction'
        window.linearize()
        window.get_regression_coefs()
        swath.get_results(window)

    swath.smooth()


if __name__ == "__main__":
    main()


## python -m bin.main
