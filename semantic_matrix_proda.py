import numpy as np
import glob
import os


input_dir = sys.argv[1]
output_file = sys.argv[2]
Matr=np.array()
a,b=
def complete_m(filename,Matr):
    Matr.append(np.load(filename))
    return Matr

def standardize_by_rows(Matr):
    mean_by_rows = np.mean(Matr, axis=0)
    std_by_rows = np.std(Matr, axis=0)
    out_matrix = (Matr - mean_by_rows) / std_by_rows
    return out_matrix


all_input_files=glob.glob(os.path.join(input_dir,'*'))
for file in all_input_files:
    Matr=complete_m(file,Matr)

Matr=standardize_by_rows(Matr)
np.savetxt(output_file,Matr)



