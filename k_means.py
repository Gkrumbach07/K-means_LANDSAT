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
            normalized_data[j] != None:
                temp_point.location.append(normalized_data[j][i])
        data_points.append(temp_point)

def get_distance(pos_1, pos_2):
    if pos_1.__len__() == pos_2.__len__():
        sum = 0
        for i in range(pos_1):
            sum += math.pow(pos_1[i] - pos_2[i], 2)
        return math.sqrt(sum)
    else return None
  
def make_centroids(num):
    for i in range(num):
        temp_centroid = Centroid()
        for j in range(normalized_data.__len__()):
            normalized_data[j] != None:
                temp_centroid.location.append(randint(data_min, data_max))
        centroids.append(temp_centroid)
    # randomly place centroids based on points
    
def update_point_labels():
    for i in range(data_points):
        top_dist = None
        label = None
        for j in range(centroids):
            if get_distance(data_points[i], centroids[j]) > top_dist:
                label = centroids[j].label
        data_points[i].label = label
        
def update_centroid_pos():
    for i in range(centroids):
        temp_pos = []
        for a in range(centroids[0].location)  # for each dimension in centroid location
            temp_sum = 0
            for j in range(data_points):
                if data_points[j].label == centroids[i].label:
                    temp_sum += data_points[j].location[a]
            temp_pos.append(temp_sum/data_points.__len__())
                

import_data(100)
make_points()
print normalized_data
