from omegaconf import DictConfig
from .annotation import ExtractedHDF5Data
from .defs import FILL_VALUE_RESAMPLE, INFLUENCE_RADIUS, EPSILON_RESAMPLE
from pyresample import kd_tree, geometry
from .window_processing import Window

import numpy as np
from typing import Any


class Swath:
    def __init__(
        self,
        cfg: DictConfig,
        one_track_data: ExtractedHDF5Data,
        band_label: str,
    ):
        self.cfg = cfg
        self.one_track_data = one_track_data
        self.chosen_band_data = (
            one_track_data.Ka if band_label == "Ka" else one_track_data.Ku
        )

    def resample_ice_concentration_DPR(
        self,
    ) -> None:
        DPR_swath_def = geometry.SwathDefinition(
            lons=self.chosen_band_data.latitude, lats=self.chosen_band_data.longitude
        )
        GMI_swath_def = geometry.SwathDefinition(
            lons=self.one_track_data.latitude_GMI,
            lats=self.one_track_data.longitude_GMI,
        )

        self.ice_conc_DPR = kd_tree.resample_nearest(
            GMI_swath_def,
            self.one_track_data.ice_concentration_GMI,
            DPR_swath_def,
            fill_value=FILL_VALUE_RESAMPLE,
            radius_of_influence=INFLUENCE_RADIUS,
            epsilon=EPSILON_RESAMPLE,
            nprocs=1,
        )

    def create_mask(
        self,
    ) -> None:
        surface_type = self.chosen_band_data.surface_type
        latitude = self.chosen_band_data.latitude
        longitude = self.chosen_band_data.longitude

        open_ocean_mask = np.logical_and(surface_type >= 0, surface_type <= 99)
        internal_waters_mask = np.logical_and(surface_type >= 300, surface_type <= 399)
        mask_no_land = np.logical_or(open_ocean_mask, internal_waters_mask)

        mask_no_rain = self.chosen_band_data.precipitation_rate < 1
        mask_no_ice = self.ice_conc_DPR < 0.01
        roi = self.cfg.region_of_interest

        mask_geo = np.logical_and.reduce(
            (
                latitude >= roi.latitude_min,
                latitude <= roi.latitude_max,
                longitude >= roi.longitude_min,
                longitude <= roi.longitude_max,
            )
        )

        self.mask = np.logical_and.reduce(
            (mask_no_land, mask_no_rain, mask_no_ice, mask_geo)
        )
        self.idxs_mask_true = np.argwhere(self.mask)

    def select_window(
        self,
        window_center: Any,
    ) -> np.ndarray:
        window_size_along = (
            self.cfg.window_processing.window_size.along_flight_direction
        )
        window_size_across = (
            self.cfg.window_processing.window_size.across_flight_direction
        )

        index_min_flight = (
            window_center.along_flight_direction - window_size_along * 0.5
        )

        index_max_flight = (
            window_center.along_flight_direction + window_size_along * 0.5 + 1
        )

        index_min_scan = (
            window_center.across_flight_direction - window_size_across * 0.5
        )

        index_max_scan = (
            window_center.across_flight_direction + window_size_across * 0.5 + 1
        )

        window = Window(
            cfg=self.cfg,
            window_center=window_center,
            incidence_angle=self.chosen_band_data.incidence_angle[
                index_min_flight:index_max_flight, index_min_scan:index_max_scan
            ],
            sigma=self.chosen_band_data.sigma[
                index_min_flight:index_max_flight, index_min_scan:index_max_scan
            ],
            mask=self.mask[
                index_min_flight:index_max_flight, index_min_scan:index_max_scan
            ],
        )

        return window

    def get_results(
        self,
        window: Window,
    ):
        pass

    def smooth(
        self,
    ):
        pass
