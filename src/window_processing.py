from omegaconf import DictConfig
import numpy as np
from typing import Any


class Window:
    def __init__(
        self,
        cfg: DictConfig,
        window_center: Any,
        incidence_angle: Any,
        sigma: Any,
        mask: np.ndarray,
    ):
        self.cfg = cfg

    def linearize(
        self,
    ):
        pass

    def get_regression_coefs(
        self,
    ):
        pass
