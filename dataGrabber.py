import gdal
import struct
from gdalconst import *


class LandsatImageData:
    def __init__(self, data_file_path, iterate, line=-1):
        self. compiled_data = []
        self.data_min = None
        self.data_max = None
        self.band = None
        self.iteration = 100
        self.data_set = None
        self.line = line

        self.data_set = gdal.Open(data_file_path, GA_ReadOnly)
        self.band = self.data_set.GetRasterBand(1)
        self.band.DeleteNoDataValue()
        (self.data_min, self.data_max) = self.band.ComputeRasterMinMax(1)
        self.iteration = iterate
        self.create_dataset()

    def unpack_data(self, xoff, yoff, xsize, ysize):
        scan_area = self.band.ReadRaster(xoff, yoff, xsize, ysize, xsize, ysize, GDT_Float32)
        float_tuple = struct.unpack('f' * xsize * ysize, scan_area)
        return float_tuple

    def create_dataset(self):
        if self.line == -1:
            for i in range(self.band.YSize):
                if i % self.iteration == 0:
                    self.thin_data(self.unpack_data(0, i, self.band.XSize, 1))
        else:
            self.thin_data(self.unpack_data(0, self.line, self.band.XSize, 1))

    def normalize(self, value, min, max):
        normalized = (value - min) / (max - min)
        return normalized

    def thin_data(self, float_tuple):
        for i in range(float_tuple.__len__()):
            if self.line == -1:
                if i % self.iteration == 0:
                    if float_tuple[i] != 0:
                        self.compiled_data.append(self.normalize(float_tuple[i], self.data_min, self.data_max))
            else:
                self.compiled_data.append(self.normalize(float_tuple[i], self.data_min, self.data_max))
