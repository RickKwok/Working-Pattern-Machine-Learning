import xlrd
import csv
from sklearn.cluster import KMeans


All_Series = []
Pattern_Classes = []


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


# get all first 20 days of working temporal patterns.
def get_all_series():
    with open('all_series.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            All_Series.append(list(map(int, row[:20])))


# convert the the field of Github link into Integer representing number of class.
def get_cluster_label(pattern, num_clusters):

    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(All_Series)

    return kmeans.predict(pattern)


def _main():
    all_projects = get_all_labeled(read_sheet("Workbook1.xlsx"))

    matrix =  []
    # print all_projects[0][7:]

    get_all_series()

    for i in range(len(all_projects)):
        row = all_projects[i][7:]
        tmp = []
        for j in range(len(row)):
            if 0 < j < 4:
                continue
            else:
                if j == 0:
                    tmp.append(get_cluster_label(row[j]))
                else:
                    tmp.append(row[j])
        matrix.append(tmp)

    print matrix
