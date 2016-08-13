import pymorphy2
import re
import glob
import os
import sys

FORBIDDEN_TAGS = ['PRCL', 'PREP', 'CONJ', 'UNKN', 'LATN']


def norm2(data):
    filename, output_filename = data[0]
    with open(filename, 'r') as text:
        rawtext = [i.strip() for i in text.readlines()]

    def stage1(rawfile):
        n_text = []
        for e in xrange(len(rawfile)):
            n_text.append(rawfile[e].split()[1])
        for e in xrange(len(n_text)):
            n_text[e] = n_text[e].decode('utf-8')
        return n_text
    text = stage1(rawtext)
    def norm(text):
        for i in xrange(len(text)):
            text[i] = re.sub('[^\w\s]', '', text[i], flags=re.U)
            text[i] = text[i].encode('utf-8')
        return text
    corpus = norm(text)
    norm_corpus = []
    analyzer = pymorphy2.MorphAnalyzer()
    for e in xrange(len(corpus)):
        corpus[e] = corpus[e].decode('utf-8')
        parsed_value = analyzer.parse(corpus[e])[0]
        corpus[e] = parsed_value.normal_form
        if all(tag not in parsed_value.tag for tag in FORBIDDEN_TAGS):
            norm_corpus.append(corpus[e])
    return norm_corpus


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print 'Sorry, usage: {} <input-dir> <output-dir>'.format(sys.argv[0])
        sys.exit(0)
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    all_input_files = glob.glob(os.path.join(input_dir))

    input_data = [(filename, output_dir) for filename in all_input_files]
    A=norm2(input_data)
    with open(output_dir, 'w') as text:
        text.write(' '.join(A).encode('utf-8'))

