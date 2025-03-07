import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

# Load the audio file
filename = "GuitarStandard.mp3"  # Replace with your file
y, sr = librosa.load(filename, sr=None)

# Time axis for waveform
time = np.linspace(0, len(y) / sr, len(y))

# Compute Short-Time Fourier Transform (STFT) to get frequency over time
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

# Plot Time-Domain Waveform (Amplitude vs Time)
ax1.plot(time, y, color='b')
ax1.set_xlabel("Time (seconds)")
ax1.set_ylabel("Amplitude")
ax1.set_title("Time-Domain Waveform (Amplitude vs Time)")
ax1.grid()

# Plot Spectrogram (Frequency vs Time)
img = librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="log", ax=ax2)
ax2.set_title("Spectrogram (Frequency over Time)")
fig.colorbar(img, ax=ax2, format="%+2.0f dB")

# Show plots
plt.tight_layout()
plt.show()
