import pygame
import time

def play_audio_with_timestamps(audio_file, timestamps):
    # Initialize pygame mixer
    pygame.mixer.init()

    # Start playing the audio
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    timel = [timestamps[k+1] - timestamps[k] for k in range(len(timestamps)-1)]
    timel = [int(float(ts) * 1000) for ts in timel]

    for ts in timel:
        time.sleep(ts / 1000.0)  # Convert milliseconds back to seconds
        print(f"Timestamp: {ts / 1000.0} seconds")

    # Wait until the audio finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Adjust tick rate as needed

    # Clean up pygame mixer
    pygame.mixer.quit()

# Example usage
audio_file = 'dont-blink-short.mp3'  
timestamps = [0.1277,0.2554,0.3947,0.4992,0.9636,1.4512,1.8112,2.055,2.1711,2.4149,2.8909,3.3669,3.7268,4.0867,4.2028,4.4466,4.6904,4.911,5.1664,5.3986,5.6424,5.7585,6.0024,6.1301,6.3623,6.8499]  # Replace with your list of timestamps

play_audio_with_timestamps(audio_file, timestamps)
