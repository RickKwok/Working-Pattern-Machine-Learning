import xlrd
import csv
import sys
import os
import re
from plot_commits_each_pr import dtw_distance
from plot_commits_each_pr import read_series
from sklearn.cluster import KMeans

# Global Variable
All_Series = []

Pattern_Classes = []

DTW_WIDTH = 5

git_headers = {'Authorization': 'token %s' % os.environ['GITHUB']}

ROOT_URL = 'https://api.github.com/repos/expertiza/expertiza/pulls/'


# Initialization. Get all first 20 days of working temporal patterns. Need to run beforehand to set the global variable
# "Pattern Classes".
def get_all_series(num_clusters):
    with open('all_series.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            All_Series.append(list(map(int, row[:20])))

    km = KMeans(n_clusters=num_clusters, random_state=0).fit(All_Series)
    global Pattern_Classes
    Pattern_Classes = km.cluster_centers_


# read from Excel sheet and return matrix.
def read_sheet(sheet_name, sheet_number):
    wkb = xlrd.open_workbook(sheet_name)
    sheet = wkb.sheet_by_index(sheet_number)

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


# convert the the field of Github link into Integer representing number of class.
# 0th column of the training data matrix (PR_vectors.csv).
def get_series_label(git_link):
    URL_REGEX = re.compile('https.+github.+')
    if URL_REGEX.match(git_link):
        num = 0
        for x in git_link.split('/'):
            if x.isdigit():
                num = x
        link = ROOT_URL + num
        pattern = read_series(link)[:20]

        dist = sys.maxint
        label = -1

        for center in Pattern_Classes:
            tmp_dist = dtw_distance(center, pattern, DTW_WIDTH)
            if tmp_dist < dist:
                dist = tmp_dist
                label += 1
        return label
    else:
        print 'Not Github url.'
        return -1


# Process the read in excel sheet and convert the GITHUB link to a temporal class label.
# And write to "PR_vectors.csv". Need to call "get_all_labeled" before this to append label to the end of each row.
def get_vector_for_regression(all_projects):
    writer = csv.writer(open("PR_vectors.csv", "a"))
    git_url_regex = re.compile('https.+github.+')
    for i in range(119, len(all_projects)):
        row = all_projects[i][7:]
        if git_url_regex.match(row[0]):
            link = get_series_label(row[0])
            tmp = [link, row[4], row[5], row[6]]
            print tmp
            writer.writerow(tmp)
        else:
            continue


# get_all_series(3)
# print Pattern_Classes

# projects = read_sheet("Workbook1.xlsx", 1)
# print len(projects)
# print projects
#
# writer = csv.writer(open("new_train_set_3_series_types", "wb"))
# for row in projects:
#     series_label = get_series_label(row[1])
#     if row[3] == '':
#         label = 0
#     if row[3] == 'P':
#         label = 1
#     else:
#         label = 2
#     tmp = [series_label, row[4], row[5], label]
#     writer.writerow(tmp)
#     print tmp

# print get_all_labeled(projects)
# get_vector_for_regression(get_all_labeled(projects))
# print type(get_all_labeled(projects)[0][7])
# print read_series('https://api.github.com/repos/expertiza/expertiza/pulls/388')

