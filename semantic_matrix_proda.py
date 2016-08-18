import multiprocessing as mp
import numpy as np
import glob
import os
import sys


def complete_m(files):
    matrix = None
    for filename in files:
        if None is matrix:
            matrix = np.loadtxt(filename)
        else:
            matrix += np.loadtxt(filename)
        print 'file {} processed'.format(filename)
    return matrix


def standardize_by_rows(Matr):
    mean_by_rows = np.mean(Matr, axis=0)
    std_by_rows = np.std(Matr, axis=0)
    out_matrix = (Matr - mean_by_rows) / std_by_rows
    return out_matrix


def chunkify(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


if __name__== '__main__':
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    all_input_files = glob.glob(os.path.join(input_dir, '*'))
    num_cores = mp.cpu_count()
    chunk_size = len(all_input_files) / num_cores
    chunks = list(chunkify(all_input_files, chunk_size))

    pool = mp.Pool(processes=num_cores)
    final_result = None
    for i, result_matrix in enumerate(pool.imap_unordered(complete_m, chunks)):
        print 'Part {} processed successfully'.format(i)
        if None is final_result:
            final_result = result_matrix
        else:
            final_result += result_matrix
    pool.close()
    pool.join()

    # # Matr=np.log1p(Matr)
    # # Matr = standardize_by_rows(Matr)
    # # Matr = standardize_by_rows(Matr.T).T

    np.savetxt(output_file, final_result, fmt='%.6f')
