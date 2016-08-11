from pydub import AudioSegment
from pydub.utils import (
    db_to_float
)

def detect_silence(audio_segment, min_silence_len=50, silence_thresh=25,koef=3000):
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
        if silence_start_i != prev_i + 1:
            silent_ranges.append([current_range_start,
                                  prev_i ])
            current_range_start = silence_start_i
        prev_i = silence_start_i
 
    silent_ranges.append([current_range_start,
                          prev_i + min_silence_len])
    a=len(silent_ranges)
    for e in range(a):
        try:
            if silent_ranges[e][1]-silent_ranges[e][0]<min_silence_len:
                silent_ranges.pop(e)
        except:
            break
        
    return silent_ranges
non_silent=[]
A = AudioSegment.from_mp3( 'recordtest1.mp3')
silence=(detect_silence(A))
for e in range(len(silence)-1):
    if silence[e+1][0]-silence[e][1]>100:
        non_silent.append([silence[e][1],silence[e+1][0]])
    
print(non_silent,silence,sep='\n')
##NS=open('sek.txt','w')
##print(non_silent,file=NS)
##NS.close()
