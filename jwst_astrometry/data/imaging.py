'''Module for loading the (simultaneous) imaging data.'''

from data import DataAbstractBase
from calibration.utils import match_sources_to_cat

import numpy as np
from astropy.wcs import WCS
from astropy.io import fits
import astropy.units as u
from astropy.coordinates import SkyCoord

from photutils import DAOStarFinder

class ImagingData(DataAbstractBase):
    def __init__(self, filename, image_idx=1):

        super(ImagingData, self).__init__(filename, image_idx)

        self.hdulist = fits.open(filename)
        self.header = self.hdulist[image_idx].header
        self.data = self.hdulist[image_idx].data

        self.wcs = WCS(self.header)
        self.crval_ra = self.wcs.wcs.crval[0] * u.deg
        self.crval_dec = self.wcs.wcs.crval[1] * u.deg

        self.rms = np.std(self.data)


    def find_sources(self, fwhm=5, threshold_factor=5):

        # find sources with DAOStarFinder
        daofind = DAOStarFinder(fwhm=fwhm, threshold=threshold_factor*self.rms)
        sources = daofind(self.data)
        print ("Found {} sources.".format(len(sources)))

        # convert pixel coordinates to RA/Dec
        pos_pix = np.transpose((sources['xcentroid'], sources['ycentroid']))
        pos_sky = self.wcs.pixel_to_world(pos_pix[:,0], pos_pix[:,1])

        # add RA/Dec to the table
        sources['RA'] = pos_sky.ra
        sources['Dec'] = pos_sky.dec

        # store the table as an attribute for later use
        self.sources = sources

        return sources


    def match_sources(self, sources, cat_coords, max_separation=1*u.arcsec):
        '''

        :param sources:
        :param cat_coords:
        :param max_separation:
        :return:
        '''

        pos_sky = SkyCoord(sources['RA'], sources['Dec'], frame="icrs")
        pos_sky_detected, pos_sky_catalog = match_sources_to_cat(pos_sky, cat_coords, max_separation=max_separation)

        return pos_sky_detected, pos_sky_catalog


    def close(self, verbose=True):

        self.hdulist.close()

        if verbose:
            print ("Closed imaging data file: {}".format(self.filename))