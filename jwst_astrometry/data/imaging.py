'''Module for loading the (simultaneous) imaging data.'''

from data import DataAbstractBase

import numpy as np
from astropy.wcs import WCS
from astropy.io import fits

class ImagingData(DataAbstractBase):
    def __init__(self, filename, image_idx=1):

        super(ImagingData, self).__init__(filename, image_idx)

        self.hdulist = fits.open(filename)
        self.header = self.hdulist[image_idx].header
        self.data = self.hdulist[image_idx].data
        self.wcs = WCS(self.header)

        self.rms = np.std(self.data)


    def close(self, verbose=True):

        self.hdulist.close()

        if verbose:
            print ("Closed imaging data file: {}".format(self.filename))