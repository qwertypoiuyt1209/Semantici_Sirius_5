# -*- coding: utf-8 -*-
from joblib import Parallel, delayed
import multiprocessing as mp
import pymorphy2
import re
import glob
import os
import sys

FORBIDDEN_TAGS = ['PRCL', 'PREP', 'CONJ', 'UNKN', 'LATN']


def norm2(data):
    filename, output_dir = data
    with open(filename, 'r') as text:
        rawtext = [i.strip() for i in text.readlines()]

    def stage1(rawfile):
        n_text = []
        for e in xrange(len(rawfile)):
            n_text.extend(rawfile[e].split())
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

    output_filename = os.path.join(output_dir, os.path.basename(filename))
    with open(output_filename, 'w') as text:
        text.write(' '.join(norm_corpus).encode('utf-8'))
    return output_filename


if __name__ == '__main__':
    # with open('text5.txt', 'r') as story:
    #     C = [i.strip() for i in story.readlines()]
    #
    # with Parallel(n_jobs=8) as parallel:
    #
    #     if len(sys.argv) < 3:
    #         print 'Sorry, usage: {} <input-dir> <output-dir>'.format(sys.argv[0])
    #         sys.exit(0)
    #     input_dir = sys.argv[1]
    #     output_dir = sys.argv[2]
    #     all_input_files = glob.glob(os.path.join(input_dir, '*.txt'))
    #     for file in all_input_files:
    #         with open(file, 'r') as text:
    #             D = [i.strip() for i in text.readlines()]
    #             M = parallel(delayed(norm2)(D) for i in rande(1))
    #         with open('text.txt', 'w') as text:
    #             for paragraph in M:
    #                 text.write(' '.join(paragraph).encode('utf-8'))
    #
    #     N = parallel(delayed(norm2)(C) for corpus1 in range(1))
    #
    # with open('story.txt','w') as stories:
    #     for paragraph in N:
    #         stories.write(' '.join(paragraph).encode('utf-8'))
    #
    #

    if len(sys.argv) < 3:
        print 'Sorry, usage: {} <input-dir> <output-dir>'.format(sys.argv[0])
        sys.exit(0)
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    all_input_files = glob.glob(os.path.join(input_dir, '*.txt'))

    # import cProfile
    #
    # pr = cProfile.Profile()
    # pr.enable()
    input_data = [(filename, output_dir) for filename in all_input_files]
    # norm2(input_data[0])
    # pr.disable()
    # # after your program ends
    # pr.print_stats(sort="calls")

    pool = mp.Pool(processes=8)
    for result_filename in pool.imap_unordered(norm2, input_data):
        print 'Converted {} successfully'.format(result_filename)
    pool.close()
    pool.join()
