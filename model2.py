from itertools import permutations
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

def mymodel(filename,filter_persent = 20):

    y, sr = librosa.load(filename, sr=None)

    N = len(y)  # Number of samples
    frequencies = np.fft.rfftfreq(N, d=1/sr)  # Frequency bins
    fft_values = np.fft.rfft(y)  # Compute FFT
    magnitude = np.abs(fft_values)  # Magnitude spectrum

    max_mag = max(magnitude)

    new_mag = magnitude/max_mag*100
    fileter_mag = new_mag.copy()
    fileter_mag[fileter_mag < filter_persent] = 0

    ans = []
    for i in range(len(fileter_mag)):
        if fileter_mag[i] >= filter_persent:
            # print(frequencies[i])
            ans.append(int(frequencies[i]))
    ans = list(set(ans))
    ans.sort()
    return ans

def freq_to_note(freq):
    while (freq > 165):
        freq /= 2
    if freq < 80:return "X"
    if (freq < 84.5):return "E"
    elif freq < 90 :return "F"
    elif freq < 95.5 :return "F#"
    elif freq < 101 :return "G"
    elif freq < 107 :return "G#"
    elif freq < 113.5 :return "A"
    elif freq < 120.5 :return "A#"
    elif freq < 127.5 :return "B"
    elif freq < 135 :return "C"
    elif freq < 143 :return "C#"
    elif freq < 151.5 :return "D"
    elif freq < 160.5 :return "D#"
    else :return "E"

def tell_note(filename,percent = 20): 
    freqs = mymodel(filename,percent)
    ans = {'X'}
    for i in freqs:
        if i>600:continue
        ans.add(freq_to_note(i))
        if len(ans)>=4:break
    # print(ans)
    ans.remove('X')
    return ans

note_to_num = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 
               'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
num_to_note = {v: k for k, v in note_to_num.items()}
chords = {
    "": [0, 4, 7], #Major
    "m": [0, 3, 7]
}

def identify_chord(notes):
    # แปลงโน้ตเป็นตัวเลข
    nums = [note_to_num[n] for n in notes]
    
    for perm in permutations(nums):  # ลองทุกลำดับของโน้ต
        root = perm[0]
        intervals = [(n - root) % 12 for n in perm]
        
        for chord_name, pattern in chords.items():
            if intervals == pattern:
                return f"{num_to_note[root]}{chord_name}"  # แสดงชื่อคอร์ดที่แท้จริง
    
    return "Unknown Chord"

def note_to_chord(notes):
    note = list(notes)
    # note.remove('X')
    ans = identify_chord(note)
    # print(type(note))
    return ans

def sound_to_chord(filename,percent=20):
    note = tell_note(filename,percent)
    ans = note_to_chord(note)
    return ans


