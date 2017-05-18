import math
import os
from dataGrabber import LandsatImageData
import random


# make into class?
normalized_data = []
data_points = []
centroids = []  # centroid label is index and a centroid is defined by a list of floats or make into class
data_min = 0
data_max = 1000

class Point:
    location = []
    label = None  # int value or centroid
    
class Centroid:
    location = []
    label = None  # int value


def import_data(iterations):  # make min and max the same
    for filename in os.listdir("landsat_tif"):
        if filename.endswith(".TIF"):
            normalized_data.append(LandsatImageData('landsat_tif\\' + filename, iterations).compiled_data)
            continue
        else:
            continue


def make_points():
    for i in range(10):  # find a way to get length of a band
        temp_point = Point()
        for j in range(normalized_data.__len__()):
            temp_point.location.append(normalized_data[j][i])
        data_points.append(temp_point)

def get_distance(pos_1, pos_2):
    sum = 0
    for i in range(pos_1):
        sum += math.pow(pos_1[i] - pos_2[i], 2)
    return math.sqrt(sum)
  
def make_centroids(num):
    for i in range(num):
        temp_centroid = []
        for j in range(normalized_data.__len__()):
            normalized_data[i] != None:
                temp_centroid.append(randint(data_min, data_max))
    # randomly place centroids based on points


import_data(100)
make_points()
print normalized_data
