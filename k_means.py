import math
import os
from dataGrabber import LandsatImageData
import random
import matplotlib.pyplot as plt


class Point:
    def __init__(self):
        self.pos = []
        self.label = None  # int value


class Centroid:
    def __init__(self):
        self.pos = []
        self.old_pos = []
        self.label = None  # int value

    def print_num_points(self):
        total = 0
        for i in data_points:
            if i.label == self.label:
                total += 1
        print total


def import_data(iterations):  # make min and max the same
    for filename in os.listdir("landsat_tif"):
        if filename.endswith(".TIF"):
            normalized_data.append(LandsatImageData('landsat_tif\\' + filename, iterations).compiled_data)


def make_points(num):
    for i in range(num):  # find a way to get length of a band
        temp_point = Point()
        for j in range(normalized_data.__len__()):
            temp_point.pos.append(normalized_data[j][i])
        data_points.append(temp_point)


def get_distance(pos_1, pos_2):
    if pos_1.__len__() == pos_2.__len__():
        dist_sum = 0
        for i in range(pos_1.__len__()):
            dist_sum += math.pow(pos_1[i] - pos_2[i], 2)
        return math.sqrt(dist_sum)
    else:
        return None


def make_centroids(num):
    for i in range(num):
        temp_centroid = Centroid()
        for j in range(normalized_data.__len__()):
            temp_centroid.pos.append(random.uniform(0.0, 1.0))
            temp_centroid.label = i
        centroids.append(temp_centroid)
    # randomly place centroids based on points


def update_point_labels():
    for i in range(data_points.__len__()):
        short_dist = 2
        label = None
        for j in range(centroids.__len__()):
            temp_dist = get_distance(data_points[i].pos, centroids[j].pos)
            if temp_dist < short_dist:
                label = centroids[j].label
                short_dist = temp_dist
        data_points[i].label = label


def update_centroid_pos():
    for i in centroids:
        temp_pos = []
        for d in range(centroids[0].pos.__len__()):  # for each dimension in centroid pos
            temp_sum = 0
            num_points = 0
            for j in data_points:
                if j.label == i.label:
                    num_points += 1
                    temp_sum += j.pos[d]
            if num_points != 0:
                temp_pos.append(temp_sum/num_points)
        i.old_pos = i.pos
        i.pos = temp_pos


def change_threshold(threshold):
    for i in centroids:
        if get_distance(i.pos, i.old_pos) > threshold:
            return False
    return True


def k_means(points_num, centroids_num, max_dist, stop=-1, plot=False, x_axis=0, y_axis=1):
    if plot:
        ax = plt.figure()

    make_points(points_num)
    make_centroids(centroids_num)

    count = 0
    if plot:
        plot_data(count, ax, x_axis, y_axis)

    while count != stop:
        count += 1
        update_point_labels()
        update_centroid_pos()
        if plot:
            plot_data(count, ax, x_axis, y_axis)
        if change_threshold(max_dist):
            break

    if plot:
        plt.show()


def make_debug_data(num):
    temp = []
    for i in range(num):
        temp.append(random.uniform(0.0, 0.4))
    for i in range(num):
        temp.append(random.uniform(0.6, 1.0))
    normalized_data.append(temp)

    temp1 = []
    for i in range(num):
        temp1.append(random.uniform(0.0, 0.4))
    for i in range(num):
        temp1.append(random.uniform(0.6, 1.0))
    normalized_data.append(temp1)

    c1 = Centroid()
    c1.label = 0
    c1.pos = [0, 0]

    c2 = Centroid()
    c2.label = 1
    c2.pos = [1.0, 1.0]

    centroids.append(c1)
    centroids.append(c2)


def plot_data(plot_num, figure, x_axis, y_axis):
    sub = figure.add_subplot(4, 4, plot_num + 1, title="Iteration " + str(plot_num))

    if plot_num != 0:
        col = ('r', 'g', 'y', 'c', 'm', 'k', 'w', '#ce6f3b')
        for i in data_points:
            sub.scatter(i.pos[x_axis], i.pos[y_axis], color=col[i.label], alpha=0.3, marker='.')
    for i in centroids:
        sub.scatter(i.pos[x_axis], i.pos[y_axis], color='b', marker='.', s=50)

    axes = plt.gca()
    axes.set_xlim([0, 1])
    axes.set_ylim([0, 1])

normalized_data = []
data_points = []
centroids = []

import_data(100)
k_means(500, 2, 0, plot=True, x_axis=1, y_axis=0)
