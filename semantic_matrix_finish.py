import numpy as np
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
matrix = np.load(input_file)
def standardize_by_strings(Matr):
    mean_by_strings = np.mean(Matr, axis=1)
    std_by_strings = np.std(Matr, axis=1)
    out_matrix = np.array([])
    for e in range(len(std_by_rows)):
        if std_by_rows[e]!=0:
            out_matrix.append((Matr[e] - mean_by_strings[e]) / std_by_strings[e])
    return out_matrix

matrix = np.log1p(matrix)
matrix = standardize_by_strings(matrix)
matrix = standardize_by_strings(matrix.T).T

np.savetxt(output_file, matrix)