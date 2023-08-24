'''Module for visualising 2D sky images with a coordinate frame.'''

from jwst_astrometry.visualisation.sky_im_base import SkyImBase

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


class SkyIm2D(SkyImBase):
    def __init__(self, wcs, *fig_args):

        super(SkyIm2D, self).__init__(wcs)

        self.fig = plt.figure(*fig_args)
        self.ax = self.fig.add_subplot(projection=self.wcs)

        self.ax.set_xlabel("RA")
        self.ax.set_ylabel("Dec")


    def imshow(self, im_data, norm="log", cmap="turbo", *args, **kwargs):

        if norm == "log":
            self.im = self.ax.imshow(im_data, norm=LogNorm(), cmap=cmap, *args, **kwargs)

        elif norm == "linear":
            self.im = self.ax.imshow(im_data, cmap=cmap, *args, **kwargs)

        self.cbar = self.fig.colorbar(self.im, ax=self.ax)


    def plot_coords(self, sky_coords, marker="o", markersize=4, alpha=.6, markerfacecolor="none",
                    *args, **kwargs):

        self.ax.plot(sky_coords.ra, sky_coords.dec, transform=self.ax.get_transform("icrs"), ls="",
                     marker=marker, markersize=markersize, alpha=alpha, markerfacecolor=markerfacecolor,
                     *args, **kwargs)



    def grid(self, color="white", alpha=.6, *args, **kwargs):

        self.ax.grid(which="major", color=color, alpha=alpha, *args, **kwargs)



    def show(self):

        self.fig.show()


    def save(self, filename, *args):

        self.fig.savefig(filename, *args)


    def close(self):

        self.fig.close()
