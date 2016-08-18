# -*- coding: utf-8 -*-

import numpy as np
from pydub import AudioSegment
import sys
import glob
import re
import os
from pydub.utils import (
    db_to_float,
    ratio_to_db,
    register_pydub_effect,
    make_chunks,
    audioop,
    get_min_max_value
)
import pymorphy2


def normalize(seg, headroom=0.1):
    peak_sample_val = seg.max
    
    if peak_sample_val == 0:
        return seg
    
    target_peak = seg.max_possible_amplitude * db_to_float(-headroom)

    needed_boost = ratio_to_db(target_peak / peak_sample_val)
    return seg.apply_gain(needed_boost)



def detect_silence(audio_segment, min_silence_len=60, silence_thresh=20, koef=200):
    seg_len = len(audio_segment)
    if seg_len < min_silence_len:
        return []
    silence_thresh = db_to_float(silence_thresh) * audio_segment.max_possible_amplitude
    silence_thresh = silence_thresh//koef
    silence_starts = []

    slice_starts = seg_len - min_silence_len
    for i in range(slice_starts + 1):
        audio_slice = audio_segment[i:i+min_silence_len]
        if audio_slice.rms < silence_thresh:
            silence_starts.append(i)
    if not silence_starts:
        return []
 
    silent_ranges = []
    prev_i = silence_starts.pop(0)
    current_range_start = prev_i
 
    for silence_start_i in silence_starts:
        if silence_start_i - prev_i >= min_silence_len:
            silent_ranges.append([current_range_start,
                                  prev_i ])
            current_range_start = silence_start_i
        prev_i = silence_start_i
 
    silent_ranges.append([current_range_start,
                          prev_i + min_silence_len])
    silent_ranges1=[]
    for e in range(len(silent_ranges)):
        if silent_ranges[e][1]-silent_ranges[e][0]>=min_silence_len:
            silent_ranges1.append(silent_ranges[e])
        
    return silent_ranges1

def non_silent(silence,min_word_len=50):
    non_silent=[]
    for e in range(len(silence)-1):
        if silence[e+1][0]-silence[e][1]>= min_word_len:
            non_silent.append([silence[e][1],silence[e+1][0]])
    return non_silent


def expected_duration(word):
    MEAN_CONS_DURATION = 30
    MEAN_VOWEL_DURATION = 100
    VOWELS = u'аеуоиыэяюё'
    num_vowels = sum(word.count(vowel) for vowel in VOWELS)
    num_consonants = len(word) - num_vowels
    return MEAN_VOWEL_DURATION * num_vowels + MEAN_CONS_DURATION * num_consonants


def align_audio_text(segment, words):
    aligned_segments = []
    iter_segments = iter(segment)
    current_segment = next(iter_segments)

    no_more_segments = False
    expected_end = None
    for i, (word, normal_word) in enumerate(words):
        if no_more_segments:
            print '{} more words left'.format(len(words) - i)
            break
        current_word_duration = expected_duration(word)

        detected_start, detected_end = current_segment
        expected_start = max(detected_start, expected_end if None is not expected_end else detected_start)
        expected_end = expected_start + current_word_duration
        print word, current_word_duration, (detected_start, detected_end), (expected_start, expected_end)
        aligned_segments.append((expected_start, expected_end, normal_word))
        while expected_end > detected_end:
            try:
                current_segment = next(iter_segments)
            except StopIteration:
                no_more_segments = True
                break
            detected_start, detected_end = current_segment
    return aligned_segments

if __name__ == '__main__':
    input_file = sys.argv[1]
    input_text = sys.argv[2]
    output_alignment = sys.argv[3]

    # # files=glob.glob(os.path.join(input_file,'*'))
    # A = AudioSegment.from_mp3(input_file)
    # with open(input_text,'r') as text:
    #     Text = [i.strip() for i in text.readlines()]
    #     text_audio=[]
    #     for e in range(len(Text)):
    #         text_audio.extend(Text[e].split())
    # not_silent = non_silent(detect_silence(normalize(A)))
    # if len(text_audio) >= len(not_silent) >= len(text_audio)*0.9:
    #     print 'OK'
    #     # b = open('sek.txt', 'r')
    #     # B = [i.strip() for i in b.readlines()]
    #     # B[0] = B[0].replace('[[', '')
    #     # B[0] = B[0].replace(']]', '')
    #     # B = ''.join(B[0])
    #     # b.close()
    #     # C = []
    #     # B = B.split('],[')
    #     # for e in range(len(B)):
    #     #     B[e] = B[e].split(',')
    #     # q = len(A)
    #     # for e in range(q):
    #     #     A.extend(A[e].split())
    #     # del A[0:q]
    #     # c = open('got.txt', 'w')
    #     # print('start_i', 'end_i', 'word', sep=' ', file = c)
    #     # c.close()
    #     # c = open('got.txt', 'a')
    #     # for e in range(len(B)):
    #     #     print(B[e][0], B[e][1], A[e], sep=' ', file = c)
    #     #
    #     #     c.close()
    # else:
    #     print 'slishkom krivo'
    #     print len(text_audio)


    # load audio
    audiodata = AudioSegment.from_mp3(input_file) #'/home/sirius/bigdata/audio/hp_rus.mp3'
    # print(non_silent(detect_silence(normalize(A))))

    # load and preprocess text
    # '/home/sirius/bigdata/corpus-wiki/Harry_Potter.txt'
    with open(input_text) as story_file:
        story = story_file.read().strip().decode('utf-8')
    story = re.sub('[^\w\s]', '', story, flags=re.U)
    story_words = re.split('\s+', story)

    FORBIDDEN_TAGS = ['PRCL', 'PREP', 'CONJ', 'UNKN', 'LATN']
    analyzer = pymorphy2.MorphAnalyzer()
    story_words_noprep = []
    for word in story_words:
        parsed = analyzer.parse(word)[0]
        forbidden_tags_present = [tag in parsed.tag for tag in FORBIDDEN_TAGS]
        if not any(forbidden_tags_present):
            story_words_noprep.append((word, parsed.normal_form))

    # split audio on silence
    segment = np.array(non_silent(detect_silence(normalize(audiodata))))
    aligned_segments = align_audio_text(segment, story_words_noprep)
    with open(output_alignment, 'w') as align_file:
        for start, end, word in aligned_segments:
            align_file.write('{}\t{}\t{}\n'.format(start, end, word.encode('utf-8')))
