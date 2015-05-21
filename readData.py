import csv

def read_to_list( file_name ):
    with open( file_name ) as f:
        reader = csv.reader(f, delimiter=' ')
        matrix = [word for word in [row for row in reader]]
    matrix2 = []
    for row in matrix:
        for entry in row:
            if entry == '':
                row.remove(entry)
        row = [float(i) for i in row]
        matrix2.append(row)
    return matrix2
