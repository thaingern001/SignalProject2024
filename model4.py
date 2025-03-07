import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from itertools import permutations

def mymodel_stft(y, sr, filter_percent=20, window_size=2048, hop_size=512):
    # Perform STFT (Short-Time Fourier Transform)
    D = librosa.stft(y, n_fft=window_size, hop_length=hop_size)
    magnitude, _ = librosa.magphase(D)  # Get magnitude of STFT

    # Convert magnitude to decibels (log scale)
    magnitude_db = librosa.amplitude_to_db(magnitude, ref=np.max)
    
    # Find the peak frequencies in the magnitude spectrum
    freqs = librosa.fft_frequencies(sr=sr, n_fft=window_size)
    
    # Flatten the magnitude and frequencies
    mag_flatten = magnitude_db.flatten()
    freqs_flatten = np.tile(freqs, magnitude.shape[1])

    # Filter the magnitudes based on threshold (filter_percent)
    threshold = np.percentile(mag_flatten, 100 - filter_percent)
    freqs_filtered = freqs_flatten[mag_flatten >= threshold]

    # Return the unique frequencies after thresholding
    freqs_filtered = sorted(set(freqs_filtered))
    
    return freqs_filtered

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
    nums = [note_to_num[n] for n in notes]
    
    for perm in permutations(nums):  
        root = perm[0]
        intervals = [(n - root) % 12 for n in perm]
        
        for chord_name, pattern in chords.items():
            if intervals == pattern:
                return f"{num_to_note[root]}{chord_name}"  
    
    return "Unknown Chord"

def sound_to_chord_stft(y, sr, percent=20, window_size=2048, hop_size=512):
    freqs = mymodel_stft(y, sr, percent, window_size, hop_size)
    print("Detected Frequencies:", freqs)  # Debugging print
    if len(freqs) == 0:
        return "No chord detected"
    
    notes = [freq_to_note(f) for f in freqs]
    print("Mapped Notes:", notes)  # Debugging print
    return note_to_chord(notes)

def note_to_chord(notes):
    # Remove 'X' from the notes list if present
    notes = [note for note in notes if note != 'X']
    ans = identify_chord(notes)
    return ans

def identify_chord(notes):
    nums = [note_to_num[n] for n in notes]
    
    for perm in permutations(nums):  
        root = perm[0]
        intervals = [(n - root) % 12 for n in perm]
        
        for chord_name, pattern in chords.items():
            if intervals == pattern:
                return f"{num_to_note[root]}{chord_name}"  # Return chord name
    
    return "Unknown Chord"

# Testing with an example file
filename = "Comp/Am.mp3"
y, sr = librosa.load(filename, sr=None)

print("Audio Loaded Successfully")  # Debugging print

chord = sound_to_chord_stft(y, sr)
print(f"Detected Chord: {chord}")  # Output the detected chord
