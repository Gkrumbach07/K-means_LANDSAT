import math
import os
from dataGrabber import LandsatImageData

normalized_data = [None, None, None, None, None, None, None, None, None, None, None]
data_points = []


class Point:
    # 1 Ultra Blue (coastal/aerosol)
    # 2 Blue
    # 3 Green
    # 4 Red
    # 5 Near Infrared (NIR)
    # 6 Shortwave Infrared (SWIR) 1
    # 7 Shortwave Infrared (SWIR) 2
    # 8 Panchromatic
    # 9 Cirrus
    # 10 Thermal Infrared (TIRS) 1
    # 11 Thermal Infrared (TIRS) 2
    bands = []
    label = None  # int value

    def __init__(self, b1=None, b2=None, b3=None, b4=None, b5=None, b6=None,
                 b7=None, b8=None, b9=None, b10=None, b11=None):
        self.bands = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11]


def import_data(iterations):
    for filename in os.listdir("landsat_tif"):
        if filename.endswith(".TIF"):
            for i in range(11):
                if filename.__contains__(str(i+1)):
                    normalized_data[i] = LandsatImageData('landsat_tif\\' + filename, iterations).compiled_data
            continue
        else:
            continue


def make_points():
    for i in range(10):  # find a way to get length of a band
        data_points.append(Point(normalized_data[0][i], normalized_data[1][i], normalized_data[2][i],  # list has None types in it so [i] cant be used
                                 normalized_data[3][i], normalized_data[4][i], normalized_data[5][i],
                                 normalized_data[6][i], normalized_data[7][i], normalized_data[8][i],
                                 normalized_data[9][i], normalized_data[10][i]))

def get_distance(pos_1, pos_2):
    sum = 0
    for i in range(pos_1):
        sum += math.pow(pos_1[i] - pos_2[i], 2)
    return math.sqrt(sum)


import_data(100)
make_points()
print normalized_data
