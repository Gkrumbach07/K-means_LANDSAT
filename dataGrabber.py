import gdal
import struct
import numpy as np
from gdalconst import *


class LandsatImageData:
    data_min = None
    data_max = None
    band = None
    iteration = 100
    compiled_data = []

    def __init__(self, data_file_path, iterate):
        data_set = gdal.Open(data_file_path, GA_ReadOnly)
        self.band = data_set.GetRasterBand(1)
        self.dataMin = self.band.GetMinimum() #16-bit =  0-65535
        self.dataMax = self.band.GetMaximum()
        self.iteration = iterate

    def upack_data(self, xoff, yoff, xsize, ysize):
        scan_area = self.band.ReadRaster(xoff, yoff, xsize, ysize, xsize, ysize, GDT_Float32)
        float_tuple = struct.unpack('f' * xsize * ysize, scan_area)
        return float_tuple

    def thin_data(self, float_tuple):
        for i in range(float_tuple.__len__()): # ++n
            if i % self.iteration == 0:
                if float_tuple[i] != 0: #OPTIMIZE--- Start from middle and go until n number of no data pixles show up
                    compiled_data.append(normalize(float_tuple[i], data_min, data_max)
    
    def create_dataset(self):
      for i in range(self.band.YSize):
        self.thin_data(self.upack_data(0, i, self.band.XSize, 1), self.iteration)
        
    def normalize(self, value, min, max):
      normalized = (value - min) / (max - min)
      return normalized


blue_band = LandsatImageData("landsat_tif\B2.TIF", 100)
blue_band.create_dataset()