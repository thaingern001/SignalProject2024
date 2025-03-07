#work not tune
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from itertools import permutations

def mymodel(y, sr, filter_percent=20):
    N = len(y)  # Number of samples
    frequencies = np.fft.rfftfreq(N, d=1/sr)  # Frequency bins
    fft_values = np.fft.rfft(y)  # Compute FFT
    magnitude = np.abs(fft_values)  # Magnitude spectrum

    max_mag = max(magnitude)
    new_mag = magnitude / max_mag * 100
    filtered_mag = new_mag.copy()
    filtered_mag[filtered_mag < filter_percent] = 0

    ans = []
    for i in range(len(filtered_mag)):
        if filtered_mag[i] >= filter_percent:
            ans.append(int(frequencies[i]))

    ans = sorted(set(ans))  # Remove duplicates and sort
    return ans

def freq_to_note(freq):
    while freq > 165:
        freq /= 2
    if freq < 80: return "X"
    if freq < 84.5: return "E"
    elif freq < 90: return "F"
    elif freq < 95.5: return "F#"
    elif freq < 101: return "G"
    elif freq < 107: return "G#"
    elif freq < 113.5: return "A"
    elif freq < 120.5: return "A#"
    elif freq < 127.5: return "B"
    elif freq < 135: return "C"
    elif freq < 143: return "C#"
    elif freq < 151.5: return "D"
    elif freq < 160.5: return "D#"
    else: return "E"

def tell_note(y, sr, percent=20):
    freqs = mymodel(y, sr, percent)
    ans = {'X'}
    for i in freqs:
        if i > 600: continue
        ans.add(freq_to_note(i))
        if len(ans) >= 4: break
    ans.discard('X')  # Remove placeholder
    return ans

note_to_num = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 
               'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
num_to_note = {v: k for k, v in note_to_num.items()}
chords = {
    "": [0, 4, 7],  # Major
    "m": [0, 3, 7]   # Minor
}

def identify_chord(notes):
    if not notes:
        return "No Notes Detected"
    
    print(f"Notes received: {notes}")  # Debugging print

    nums = [note_to_num[n] for n in notes if n in note_to_num]  # ตรวจสอบว่าโน้ตถูกต้อง
    
    if not nums:  # ถ้าไม่มีโน้ตที่ตรงกับ `note_to_num`
        return "No Valid Notes"

    print(f"Converted to numbers: {nums}")  # Debugging print

    for perm in permutations(nums):
        root = perm[0]  # <- Error เกิดที่นี่หาก perm เป็นค่าว่าง
        intervals = [(n - root) % 12 for n in perm]

        for chord_name, pattern in chords.items():
            if intervals == pattern:
                return f"{num_to_note[root]}{chord_name}"

    return "Unknown Chord"


def tell_note(y, sr, percent=20):
    freqs = mymodel(y, sr, percent)
    # print(f"Detected frequencies: {freqs}")  # Debugging print

    ans = {'X'}
    for i in freqs:
        if i > 600: 
            continue
        ans.add(freq_to_note(i))
        if len(ans) >= 4:
            break
    
    ans.discard('X')  # Remove placeholder

    print(f"Identified Notes: {ans}")  # Debugging print

    return ans

note_to_num = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 
               'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
num_to_note = {v: k for k, v in note_to_num.items()}
chords = {
    "": [0, 4, 7],  # Major
    "m": [0, 3, 7]   # Minor
}

def identify_chord(notes):
    if not notes:
        return "No chord detected"
    nums = [note_to_num[n] for n in notes if n in note_to_num]
    if not nums:
        return "No valid note detected"
    for perm in permutations(nums):
        if not perm:  # หรือไม่จำเป็นในกรณีนี้
            continue
        root = perm[0]
        intervals = [(n - root) % 12 for n in perm]
        for chord_name, pattern in chords.items():
            if intervals == pattern:
                return f"{num_to_note[root]}{chord_name}"
    return "Unknown Chord"

def note_to_chord(notes):
    return identify_chord(list(notes))

def sound_to_chord(y, sr, percent=20):
    notes = tell_note(y, sr, percent)
    return note_to_chord(notes)

### NEW FUNCTION: MULTIPLE CHORD DETECTION ###
def sound_to_chords(filename, percent=20, window_size=1.0, hop_size=0.5):
    """
    Process an audio file in segments and detect chords over time.
    
    filename: path to the audio file
    percent: threshold for frequency detection
    window_size: length of each segment in seconds
    hop_size: step size between windows (overlapping allowed)
    
    Returns:
        List of (timestamp, chord) pairs
    """
    y, sr = librosa.load(filename, sr=None)
    segment_length = int(sr * window_size)
    hop_length = int(sr * hop_size)
    num_segments = (len(y) - segment_length) // hop_length + 1

    chords_over_time = []

    for i in range(num_segments):
        start = i * hop_length
        end = start + segment_length
        segment = y[start:end]

        if len(segment) < segment_length:
            break  # Skip last incomplete segment

        chord = sound_to_chord(segment, sr, percent)
        timestamp = round(start / sr, 2)
        chords_over_time.append((timestamp, chord))

    return chords_over_time


filename = "test/dowload01.mp3"
chord_progression = sound_to_chords(filename,20)

for time, chord in chord_progression:
    print(f"Time: {time}s -> Chord: {chord}")

# y, sr = librosa.load("phone/chordD.mp3", sr=None)
# notes = tell_note(y, sr, percent=10)
# print(f"Notes Detected: {notes}")

# if notes:
#     chord = note_to_chord(notes)
#     print(f"Detected Chord: {chord}")
# else:
#     print("No Notes Detected")
