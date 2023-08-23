'''Module for the abstract base class for the data.'''

from abc import ABC, abstractmethod

class DataAbstractBase(ABC):

    def __init__(self, filename, data_idx):

        self.filename = filename
        self.data_idx = data_idx

    @abstractmethod
    def close(self):
        pass

