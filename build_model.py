#-*- coding: utf-8-*-
import sys
import multiprocessing as mp
from itertools import izip
from sklearn.linear_model import LinearRegression
#from sklearn import linear_model
import numpy as np
# Time_words = open('Time_words.txt', 'r', encoding='utf-8') #Данные от швейцаров (текст)
# A1 = Time_words.readlines()
#
# sc=0 # счетчик столбцов
# ssc = 0 # обозначает\определяет промежуток
# Matrix_TW = [[0]*3 for i in range (len(A1))] #Матрица соответствия слова и времени его произношения
# for j in range(len(A1)):
#     pr1 = A1[j].find(' ') #Ищем первый пробел
#     pr2 = A1[j].rfind(' ') #Ищем последний пробел
#     Matrix_TW[j][0] = int(A1[j][:pr1]) #первому элементу матрицы присваиваем набор символов до первого пробела
#     Matrix_TW[j][1] = int(A1[j][pr1+1:pr2]) #второму элементу матрицы присваиваем набор символов с первого пробела до последнего
#     if j==len(A1)-1: #Убираем \n
#         Matrix_TW[j][2] = A1[j][pr2+1:]
#     else:
#         Matrix_TW[j][2] = A1[j][pr2+1:len(A1[j])-1]
#         i=0
# ###
#
# ###
#
# scet1 = 0
# Dop_mass = [[0]*2 for i in range (30000)] #Дополнительный массив
# while i<len(Matrix_TW): #определяем расположение слово относительно двух границ временного промежутка: рассматриваем 4 случая
#     if Matrix_TW[i][0]>ssc*3000 and Matrix_TW[i][1]<(ssc+1)*3000: #слово полностью содержится в одном промежутке
#         sc+=1
#         Dop_mass[scet1][0]=ssc+1
#         Dop_mass[scet1][1]=(Matrix_TW[i][2])
#         scet1+=1
#         i+=1
#     elif Matrix_TW[i][0]>ssc*3000 and Matrix_TW[i][1]>(ssc+1)*3000:
#         sc+=1
#         Dop_mass[scet1][0]=ssc+1
#         Dop_mass[scet1][1]=Matrix_TW[i][2]
#         ssc+=1
#         scet1+=1
#     elif Matrix_TW[i][0]<ssc*3000 and Matrix_TW[i][1]>(ssc+1)*3000:
#         sc+=1
#         ssc+=1
#         Dop_mass[scet1][0]=ssc+1
#         Dop_mass[scet1][1]=Matrix_TW[i][2]
#         scet1+=1
#     else:
#         sc+=1
#         Dop_mass[scet1][0]=ssc+1
#         Dop_mass[scet1][1]=Matrix_TW[i][2]
#         i+=1
#         scet1+=1
#
# Ok_matr = [[0]*sc for i in range (1004)] #Окончательная матрица
#
# with open(story_file, encoding='utf-8') as kslov: #Данные от швейцаров (корпус нормализованных слов)
#     story_words = kslov.read().strip().split()
# Dicts = dict()
#
#
# #### ??????!!!!!
# for i in range (len(story_words)): # файл => словарь
#     pr1 = story_words[i].find(' ')
#     if i==len(story_words)-1:
#         Dicts[story_words[i][pr1 + 1:]]=int(story_words[i][:pr1])
#     else:
#         Dicts[story_words[i][pr1 + 1:len(story_words[i]) - 1]] = int(story_words[i][:pr1])
# #### ??????!!!!!
#
# srez_slov = open('srez_slov.txt', 'r', encoding='utf-8') #Данные от левых
# A3 = srez_slov.readlines()
# for i in range (len(A3)):
#     A3[i].rstrip()
# A32 = []
# for i in range (len(A3)): #файл => двумерный массив
#     A32.append(list(map(float, A3[i].split())))
# priz_slovo = open('priz_slovo.txt', 'r') #Данные семантиков
# A3 = priz_slovo.readlines()
# for i in range (len(A3)):
#     A3[i].rstrip()
# A33 = []
# for i in range (len(A3)): #файл => двумерный массив
#     A33.append(list(map(float, A3[i].split())))
#
#
# ###########################################################################
# Dop_mass = np.array(Dop_mass)
# Dop_mass = Dop_mass.T #Транспонируем
# for s in range (len(Ok_matr[0])):
#     Ok_matr[0][s]=int(Dop_mass[0][s])
#     Ok_matr[1][s]=A32[1][Ok_matr[0][s]-1]
#     #print(Ok_matr[1002][s])
#     Ok_matr[1002][s]=Dop_mass[1][s]
#     sqq = Dicts[Ok_matr[1002][s]]
#     for k in range (0,1000):
#         Ok_matr[k+2][s] = A33[k+1][sqq-1]
#
# #print(Ok_matr)
#
# #------
#
# #############################################################################
#
# X_train = [[0]*sc for i in range (len(Ok_matr)-3)]
#
# cl = 0
# for i in range (1,len(Ok_matr)-2):
#     X_train[cl] = Ok_matr[i]
#     cl += 1
# X_train = np.array(X_train)
# X_train = X_train.T
from sklearn.linear_model import Ridge


def linear_regressor(X_train, y_train, Ok_matr):
    # y_train = [[0]*3 for i in range (sc)] #*2-требует изменения(кол-во врем. промежутков для каждого слова)
    # #print(y_train)
    #
    # cl=0 # счетчик строк в y_train
    # for j in Ok_matr[0]:
    #     y_train[cl] = data[j-1]
    #     cl += 1
    #
    # y_train = np.array(y_train)
    # #print(y_train) #создан ок.вар y_train
    #
    #
    #

    lr = LinearRegression(fit_intercept=False)
    lr.fit(X_train, y_train)
    return lr.coef_
#
# data = np.loadtxt('X1.txt') #первый испытуемый
# data = data.T
# lreg = linear_regressor(X_train, data, Ok_matr)
#
# data = np.loadtxt('X2.txt')#второй
# data = data.T
# lreg = linear_regressor(X_train, data, Ok_matr)
#
# data = np.loadtxt('X3.txt')#3
# data = data.T
# lreg = linear_regressor(X_train, data, Ok_matr)
#
# data = np.loadtxt('X4.txt')#4
# data = data.T
# print(linear_regressor(X_train, data, Ok_matr))
#

def linear_regressor_with_regularization(X_train, y_train, voxel_id):
    lr = Ridge(alpha=1e2,  fit_intercept=False)
    lr.fit(X_train, y_train)
    return voxel_id, lr.coef_


def linear_regressor_with_regularization_wrapper(data):
    X_train, y_train, voxel_id = data
    return linear_regressor_with_regularization(X_train, y_train, voxel_id)


if __name__ == '__main__':
    alignment_file = sys.argv[1]
    semantic_file = sys.argv[2]
    fmri_file = sys.argv[3]
    model_file = sys.argv[4]
    with open(alignment_file, 'r') as time_word:
        Time_word = [i.strip() for i in time_word.readlines()]
        Time_Word = []
        Words = []
        for e in range(len(Time_word)):
            Time_Word.append(Time_word[e].split('\t'))
            Words.append(Time_word[e].split('\t')[2])

    Words = sorted(set(Words))
    sem_matrix = np.loadtxt(semantic_file)
    print 'sem matrix OK'
    fmri = np.loadtxt(fmri_file)
    fmri = fmri[:, 5:]
    print 'fMRI OK'

    num_voxels, num_time = fmri.shape
    time_segments = np.arange(0, num_time * 3, 3).astype(float)
    words_for_all_segment = []
    for time_segment_start in time_segments:
        time_segment_end = time_segment_start + 3
        words_for_segment = []
        for start, end, word in Time_Word:
            if time_segment_start <= float(end) / 1e3 <= time_segment_end:
                words_for_segment.append(word)
        words_for_all_segment.append(words_for_segment)
    print 'words for each segment OK'

    y_train = []
    X_train = []
    X_train_for_voxel = None
    for voxel_index, fmri_for_voxel in enumerate(fmri):
        y_train_for_voxel = []
        if X_train_for_voxel:
            x_already_computed = True
        else:
            X_train_for_voxel = []
            x_already_computed = False
        for fmri_activation, words_for_segment in izip(fmri_for_voxel, words_for_all_segment):
            columns_in_sem = []
            column = None
            for word in words_for_segment:
                # start = column if None is not column else 0
                # print word
                column = Words.index(word)
                columns_in_sem.append(column)

            for column in columns_in_sem:
                if not x_already_computed:
		    X_train_for_voxel.append(sem_matrix[:, column])
                y_train_for_voxel.append(fmri_activation)

        y_train.append(y_train_for_voxel)
        X_train.append(X_train_for_voxel)
        print 'fMRI sample {} read'.format(voxel_index)

    print 'train set OK'

    # for X_train_for_voxel, y_train_for_voxel in izip(X_train, y_train):
    #     # alphas = linear_regressor(X_train_for_voxel, y_train_for_voxel, None)
    #     alphas = linear_regressor_with_regularization(X_train_for_voxel, y_train_for_voxel, None)
    #     print alphas

    input_data = izip(X_train, y_train, range(len(y_train)))
    pool = mp.Pool(processes=8)

    num_features = 2000
    num_voxels = len(fmri)
    all_alphas = np.zeros((num_voxels, num_features))
    print all_alphas.shape
    for voxel_id, alphas in pool.imap_unordered(linear_regressor_with_regularization_wrapper, input_data):
        print 'Learned {} successfully'.format(voxel_id)
        # all_alphas.append((voxel_id, alphas))
        all_alphas[voxel_id, :] = alphas
    print 'machine learning OK'

    np.savetxt(model_file, all_alphas, fmt='%.6f')
    print 'save OK'

    pool.close()
    pool.join()
