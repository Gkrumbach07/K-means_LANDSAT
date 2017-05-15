import gdal
import struct
from gdalconst import *


class LandsatImageData:
    data_min = None
    data_max = None
    band = None
    iteration = 100
    compiled_data = []
    data_set = None

    def __init__(self, data_file_path, iterate):
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
        for i in range(self.band.YSize):
            if i % self.iteration == 0:
                self.thin_data(self.unpack_data(0, i, self.band.XSize, 1))

    def normalize(self, value, min, max):
        normalized = (value - min) / (max - min)
        return normalized

    def thin_data(self, float_tuple):
        for i in range(float_tuple.__len__()):  # ++n
            if i % self.iteration == 0:
                if float_tuple[i] != 0:  # OPTIMIZE--- Start from middle and go until n number of no data pixles show up
                    self.compiled_data.append(self.normalize(float_tuple[i], self.data_min, self.data_max))
