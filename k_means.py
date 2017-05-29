import math
import os
from dataGrabber import LandsatImageData
import random
import matplotlib.pyplot as plt
import gdal
import numpy
import time
import sys


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
    def __init__(self, file_indexes=[]):
        self.normalized_data = []
        self.data_points = []
        self.centroids = []
        self.x_size = None
        self.y_size = None
        self.file_indexes = file_indexes

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
            return dist_sum
        else:
            return None

    def make_points(self, num):
        for i in range(num):
            temp_point = Point()
            for j in range(self.normalized_data.__len__()):
                temp_point.pos.append(self.normalized_data[j][i])
            self.data_points.append(temp_point)

    def import_data(self, sample):  # make min and max the same
        index = 0
        for filename in os.listdir("landsat_tif"):
            if filename.endswith(".tif") or filename.endswith(".TIF"):
                if self.file_indexes.__contains__(index) and self.file_indexes != []:
                    temp = LandsatImageData('landsat_tif\\' + filename, sample)
                    self.normalized_data.append(temp.compiled_data)
                    self.x_size = temp.band.XSize
                    self.y_size = temp.band.YSize
            index += 1

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


class Classifier:
    def import_data(self, line):
        index = 0
        temp = []
        for filename in os.listdir("landsat_tif"):
            if filename.endswith(".tif") or filename.endswith(".TIF"):
                if self.file_indexes.__contains__(index) and self.file_indexes != []:
                    temp.append(LandsatImageData('landsat_tif\\' + filename, 0, line).compiled_data)
            index += 1
        return temp

    def get_point_labels(self, pos):
        short_dist = 100000
        label = None
        for i in self.alg.centroids:
            temp_dist = self.alg.get_distance(pos, i.pos)
            if temp_dist < short_dist:
                label = i.label
                short_dist = temp_dist
        return label

    def make_point(self, index):
        point = []
        for i in self.data:
            point.append(i[index])
        return point

    def export_tif(self):
        format = "GTiff"
        driver = gdal.GetDriverByName(format)
        raster = numpy.zeros((self.alg.y_size, self.alg.x_size), dtype=numpy.uint8)
        for filename in os.listdir("landsat_tif"):
            if filename.endswith(".tif") or filename.endswith(".TIF"):
                src_file = filename
                break
        src_ds = gdal.Open('landsat_tif/' + src_file)
        dst_ds = driver.CreateCopy(str(self.export_name) + '.tif', src_ds, 0)

        for y in range(self.alg.y_size - 1):
            if y % 100 == 0:
                sys.stdout.write("\r" + str(y) + "/" + str(self.alg.y_size) + "  " + str(round(y*100.0/self.alg.y_size, 2)) + "%")
                sys.stdout.flush()
            self.data = self.import_data(y)
            for x in range(len(self.data[0]) - 1):
                raster[y][x] = self.get_point_labels(self.make_point(x))
        dst_ds.GetRasterBand(1).WriteArray(raster)
        dst_ds = None
        src_ds = None

    def stop_watch(self, value):
        valueD = (((value / 365) / 24) / 60)
        Days = int(valueD)

        valueH = (valueD - Days) * 365
        Hours = int(valueH)

        valueM = (valueH - Hours) * 24
        Minutes = int(valueM)

        valueS = (valueM - Minutes) * 60
        Seconds = int(valueS)

        return Hours, ":", Minutes, ";", Seconds

    def __init__(self, iterations, clusters, max_dist, export_name, points=-1, stop=-1, plot=False, plot_x_axis=0, plot_y_axis=1, file_indexes=[]):
        start_time = time.time()
        self.export_name = export_name
        self.file_indexes = file_indexes
        self.alg = Kmeans(file_indexes)
        self.alg.import_data(iterations)
        max_size = float('inf')
        for i in range(self.alg.normalized_data.__len__()):
            if max_size > self.alg.normalized_data[i].__len__():
                max_size = self.alg.normalized_data[i].__len__()
        if points >= max_size or points == -1:
            points = max_size
        self.alg.main(points, clusters, max_dist, stop, plot, plot_x_axis, plot_y_axis)
        self.data = None
        self.export_tif()
        print 'Finished in ' + str(self.stop_watch(time.time() - start_time))


Classifier(100, 4, .005, "export1", file_indexes=[1, 2, 3])
Classifier(100, 4, .005, "export2", file_indexes=[3, 4, 5, 6])
Classifier(100, 4, .005, "export3", file_indexes=[4, 5, 6])
