import nltk
import re
import sys
import os
import glob

input_dir = sys.argv[1]
output_dir = sys.argv[2]
all_input_files = glob.glob(os.path.join(input_dir, '*'))

def normalize(in_filename, output_dir):
    with open(in_filename) as file:
        raw_text = [i.strip() for i in file.readlines()]
    text = []
    for e in range(len(raw_text)):
        text.extend(re.split(r'\W+', raw_text[e]))
    wnl = nltk.WordNetLemmatizer()
    text = [wnl.lemmatize(t) for t in text]

    out_filename = os.path.join(output_dir, os.path.basename(in_filename))
    with open(out_filename,'w') as out_file:
        outfile.write(' '.join(text))
    return text
for in_file in all_input_files:
    A = normalize(in_file,output_dir)
    print('file {} OK'.format(in_file))

