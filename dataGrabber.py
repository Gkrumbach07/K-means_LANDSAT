import gdal
import struct
import numpy as np
from gdalconst import *


class LandsatImageData:
    dataMin = None
    dataMax = None
    dataSet = None
    band = None

    def __init__(self, data_file_path):
        self.dataSet = gdal.Open(data_file_path, GA_ReadOnly)
        self.band = self.dataSet.GetRasterBand(1)
        self.dataMin = self.band.GetMinimum()
        self.dataMax = self.band.GetMaximum()

    def UnpackData(self, xoff, yoff, xsize, ysize):
        scanArea = self.band.ReadRaster(xoff, yoff, xsize, ysize, xsize, ysize, GDT_Float32)
        floatTuple = struct.unpack('f' * xsize * ysize, scanArea)
        return floatTuple

    def thinData(self, float_tuple, iteration):
        newData = []
        for i in range(float_tuple.__len__()):
            if i % iteration == 0:
                newData.append(float_tuple[i])
        return newData


blueBand = LandsatImageData("landsat_tif\B2.TIF")
print blueBand.thinData(blueBand.unpackData(0, 3000, blueBand.band.XSize, 1), 1)
