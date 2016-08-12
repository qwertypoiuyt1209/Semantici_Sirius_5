# -*- coding: utf-8 -*-

from joblib import Parallel, delayed
import numpy as np


def tokenize_text(paragraphs):
    """

    :param paragraphs: list of long strings (multiple words in each)
    :return:
    """
    words = []
    for paragraph in paragraphs:
        words.extend(paragraph.split())
    return words


def standardize_by_rows(Matr):
    mean_by_rows = np.mean(Matr, axis=0)
    std_by_rows = np.std(Matr, axis=0)
    out_matrix = (Matr - mean_by_rows) / std_by_rows
    return out_matrix


def compute_semantic_matrix(basis_filename, story_filename, corpus_filename, window_size):
    # TODO
    # 1. rename one-letter variables
    # 2. use WITH to work with files:
    #     https://pythonworld.ru/osnovy/with-as-menedzhery-konteksta.html

    """Compute the semantic matrix.

    :param corpus_filename: name of the corpus file
    :param story_filename: name of the file with story (one per line)
    :param basis_filename: name of the file with basis words (one per line)
    :param window_size: size of the window to use for searching the co-occurence.
    :return:
    """
    with open(basis_filename) as basis_file:
        basis_words = [i.strip() for i in basis_file.readlines()]

    with open(story_filename) as story_file:
        story_paragraphs = [i.strip() for i in story_file.readlines()]

    story_words = tokenize_text(story_paragraphs)
    story_words = sorted(set(story_words))
    # for e in story_words:
    #     if len(e)==1 and e!=u'я':
    #         story_words.pop(story_words.index(e))

    with open(corpus_filename) as corpus_file:
        corpus_paragraphs = [i.strip() for i in corpus_file.readlines()]

    corpus_words = tokenize_text(corpus_paragraphs)

    num_basis_words = len(basis_words)
    num_story_words = len(story_words)
    num_corpus_words = len(story_words)
    matrix = np.zeros((num_basis_words, num_story_words))
    for j in xrange(num_basis_words):
        for i in xrange(num_corpus_words - window_size):
            if basis_words[j] in corpus_words[i:i + window_size + 1]:
                for e in xrange(num_story_words):
                    if story_words[e] in corpus_words[i:i + window_size + 1]:
                        matrix[j][e] += 1

    matrix=np.log1p(matrix)
    # matrix = standardize_by_rows(matrix)
    # matrix = standardize_by_rows(matrix.T).T
    return matrix
                       
 
if __name__== '__main__':
    basis_filename = 'basis.txt'
    story_filename = 'story.txt'
    corpus_filenames = ['text1.txt', 'text2.txt', 'text3.txt', 'text4.txt']
    window_size = 30
    with Parallel(n_jobs=4) as parallel:
        r=parallel(
            delayed(compute_semantic_matrix)(basis_filename,
                                             story_filename,
                                             corpus_filename,
                                             window_size)
            for corpus_filename in corpus_filenames
        )
        print(r)
