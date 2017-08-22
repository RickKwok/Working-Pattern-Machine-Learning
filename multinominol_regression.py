import csv
import xlrd
import numpy as np
from sklearn import linear_model
from source_data import read_sheet
from source_data import get_all_labeled
from source_data import get_series_label
from plot_commits_each_pr import read_series

ROOT_URL = 'https://api.github.com/repos/expertiza/expertiza/pulls/'


# Interface to get the feature parts in the data set.
def get_data(data_set):
    data = []
    for i in range(len(data_set)):
        try:
            data.append(list(map(float, data_set[i][:3])))
        except ValueError, e:
            print "Error", e, "so omit the feature at line", i
    return data


# Interface to get the label part in the data set.
def get_target(data_set):
    target = []
    for row in data_set:
        try:
            list(map(float, row[:3]))
            if row[len(row) - 1] == 'True':
                target.append(1)
            else:
                target.append(0)
        except ValueError, e:
            print "error", e, "so that omit label", row[len(row) - 1]
    return target


def parse_to_api_link(pr_link):
    num = 0
    for x in pr_link.split('/'):
        if x.isdigit():
            num = x
    git_link = ROOT_URL + num
    return git_link


def get_test_data(test_projects):
    writer = csv.writer(open("test_data.csv", "wb"))
    test_data = []
    test_data_label = []
    for row in test_projects:
        tmp = [get_series_label(parse_to_api_link(row[7])), row[8], row[9]]
        test_data.append(tmp)
        test_data_label.append(row[len(row)-1])
        tmp.append(row[len(row)-1])
        writer.writerow(tmp)

######### Process Test data into nx4 matrix.

# tmp = get_all_labeled(read_sheet("test_data_last_semester.xlsx"))
#
# test_projects = []
#
# writer = csv.writer(open("test_data.csv", "wb"))
#
# for row in tmp:
#     row[7] = get_series_label((parse_to_api_link(row[7])))
#     test_projects.append(row[7:])
#
# print test_projects
# writer.writerows(test_projects)

########## Run Prediction.

vec_reader = csv.reader(open('PR_vectors.csv'))
test_reader = csv.reader(open('test_data.csv'))
train_set = []
test_set = []
for row in vec_reader:
    train_set.append(row)

for row in test_reader:
    test_set.append(row)

data = get_data(train_set)
label = get_target(train_set)

t_data = get_data(test_set)
t_label = get_target(test_set)

x_train = np.array(data)
y_train = np.array(label)

x_test = np.array(t_data)
y_test = np.array(t_label)

reg = linear_model.LogisticRegression()

reg.fit(x_train, y_train)

print reg.densify()
print reg.coef_

predict_res = []

for i in range(0, len(x_test)):
    predict_res.append(int(reg.predict(x_test[i])))

print "Predicted results are", predict_res
print "Test labels are", y_test

success_in_total = 0

for i in y_test:
    success_in_total += i

inaccurate = 0

for i in range(0, len(y_test)):
    if y_test[i] == 0:
        if predict_res[i] == 1:
            inaccurate += 1

print "Number of inaccurate is", inaccurate, "out of", len(y_test), "all projects."


# test_sheet_name = 'test_data_last_semester.xlsx'
#
# test_projects = get_all_labeled(read_sheet(test_sheet_name))
#
# # print test_projects[3][7]
# # print read_series(parse_to_api_link(test_projects[3][7]))
#
# test_data = []
# test_data_label = []
#
# # Main function on training the model. (Need prediction part)
#
# get_test_data()
#
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
#
# res = []
#
# print reg.predict(test_data[0])
# for cur in test_data:
#     res.append(reg.predict(cur))
#
# acc = 0
#
# for i in len(res):
#     if res[i] == test_data_label:
#         acc += 1
#
# print acc/len(res)
