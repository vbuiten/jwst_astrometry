'''Utility functions for the astrometric calibration.'''

import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS

from IPython import embed


def match_sources_to_cat(source_pos: SkyCoord, cat_pos: SkyCoord, max_separation: u.Quantity = 1*u.arcsec):

    idx, d2d, _ = source_pos.match_to_catalog_sky(cat_pos)   # idx is the index into cat_coords closest to each source

    # find matches within max_separation
    within_max_sep = d2d < max_separation

    # isolate the matches
    pos_detected = source_pos[within_max_sep]
    pos_catalog = cat_pos[idx[within_max_sep]]

    return within_max_sep, pos_detected, pos_catalog


def measure_offset(pos_detected, pos_catalog):

    dra, ddec = pos_detected.spherical_offsets_to(pos_catalog)
    dra_median = np.median(dra)
    ddec_median = np.median(ddec)

    return dra_median, ddec_median


def translate_wcs(wcs, dra, ddec):

    crval_new = SkyCoord(*wcs.wcs.crval, unit="deg", frame="icrs").spherical_offsets_by(dra, ddec)

    wcs_new = wcs.deepcopy()

    wcs_new.wcs.crval[0] = crval_new.ra.to(u.deg).value
    wcs_new.wcs.crval[1] = crval_new.dec.to(u.deg).value

    # it seems that the wcs object needs to be re-initialized to update the wcs
    # the crval attributes are updated, but the transforms apparently not
    wcs_new = WCS(wcs_new.to_header())

    return wcs_new,  crval_new