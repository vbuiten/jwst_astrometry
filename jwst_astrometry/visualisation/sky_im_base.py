'''Abstract base class for figures with a WCS projection.'''

from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


class SkyImBase(ABC):
    def __init__(self, wcs):

        # a WCS must be provided in all cases
        self.wcs = wcs

        # fig and ax attributes can be filled in by subclasses in initialisation
        self.fig = None
        self.ax = None

        # im and cbar attributes can be filled in by subclasses when data is plotted
        self.im = None
        self.cbar = None


    @abstractmethod
    def imshow(self, im_data, *args, **kwargs):
        pass


    @abstractmethod
    def show(self):
        pass


    @abstractmethod
    def close(self):
        pass


    @abstractmethod
    def save(self, filename):
        pass



