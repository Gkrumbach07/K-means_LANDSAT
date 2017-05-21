import math
import os
from dataGrabber import LandsatImageData
import random
import matplotlib.pyplot as plt
import gdal
from gdalconst import *
import osr
import numpy


class Point:
    def __init__(self):
        self.pos = []
        self.label = None  # int value


class Centroid:
    def __init__(self):
        self.pos = []
        self.old_pos = []
        self.label = None  # int value

    def print_num_points(self, data_points):
        total = 0
        for i in data_points:
            if i.label == self.label:
                total += 1
        print total


class Kmeans:
    def __init__(self):
        self.normalized_data = []
        self.data_points = []
        self.centroids = []
        self.x_size = None
        self.y_size = None

    def main(self, points_num, centroids_num, max_dist, stop=-1, plot=False, x_axis=0, y_axis=1):
        if plot:
            ax = plt.figure()

        self.make_points(points_num)
        self.make_centroids(centroids_num)

        count = 0
        if plot:
            self.plot_data(count, ax, x_axis, y_axis)

        while count != stop:
            count += 1
            self.update_point_labels()
            self.update_centroid_pos()
            if plot:
                self.plot_data(count, ax, x_axis, y_axis)
            if self.change_threshold(max_dist):
                break
        if plot:
            plt.show()

    def get_max_dist(self):
        dist = []
        for i in self.centroids:
            dist.append(self.get_distance(i.pos, i.old_pos))
        return str(max(dist))

    def change_threshold(self, threshold):
        for i in self.centroids:
            if self.get_distance(i.pos, i.old_pos) > threshold:
                return False
        return True

    def update_centroid_pos(self):
        for i in range(self.centroids.__len__()):
            temp_pos = []
            for d in range(self.centroids[0].pos.__len__()):  # for each dimension in centroid pos
                temp_sum = 0
                num_points = 0
                for j in self.data_points:
                    if j.label == self.centroids[i].label:
                        num_points += 1
                        temp_sum += j.pos[d]
                if num_points != 0:
                    temp_pos.append(temp_sum / num_points)

            self.centroids[i].old_pos = self.centroids[i].pos
            if num_points != 0:
                self.centroids[i].pos = temp_pos

    def update_point_labels(self):
        for i in range(self.data_points.__len__()):
            short_dist = 100000
            label = None
            for j in range(self.centroids.__len__()):
                temp_dist = self.get_distance(self.data_points[i].pos, self.centroids[j].pos)
                if temp_dist < short_dist:
                    label = self.centroids[j].label
                    short_dist = temp_dist
                self.data_points[i].label = label

    def make_centroids(self, num):
        for i in range(num):
            temp_centroid = Centroid()
            temp_centroid.pos = self.data_points[random.randint(0, len(self.data_points) - 1)].pos
            temp_centroid.label = i
            self.centroids.append(temp_centroid)

    def get_distance(self, pos_1, pos_2):
        if pos_1.__len__() == pos_2.__len__():
            dist_sum = 0
            for i in range(pos_1.__len__()):
                dist_sum += math.pow(pos_1[i] - pos_2[i], 2)
            return math.sqrt(dist_sum)
        else:
            return None

    def make_points(self, num):
        for i in range(num):  # find a way to get length of a band
            temp_point = Point()
            for j in range(self.normalized_data.__len__()):
                temp_point.pos.append(self.normalized_data[j][i])
            self.data_points.append(temp_point)

    def import_data(self, sample):  # make min and max the same
        for filename in os.listdir("landsat_tif"):
            if filename.endswith(".tif"):
                temp = LandsatImageData('landsat_tif\\' + filename, sample)
                self.normalized_data.append(temp.compiled_data)
                self.x_size = temp.band.XSize
                self.y_size = temp.band.YSize

    def make_debug_data(self, num, distribute=1):
        if distribute == 1:
            temp = []
            for i in range(num / 2):
                temp.append(random.uniform(0.0, 0.4))
            for i in range(num / 2):
                temp.append(random.uniform(0.6, 1.0))
            self.normalized_data.append(temp)

            temp1 = []
            for i in range(num / 2):
                temp1.append(random.uniform(0.0, 0.4))
            for i in range(num / 2):
                temp1.append(random.uniform(0.6, 1.0))
            self.normalized_data.append(temp1)

        elif distribute == 2:
            temp = []
            for i in range(num):
                temp.append(random.uniform(0.0, 1.0))
            self.normalized_data.append(temp)

            temp = []
            for i in range(num):
                temp.append(random.uniform(0.0, 1.0))
            self.normalized_data.append(temp)

    def plot_data(self, plot_num, figure, x_axis, y_axis):
        print "Iteration " + str(plot_num) + "- Max Distance: " + self.get_max_dist()
        sub = figure.add_subplot(5, 5, plot_num + 1, title="Iteration " + str(plot_num))

        if plot_num != 0:
            col = ('r', 'g', 'y', 'c', 'm', 'k', 'w', '#ce6f3b')
            for i in self.data_points:
                sub.scatter(i.pos[x_axis], i.pos[y_axis], color=col[i.label], alpha=0.3, marker='.')

        for c in self.centroids:
            x = c.pos[x_axis]
            y = c.pos[y_axis]
            sub.scatter(x, y, color='b', marker='.', s=50)

        axes = plt.gca()
        axes.set_xlim([0, 1])
        axes.set_ylim([0, 1])


def import_data(line):  # make min and max the same
    temp = []
    for filename in os.listdir("landsat_tif"):
        if filename.endswith(".tif"):
            temp.append(LandsatImageData('landsat_tif\\' + filename, 0, line).compiled_data)
    return temp


def get_point_labels(pos):
    short_dist = 100000
    label = None
    for i in alg.centroids:
        temp_dist = alg.get_distance(pos, i.pos)
        if temp_dist < short_dist:
            label = i.label
            short_dist = temp_dist
    return label


def make_point(index):
    point = []
    for i in data:
        point.append(i[index])
    return point

alg = Kmeans()
alg.import_data(100)
alg.main(300, 10, .005)


format = "GTiff"
driver = gdal.GetDriverByName(format)
# dst_ds = driver.Create('exportedRaster.TIF', alg.x_size, alg.y_size, 1, gdal.GDT_Byte)
raster = numpy.zeros((alg.y_size, alg.x_size), dtype=numpy.uint8)
src_ds = gdal.Open('landsat_tif/B2.TIF')
dst_ds = driver.CreateCopy('exportedRaster3.TIF', src_ds, 0)


for y in range(alg.y_size - 1):
    if y % 100 == 0:
        print str(y) + "/" + str(alg.y_size)
    data = import_data(y)
    for x in range(len(data[0]) - 1):
        raster[y][x] = get_point_labels(make_point(x))
dst_ds.GetRasterBand(1).WriteArray(raster)
dst_ds = None
src_ds = None
