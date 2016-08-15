import numpy as np
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
matrix = np.load(input_file)
def standardize_by_rows(Matr):
    mean_by_rows = np.mean(Matr, axis=0)
    std_by_rows = np.std(Matr, axis=0)
    out_matrix = (Matr - mean_by_rows) / std_by_rows
    return out_matrix

matrix=standardize_by_rows(matrix)
matrix=standardize_by_rows(matrix.T).T

np.savetxt(output_file, matrix)