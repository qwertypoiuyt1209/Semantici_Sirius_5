import os
import sys
import glob

from lxml import etree


def main(input_dir, output_dir):
    all_input_files = glob.glob(os.path.join(input_dir, '*.fb2'))
    for filename in all_input_files:
        print filename
        file_content = open(filename).read()
        try:
            e = etree.XML(file_content)
        except:
            print 'WARNING: File {} cannot be opened!'.format(filename)
            continue

        file_output_content = "".join([x for x in e.itertext()])
        output_filename = os.path.join(output_dir, os.path.basename(filename) + '.txt')
        with open(output_filename, 'w') as output_file:
            output_file.write(file_output_content.encode('utf-8'))
        print 'File {} converted'.format(filename)


if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    print input_dir, output_dir
    main(input_dir, output_dir)
