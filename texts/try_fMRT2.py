%pylab inline
import numpy as np
import nibabel
mri = nibabel.load('/home/sirius/Downloads/chertova_fmri/_ep2d_bold_moco_2_rus_20160728153543_9.nii.gz')
data = mri.get_data()
Spis = []
cr = 0
c=64
r=64
z=42
t = 72
cr = 200
for e in range(64*64*42):
    f = e // (64*64)
    d = (e % (64*64)) // 64
    k = ((e % (64*64)) % 64)
    co = 0
    for z in range(72):
        if a[d,k,f,z] > cr:
            co += 1
    if co == 0:
        Spis.append('0')
    else:
        Spis.append('1')
for i in range(len(Spis)):
    Spis[i] = int(Spis[i])

if len(sys.argv) < 3:
    print 'Sorry, usage: {} <input-dir> <output-dir>'.format(sys.argv[0])
    sys.exit(0)
input_dir = sys.argv[3]
output_dir = sys.argv[4]
all_input_files = glob.glob(os.path.join(input_dir))