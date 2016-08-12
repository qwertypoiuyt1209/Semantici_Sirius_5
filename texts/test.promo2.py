from pydub import AudioSegment
from pydub.silence import split_on_silence
import sys
import math
import array
from pydub.utils import (
    db_to_float,
    ratio_to_db,
    register_pydub_effect,
    make_chunks,
    audioop,
    get_min_max_value
)

A=AudioSegment.from_wav('record5.wav')
def normalize(seg, headroom=0.1):
    peak_sample_val = seg.max
    
    if peak_sample_val == 0:
        return seg
    
    target_peak = seg.max_possible_amplitude * db_to_float(-headroom)

    needed_boost = ratio_to_db(target_peak / peak_sample_val)
    return seg.apply_gain(needed_boost)



def detect_silence(audio_segment, min_silence_len=100, silence_thresh=25,koef=1000):
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

def non_silent(silence,min_word_len=100):
    non_silent=[]
    for e in range(len(silence)-1):
        if silence[e+1][0]-silence[e][1]>= min_word_len:
            non_silent.append([silence[e][1],silence[e+1][0]])
    return non_silent
    
print(non_silent(detect_silence(normalize(A))))
