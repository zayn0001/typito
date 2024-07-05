import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

def plot_audio_with_onsets(y, sr, onset_times):
    # Create a plot
    plt.figure(figsize=(10, 6))
    
    # Plot the waveform
    librosa.display.waveshow(y, sr=sr, alpha=0.6)
    plt.title('Waveform')
    
    # Mark the onsets with red points
    for onset in onset_times:
        plt.axvline(x=onset, color='r', linestyle='--')
    
    plt.tight_layout()
    st.pyplot(plt)

def main():
    st.title("Audio Onset Detection and Visualization")
    
    # Upload audio file
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    
    if uploaded_file is not None:
        # Load the audio file
        y, sr = librosa.load(uploaded_file, sr=None)
        
        # Detect onsets
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
        onset_times = librosa.frames_to_time(onset_frames, sr=sr)
        
        st.write("Detected Onsets (in seconds):")
        st.write(onset_times)
        
        # Plot audio with onset markers
        plot_audio_with_onsets(y, sr, onset_times)

if __name__ == "__main__":
    main()
