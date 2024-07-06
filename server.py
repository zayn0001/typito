import base64
import tempfile
import time
import pygame
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from pydub import AudioSegment
from pydub.playback import play
import streamlit.components.v1 as components


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

def play_audio_with_timestamps(audio_file, timestamps, text):
    # Initialize pygame mixer
    pygame.mixer.init()

        # get continouous values 
    timel = [timestamps[k+1] - timestamps[k] for k in range(len(timestamps)-1)]

    placeholder = st.empty()
    timestamp_outputs = []
    text = text.split(" ")
    count = 0

    # Start playing the audio
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    #audio = AudioSegment.from_file(audio_file)
    #play(audio)
    #audio_bytes = audio_file.read()
    #audio_base64 = base64.b64encode(audio_bytes).decode()

    # Generate HTML for the audio player with autoplay
    #audio_html = f"""
    #<audio autoplay>
    #    <source src="data:audio/ogg;base64,{audio_base64}" type="audio/ogg">
    #    <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
    #    Your browser does not support the audio element.
    #</audio>
    #"""

    # Embed the HTML in the Streamlit app
    #components.html(audio_html, height=0)


    for ts in timel:
        time.sleep(ts)  # Convert milliseconds back to seconds
        if count >= len(text):
            count = 0
        # Update the container with new content
        placeholder.markdown(f"<div style='font-size:48px;'>{text[count]}</div>", unsafe_allow_html=True)
        count+=1

    # Wait until the audio finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Adjust tick rate as needed

    # Clean up pygame mixer
    pygame.mixer.quit()

def main():
    st.title("Audio Onset Detection and Visualization")
    
    # Upload audio file
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    text = st.text_input("Text to use for animation")

    button = st.button("submit")
    
    if button:
        # Load the audio file
        y, sr = librosa.load(uploaded_file, sr=None)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name
        
        # Detect onsets
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
        onset_times = librosa.frames_to_time(onset_frames, sr=sr)
        
        #st.write("Detected Onsets (in seconds):")
        #st.write(onset_times)

        play_audio_with_timestamps(temp_file_path, onset_times, text)
        
        # Plot audio with onset markers
        # plot_audio_with_onsets(y, sr, onset_times)

if __name__ == "__main__":
    main()
