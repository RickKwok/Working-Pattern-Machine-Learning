import pandas as pd
import sys, os, csv
import collections
import math
import matplotlib.pyplot as plt
import random
import re
import requests
import numpy as np
from datetime import datetime
from collections import Counter
from sklearn.cluster import KMeans

URL_REGEX = re.compile('https.+github.+')
DTW_WIDTH = 5
git_headers = {'Authorization': 'token %s' % os.environ['GITHUB']}


# Filter the urls of the pull requests and store into list.

def get_url_list():
    url_list = []

    with open('pull_requests', 'rb') as f:
        for line in f:
            line = line.strip()
            if URL_REGEX.match(line):
                url_list.append(line)

    return url_list


# Interacting with Github API by making get requests from the urls.

def read_series(url):
    files_url = url + "/files"
    commits_url = url + "/commits?500"

    commiters = []
    date = []

    r_commits = requests.get(commits_url, headers=git_headers).json()
    r_files = requests.get(files_url, headers=git_headers).json()

    num_files_changed = len(r_files)
    for c in r_commits:
        # commiters.append(c["author"]["login"])
        try:
            date.append(c["commit"]["author"]["date"])
        except TypeError:
            print ("url: " + c + ", has problem.")
            continue

    for i in range(0, len(date)):
        date[i] = datetime.strptime(date[i][:10], "%Y-%m-%d")

    dict_hash = Counter(date)
    # base = datetime(2016, 11, 9)
    # end = datetime(2016, 12, 16)

    # Stretch the timeframe into project period/ 35 days.
    date_list = pd.date_range('2016-11-9', periods=35, freq='D')

    for i in date_list:
        i = i.to_pydatetime()
        if i in dict_hash.keys():
            continue
        else:
            dict_hash[i] = 0

    # sort {date : num_commits} hash into ascending date order.

    dict_hash = collections.OrderedDict(sorted(dict_hash.items()))

    # plot {x : date, y : num_commits} using Matplot.

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


# Calculate similarity between two time series. Using Dynamic Time Wrapping.

def dtw_distance(s1, s2, w):
    DTW = {}
    w = max(w, abs(len(s1) - len(s2)))

    for i in range(-1, len(s1)):
        for j in range(-1, len(s2)):
            DTW[(i, j)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(max(0, i - w), min(len(s2), i + w)):
            dist = (int(s1[i]) - int(s2[j])) ** 2
            DTW[(i, j)] = dist + min(DTW[(i - 1, j)], DTW[(i, j - 1)], DTW[(i - 1, j - 1)])

    return math.sqrt(DTW[len(s1) - 1, len(s2) - 1])


# Using LB_Keogh to Optimize DTW efficiency.

def LB_Keogh(s1, s2, r):
    LB_sum = 0
    for ind, i in enumerate(s1):

        lower_bound = min(s2[(ind - r if ind - r >= 0 else 0):(ind + r)])
        upper_bound = max(s2[(ind - r if ind - r >= 0 else 0):(ind + r)])

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


# url_list = get_url_list()
# writer = csv.writer(open("all_series.csv", "wb"))
#
# for i in url_list:
#     tmp = read_series(i)
#     writer.writerow(tmp)

# print dtw_distance(read_series(url_list[0]), read_series(url_list[1]), 5)

Distance_Matrix = []
All_Series = []

# Calculating Distance Matrix.

# writer = csv.writer(open("dist_matrix.csv", "wb"))
#
# with open('all_series.csv') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         All_Series.append(row)
#
# # print dtw_distance(All_Series[0], All_Series[1], 5)
#
# for i in range(0, len(All_Series)):
#     s1 = All_Series[i][:20]
#     tmp = []
#     for j in range(0, len(All_Series)):
#         dist = 0
#
#         if i < j:
#             s2 = All_Series[j][:20]
#             dist = dtw_distance(s1, s2, DTW_WIDTH)
#
#         print dist,
#         tmp.append(dist)
#     writer.writerow(tmp)
#     # Distance_Matrix.append(tmp)
#     print "\n"

# with open('dist_matrix.csv') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         Distance_Matrix.append(row)

# print read_series("https://api.github.com/repos/expertiza/expertiza/pulls/236")[:20]

with open('all_series.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        All_Series.append(list(map(int, row[:20])))

        # print All_Series

kmeans = KMeans(n_clusters=3, random_state=0).fit(All_Series)

centroids = kmeans.cluster_centers_

for center in centroids:
    print dtw_distance(center, All_Series[0], 5)
