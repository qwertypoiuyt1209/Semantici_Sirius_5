
import numpy as np
import nibabel
import sys
import os
import glob


def if_mozg(files):
    in_filename,output_dir,mask_dir = files
    mri = nibabel.load(in_filename)
    data = mri.get_data()

    c, r, z, t = data.shape #64, 64, 42, 72
    matrix = data.reshape(r * c * z, t)
    param = 500
    Spis = []
    for e in range(c * r * z):
        f = e // (64 * 64)
        d = (e % (64 * 64)) // 64
        k = (e % (64 * 64)) % 64
        count = 0
        for z in range(t):
            if data[d, k, f, z] > param:
                count += 1
                break
        if count == 0:
            Spis.append(0)
        else:
            Spis.append(1)

    def standardize_by_rows(Matr):
        mean_by_rows = np.mean(Matr, axis=0)
        std_by_rows = np.std(Matr, axis=0)
        out_matrix = (Matr - mean_by_rows) / std_by_rows
        return out_matrix
    matrix = standardize_by_rows(matrix)



    Spis = np.array([Spis]*t).T
    A = np.multiply(matrix, Spis)
    output_filename = os.path.join(output_dir, os.path.basename(in_filename))
    np.savetxt(output_filename, A, '%.6f')
    mask_filename = os.path.join(mask_dir, os.path.basename(in_filename))
    np.savetxt(mask_filename, Spis.T[0], '%.6f')
    # Spis=np.array(Spis)
    # A = np.multiply(matrix.T[0], Spis)

    return A, Spis.T[0]

if len(sys.argv) < 3:
    print 'Sorry, usage: {} <input-dir> <output-dir>'.format(sys.argv[0])
    sys.exit(0)
input_dir = sys.argv[1]
output_dir = sys.argv[2]
mask_dir = sys.argv[3]
all_input_files = glob.glob(os.path.join(input_dir, '*'))
# input_data = [(filename, output_dir,mask_dir) for filename in all_input_files]
print all_input_files
# print input_data
for file in all_input_files:
    input_data = (file,output_dir,mask_dir)
    Some, mask = if_mozg(input_data)

    # mask=mask.tolist()
    # s=''
    # for i in range(len(mask)):
    #     s+=str(abs(round(mask[i],1)))+' '
    # for e in range(0,64*64*42*4,64*4):
    #     print s[e:e+64*4]

# Some=Some.tolist()
# s=''
# for i in range(len(Some)):
#     s+=str(abs(round(Some[i],1)*10))+' '
# for e in range(0,64*64*42*4,64*4):
#     print s[e:e+64*4]






