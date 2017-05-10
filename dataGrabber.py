import gdal
import struct
import numpy as np
from gdalconst import *


class LandsatImageData:
    data_min = None
    data_max = None
    dat_set = None
    band = None

    def __init__(self, data_file_path):
        self.data_set = gdal.Open(data_file_path, GA_ReadOnly)
        self.band = self.data_set.GetRasterBand(1)
        self.dataMin = self.band.GetMinimum()
        self.dataMax = self.band.GetMaximum()

    def upack_data(self, xoff, yoff, xsize, ysize):
        scan_area = self.band.ReadRaster(xoff, yoff, xsize, ysize, xsize, ysize, GDT_Float32)
        float_tuple = struct.unpack('f' * xsize * ysize, scan_area)
        return float_tuple

    def thin_data(self, float_tuple, iteration):
        new_data = []
        for i in range(float_tuple.__len__()):
            if i % iteration == 0:
                if float_tuple[i] != 0: #OPTIMIZE--- Start from middle and go until n number of no data pixles show up
                    new_data.append(float_tuple[i])
        return new_data
    
    def create_dataset(self):
      compiled_data = [] #too many arrays -- reduce 
      for i in range(self.band.YSize):
        compiled_data.append(self.thin_data(self.upack_data(0, 0, self.band.XSize, i), 10))


blue_band = LandsatImageData("landsat_tif\B2.TIF")
print blue_band.thin_data(blue_band.upack_data(0, 3000, blue_band.band.XSize, 1), 1)
#16-bit =  0-65535