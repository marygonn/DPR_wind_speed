from omegaconf import DictConfig
from .annotation import ExtractedHDF5Data
from .defs import FILL_VALUE_RESAMPLE, INFL_RADIUS, EPSILON_RESAMPLE
from pyresample import kd_tree, geometry, image

import numpy as np

class Swath:
    def __init__(
        self,
        cfg: DictConfig,
        one_track_data: ExtractedHDF5Data,
        band_label: str,
    ):
        #self.inc_angle = 0
        self.cfg = cfg
        self.one_track_data = one_track_data
        self.chosen_band_data = one_track_data.Ka if band_label == 'Ka' else one_track_data.Ku
        #breakpoint()
        self.mask = []
        self.index_mask = []
        self.ice_conc_DPR = []

    def Resample_ice_conc_DPR( 
        self,
        #cfg: DictConfig,        
    ) -> None:
        
        DPR_swath_def = geometry.SwathDefinition(lons = self.chosen_band_data.latitude, 
                                                    lats = self.chosen_band_data.longitude)
        GMI_swath_def = geometry.SwathDefinition(lons = self.one_track_data.latitude_GMI, 
                                                    lats = self.one_track_data.longitude_GMI)

        self.ice_conc_DPR = kd_tree.resample_nearest(GMI_swath_def, self.one_track_data.ice_concentration_GMI,
        DPR_swath_def, fill_value = FILL_VALUE_RESAMPLE, radius_of_influence = INFL_RADIUS, epsilon = EPSILON_RESAMPLE, nprocs=1)
        #breakpoint()
        
    def Create_mask(
        self,
    ) -> None:

        surface_type = self.chosen_band_data.surface_type
        latitude = self.chosen_band_data.latitude
        longitude = self.chosen_band_data.longitude

        mask_no_land = np.logical_or(np.logical_and(surface_type >= 0,surface_type <= 99),                  # open ocean
                                    np.logical_and(surface_type >= 300,surface_type <= 399))               # internal waters

        mask_no_rain = self.chosen_band_data.precipitation_rate < 1
        mask_no_ice = self.ice_conc_DPR < 0.01
        mask_geo = np.logical_and.reduce((self.chosen_band_data.latitude >= self.cfg.region_of_interest.latitude_min,
                                        self.chosen_band_data.latitude <= self.cfg.region_of_interest.latitude_max,  
                                        self.chosen_band_data.longitude >= self.cfg.region_of_interest.longitude_min,
                                        self.chosen_band_data.longitude <= self.cfg.region_of_interest.longitude_max,         
                                        ))

        self.mask = np.logical_and.reduce((mask_no_land, mask_no_rain, mask_no_ice, mask_geo))
        self.index_mask = np.argwhere(self.mask)
        

    def Select_window(
        self,
        window_center,
    ) -> np.ndarray:

        index_min_flight = window_center.along_flight_direction -\
                            self.cfg.window_processing.window_size_along_flight_direction * 0.5

        index_max_flight = window_center.along_flight_direction +\
                            self.cfg.window_processing.window_size_along_flight_direction * 0.5 + 1

        index_min_scan = window_center.across_flight_direction -\
                            self.cfg.window_processing.window_size_across_flight_direction * 0.5

        index_max_scan = window_center.across_flight_direction +\
                            self.cfg.window_processing.window_size_across_flight_direction * 0.5 + 1 

        window.incidence_angle = self.chosen_band_data.incidence_angle[index_min_flight:index_max_flight,
                                                            index_min_scan:index_max_scan]

        window.nrcsdb = self.chosen_band_data.sigma[index_min_flight:index_max_flight,
                                                    index_min_scan:index_max_scan]

        window.mask = self.mask[index_min_flight:index_max_flight,
                                index_min_scan:index_max_scan]
        return window       


    # def Select_window:
