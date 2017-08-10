import xlrd


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


def within_index(n, x, y):
    if x < n < y:
        return True
    return False


def find_label(label_list):
    if label_list[3] == '' and label_list[4] == '' and label_list[5] == '':
        return True
    return False


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


matrix = read_sheet("Workbook1.xlsx")

print matrix[0]

all_projects = get_all_labeled(matrix)

print all_projects[0]