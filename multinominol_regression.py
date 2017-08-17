import csv
import xlrd
import numpy as np
from sklearn import linear_model
from source_data import read_sheet
from source_data import get_all_labeled

# Interface to get the feature parts in the data set.
def get_data(data_set):
    data = []
    for i in range(len(data_set)):
        try:
            data.append(list(map(float, data_set[i][:3])))
        except ValueError, e:
            print "Error", e, "at line", i
    return data


# Interface to get the label part in the data set.
def get_target(data_set):
    target = []
    for row in data_set:
        try:
            list(map(float, row[:3]))
            if row[len(row)-1] == 'True':
                target.append(1)
            else:
                target.append(0)
        except ValueError,e:
            print "error", e, "so that omit label", row[len(row)-1]
    return target

# Main function on training the model. (Need prediction part)
# vec_reader = csv.reader(open('PR_vectors.csv'))
# data_set = []
# for row in vec_reader:
#     data_set.append(row)
#
# data = get_data(data_set)
# label = get_target(data_set)
#
# Xtrain = np.array(data)
# Ytrain = np.array(label)
#
# reg = linear_model.LogisticRegression()
#
# reg.fit(Xtrain, Ytrain)


# Process training data.

test_sheet_name = 'test_data_last_semester.xlsx'

test_projects = get_all_labeled(read_sheet(test_sheet_name))

print test_projects[:][:7]


