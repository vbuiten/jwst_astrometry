'''Module for obtaining Gaia catalog data.'''

from astroquery.gaia import Gaia
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"

from astropy.coordinates import SkyCoord
import astropy.units as u


def get_gaia_catalog(ra, dec, boxwidth=.1*u.deg):

    center_coord = SkyCoord(ra, dec, frame="icrs")
    gaia_r = Gaia.query_object_async(coordinate=center_coord, width=boxwidth, height=boxwidth)
    gaia_r.pprint(max_lines=12, max_width=120)

    gaia_cat = SkyCoord(ra=gaia_r["ra"], dec=gaia_r["dec"])

    return gaia_cat