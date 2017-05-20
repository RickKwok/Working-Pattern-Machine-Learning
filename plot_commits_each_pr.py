import pandas as pd
import sys, os
import collections
import math
import matplotlib.pyplot as plt
import random
from datetime import datetime
from collections import Counter
import tensorflow as tf


def read_series(filename):
    data = pd.read_csv("./commits_data/" + filename)
    # commiters = data['commit.author.name']
    date = data['commit.author.date']

    for i in range(0, len(date)):
        date[i] = datetime.strptime(date[i][:10], "%Y-%m-%d")

    dict_hash = Counter(date)
    # base = datetime(2016, 11, 9)
    # end = datetime(2016, 12, 16)
    date_list = pd.date_range('2016-11-9', periods=35, freq='D')

    for i in date_list:
        i = i.to_pydatetime()
        if i in dict_hash.keys():
            continue
        else:
            dict_hash[i] = 0

    dict_hash = collections.OrderedDict(sorted(dict_hash.items()))
    # x = dict_hash.keys()
    # y = dict_hash.values()
    # print(x)
    # print(y)
    # could change to plt.plot_data() if want threads
    # plt.scatter(x, y)
    # plt.plot(x, y)
    # plt.title("Commits change on PR_" + sys.argv[1])
    # plt.ylabel("Number of commits")
    # plt.grid(True)
    # plt.show()
    return dict_hash.values()


def get_all_commits():
    path = "./commits_data/"
    commit_list = os.listdir(path)[1:]
    print(commit_list)
    return commit_list


def dtw_distance(s1, s2, w):
    DTW = {}
    w = max(w, abs(len(s1) - len(s2)))

    for i in range(-1, len(s1)):
        for j in range(-1, len(s2)):
            DTW[(i, j)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(max(0, i - w), min(len(s2), i + w)):
            dist = (s1[i] - s2[j]) ** 2
            DTW[(i, j)] = dist + min(DTW[(i - 1, j)], DTW[(i, j - 1)], DTW[(i - 1, j - 1)])

    return math.sqrt(DTW[len(s1) - 1, len(s2) - 1])


def LB_Keogh(s1, s2, r):
    LB_sum = 0
    for ind, i in enumerate(s1):

        lower_bound = math.min(s2[(ind - r if ind - r >= 0 else 0):(ind + r)])
        upper_bound = math.max(s2[(ind - r if ind - r >= 0 else 0):(ind + r)])

        if i > upper_bound:
            LB_sum = LB_sum + (i - upper_bound) ** 2
        elif i < lower_bound:
            LB_sum = LB_sum + (i - lower_bound) ** 2

    return math.sqrt(LB_sum)


def k_means_clust(data, num_clust, num_iter, w=5):
    centroids = random.sample(data, num_clust)
    counter = 0
    for n in range(num_iter):
        counter += 1
        print(counter)
        assignments = {}
        # assign data points to clusters
        for ind, i in enumerate(data):
            min_dist = float('inf')
            closest_clust = None
            for c_ind, j in enumerate(centroids):
                if LB_Keogh(i, j, 5) < min_dist:
                    cur_dist = dtw_distance(i, j, w)
                    if cur_dist < min_dist:
                        min_dist = cur_dist
                        closest_clust = c_ind
            if closest_clust in assignments:
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust] = []

        # recalculate centroids of clusters
        for key in assignments:
            clust_sum = 0
            for k in assignments[key]:
                clust_sum = clust_sum + data[k]
            centroids[key] = [m / len(assignments[key]) for m in clust_sum]

    return centroids


commit_list = get_all_commits()
s1 = read_series(commit_list[0])
s2 = read_series(commit_list[10])
print(dtw_distance(s1, s2, 5))
