#krivo-code
#TODODO (dodelat')
import numpy as np
import nibabel
mri = nibabel.load('mri.nii')
data = mri.get_data()

c,r,z,t=64,64,42,72
param = 200

def if_mozg(data,c,r,z,t):
    matrix = np.array(data)
    matrix = np.log1p(matrix)
    def standardize_by_rows(Matr):
        mean_by_rows = np.mean(Matr, axis=0)
        std_by_rows = np.std(Matr, axis=0)
        out_matrix = (Matr - mean_by_rows) / std_by_rows
        return out_matrix
    matrix = standardize_by_rows(matrix)
    matrix = matrix.reshape(r*c*z,t)
    ##
    Spis = []
    for e in range(c*r*z):
        f = e//(64*64)
        d = (e%(64*64))//64
        k = (e%(64*64))%64
        count = 0
        for z in range(t):
            if data[d,k,f,z] > param:
                count += 1
                break
        if count == 0:
            Spis.append(0)
        else:
            Spis.append(1)

    Spis = np.array([Spis] * 72).T
    A = np.multiply(matrix, Spis)
       ##or
    #Spis=np.array(Spis)
    #A = np.multiply(matrix.T[0], Spis)
    return A
A = if_mozg(data,c,r,z,t)
if len(sys.argv) < 3:
    print 'Sorry, usage: {} <input-dir> <output-dir>'.format(sys.argv[0])
    sys.exit(0)
input_dir = sys.argv[1]
output_dir = sys.argv[2]
all_input_files = glob.glob(os.path.join(input_dir))
input_data = [(filename, output_dir) for filename in all_input_files]


