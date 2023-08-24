'''Module for calibrating the WCS based on imaging data and the Gaia catalog.'''

import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits

from jwst_astrometry.data.imaging import ImagingData
from jwst_astrometry.data.gaia import get_gaia_catalog
from jwst_astrometry.calibration.utils import *

from IPython import embed

class WCSCalibrator:
    def __init__(self, im_data: ImagingData, gaia_box_width=0.1*u.deg, max_separation=1*u.arcsec):

        self.im_data = im_data
        self.wcs_new = None   # the new WCS will come here

        # detect sources in the image if it hasn't been done already
        if self.im_data.sources is None:
            self.im_data.find_sources()
        pos_sky_all_det = SkyCoord(self.im_data.sources['RA'], self.im_data.sources['Dec'])

        # query the Gaia catalog
        gaia_cat = get_gaia_catalog(self.im_data.crval_ra, self.im_data.crval_dec, boxwidth=gaia_box_width)

        # match to sources in the image
        self.matched_mask, self.pos_sky_det, self.pos_sky_cat = match_sources_to_cat(pos_sky_all_det, gaia_cat, max_separation=max_separation)
        print ("Found {} matches".format(len(self.pos_sky_det)))

        # measure the mean offset Gaia - image
        self.dra, self.ddec = measure_offset(self.pos_sky_det, self.pos_sky_cat)


    def correct_wcs(self):

        wcs_new, crval_new = translate_wcs(self.im_data.wcs, self.dra, self.ddec)

        # update the header in the hdulist
        self.im_data.header.update(CRVAL1=crval_new.ra.deg, CRVAL2=crval_new.dec.deg)
        self.wcs_new = wcs_new

        print ("Updated the header with the new CRVALs.")

        # also update the positions of the sources (for visualisation/checks)
        pos_pix = np.transpose((self.im_data.sources[self.matched_mask]["xcentroid"],
                                self.im_data.sources[self.matched_mask]["ycentroid"]))
        self.pos_sky_det_new = self.wcs_new.pixel_to_world(pos_pix[:,0], pos_pix[:,1])


    def write_corrected_wcs(self):

        filename, ext = self.im_data.filename.split(".")
        filename_new = filename + "_NEW_WCS." + ext

        self.im_data.hdulist.writeto(filename_new, overwrite=True)
        print ("Wrote the new WCS to {}".format(filename_new))


    def correct_header_other(self, other_filename):
        '''
        Correct the WCS in the header of another file, using the offset measured from this image. Can be used to correct
        an MRS IFU cube based on simultaneous imaging data.

        :param other_filename:
        :return:
        '''

        # open the other file
        hdulist = fits.open(other_filename)

        # update the header in the hdulist
        crval1_new = hdulist[1].header["CRVAL1"] + self.dra.to(u.deg).value
        crval2_new = hdulist[1].header["CRVAL2"] + self.ddec.to(u.deg).value

        hdulist[1].header.update(CRVAL1=crval1_new, CRVAL2=crval2_new)

        # write the new file
        filename, ext = other_filename.split(".")
        filename_new = filename + "_NEW_WCS." + ext
        hdulist.writeto(filename_new, overwrite=True)
        print ("Wrote the new WCS to {}".format(filename_new))

        # close the file
        hdulist.close()