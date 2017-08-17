import csv


def get_data(data_set):
    data = []
    for row in data_set:
        tmp = []
        j = 0
        while j < len(row)-1:
            if len(row[j]) == 0:
                tmp.append(0)
            else:
                try:
                    tmp.append(int(row[j]))
                except ValueError:
                    tmp.append(0)
            j += 1
        data.append(tmp)
    return data


def get_target(data_set):
    target = []
    for row in data_set:
        if row[len(row)-1] == 'True':
            target.append(1)
        else:
            target.append(0)
    return target


vec_reader = csv.reader(open('PR_vectors.csv'))
data_set = []
for row in vec_reader:
    data_set.append(row)

data = get_data(data_set)
label = get_target(data_set)

print len(data)
print len(label)
