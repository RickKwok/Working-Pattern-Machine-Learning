import xlrd


def read_sheet():
    wkb = xlrd.open_workbook("Workbook1.xlsx")
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


_matrix = read_sheet()


def within_label(n):
    return False


def find_label(list):
    return False


def get_all_labeled(_matrix):
    n = len(_matrix)
    m = len(_matrix[0])
    all_projects = {}
    for i in range(n):
        tmp = []
        labels = []
        for j in range(m):
            cell = _matrix[i][j]
            if within_label(j):
                labels.append(cell)
            else:
                tmp.append(cell)
        label = find_label(labels)
        all_projects[tmp] = label
    return all_projects
