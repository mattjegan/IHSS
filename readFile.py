import xlrd

# Open a excel workbook and locate a sheet
book = xlrd.open_workbook('scores.xls')
sheet = book.sheet_by_index(0)

# Display dimensions
print sheet.nrows
print sheet.ncols

# Create array of same size
arr = [[] for x in xrange(0, sheet.nrows)]
for e, i in enumerate(arr):
    arr[e] = [[] for y in xrange(0, sheet.ncols)]

# Iterate through file and add to array
for r in xrange(0, sheet.nrows):
    for c in xrange(0, sheet.ncols):
        arr[r][c] = sheet.cell(r, c).value

# Print arr in a pretty way
s = [[str(e) for e in row] for row in arr]
lens = [len(max(col, key=len)) for col in zip(*s)]
fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
table = [fmt.format(*row) for row in s]
print '\n'.join(table)