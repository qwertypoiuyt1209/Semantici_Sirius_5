from joblib import Parallel, delayed
import pymorphy2
import re


def norm(text):
    '''Убирает знаки препинания'''
    for i in range(len(text)):
        text[i]=re.sub('[^\w\s]', '', text[i], flags=re.U)
    return text


def norm2(corpus):
    '''в начальную форму'''
    norm_corpus=[]
    for e in range(len(corpus)):
        A = pymorphy2.MorphAnalyzer()
        corpus[e] = A.parse(corpus[e])[0].normal_form
        if (A.parse(corpus[e])[0].tag.POS is not 'PRCL'  and
            'PREP' not in A.parse(corpus[e])[0].tag and
            'CONJ' not in A.parse(corpus[e])[0].tag and
            'UNKN' not in A.parse(corpus[e])[0].tag and
            'LATN' not in A.parse(corpus[e])[0].tag):
            norm_corpus.append(corpus[e])
    return norm_corpus


if __name__=='__main__':
    with open('text2.txt','r') as text:
        C = [i.strip() for i in text.readlines()]
    with Parallel(n_jobs = 2) as parallel:
        corpus=[]
        for e in range(len(C)):
            corpus.extend(C[e].split())
        N=parallel(delayed(norm2)(norm(corpus)) for i in range(1))
        print(N)
