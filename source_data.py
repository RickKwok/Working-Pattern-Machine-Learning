import xlrd
import csv
import sys
import os
from plot_commits_each_pr import dtw_distance
from plot_commits_each_pr import read_series
from sklearn.cluster import KMeans

All_Series = []

Pattern_Classes = []

DTW_WIDTH = 5

git_headers = {'Authorization': 'token %s' % os.environ['GITHUB']}

# read from Excel sheet and return matrix.
def read_sheet(sheet_name):
    wkb = xlrd.open_workbook(sheet_name)
    sheet = wkb.sheet_by_index(0)

    _matrix = []

    for row in range(sheet.nrows):
        _row = []
        for col in range(sheet.ncols):
            val = sheet.cell_value(row, col)
            if type(val) == unicode:
                val = val.encode('utf-8')
            _row.append(val)
        _matrix.append(_row)
        # print _row
        # print "\n"
    return _matrix


# helper method to exclude fields.
def within_index(n, x, y):
    if x < n < y:
        return True
    return False


def find_label(label_list):
    if label_list[3] == '' and label_list[4] == '' and label_list[5] == '':
        return True
    return False


# append the label(Success or Failure) to every entry of the feature matrix.
def get_all_labeled(_matrix):
    n = len(_matrix)
    m = len(_matrix[0])
    data = []
    for i in range(n):
        features = []
        labels = []
        for j in range(m):
            cell = _matrix[i][j]
            if within_index(j, 2, 10):
                labels.append(cell)
            else:
                features.append(cell)
        label = find_label(labels)
        features.append(label)
        data.append(features)
    return data


# Initialization. Get all first 20 days of working temporal patterns.
def get_all_series(num_clusters):
    with open('all_series.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            All_Series.append(list(map(int, row[:20])))

    km = KMeans(n_clusters=num_clusters, random_state=0).fit(All_Series)
    global Pattern_Classes
    Pattern_Classes = km.cluster_centers_


get_all_series(3)
print Pattern_Classes


# convert the the field of Github link into Integer representing number of class.
def get_series_label(git_link):
    # URL_REGEX = re.compile('https.+github.+')
    try:
        pattern = read_series(git_link)[:20]
        dist = sys.maxint
        label = -1
        # km = KMeans(n_clusters=num_clusters, random_state=0).fit(All_Series)
        for index in range(len(Pattern_Classes)):
            tmp_dist = dtw_distance(Pattern_Classes[index], pattern, DTW_WIDTH)
            if tmp_dist < dist:
                dist = tmp
                label = index
        return label
    except ValueError:
        print "Problem is " + git_link
        return -1


all_projects = get_all_labeled(read_sheet("Workbook1.xlsx"))

matrix = []

row = all_projects[0][7:]

print all_projects[0][7:]

print type(row[0])
print read_series("https://github.com/expertiza/expertiza/pull/778")
#get_all_series(3)

# for i in range(len(all_projects)):
#     row = all_projects[i][7:]
#     tmp = []
#     for j in range(len(row)):
#         if 0 < j < 4:
#             continue
#         else:
#             if j == 0:
#                 tmp.append(get_series_label(row[j]))
#             else:
#                 tmp.append(row[j])
#     matrix.append(tmp)
#
# print matrix
