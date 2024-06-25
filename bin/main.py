import sys
from pathlib import Path
import hydra
import numpy as np
from omegaconf import DictConfig

from src.defs import ROOT
from src.analyze_hdf5 import PreprocessedHDF5


np.set_printoptions(linewidth=400)
np.set_printoptions(threshold=sys.maxsize)


@hydra.main(config_path=f"{ROOT}/configs", config_name="default", version_base=None)
def main(cfg: DictConfig) -> None:
    hydra_cfg = hydra.core.hydra_config.HydraConfig.get()
    out_dir = hydra_cfg.runtime.output_dir
    out_dir = Path(out_dir)

    preprocessed_hdf5 = PreprocessedHDF5(cfg)
    preprocessed_hdf5.discard_small_files()
    preprocessed_hdf5.extract_data_from_hdf5_file_pairs()
    #breakpoint()


if __name__ == "__main__":
    main()


## python -m bin.main
