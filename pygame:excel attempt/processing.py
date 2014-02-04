import xlrd

def main():
    print organiseXL2Array('scores.xls')

def organiseXL2Array(filename):
    # Open a excel workbook and locate a sheet
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_index(0)

    # Create array of same size
    arr = [[] for x in xrange(0, sheet.nrows)]
    for e, i in enumerate(arr):
        arr[e] = [[] for y in xrange(0, sheet.ncols)]

    # Iterate through file and add to array
    for r in xrange(0, sheet.nrows):
        for c in xrange(0, sheet.ncols):
            arr[r][c] = sheet.cell(r, c).value

    return arr

if __name__ == "__main__": main()