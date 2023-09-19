
#This script processes a directory of .wav audio files to extract musical features such as tempo and chroma STFT mean.
#It then saves the extracted data into CSV files and a sorted playlist with detailed track information into a text file.

import os
import librosa
import pandas as pd
from datetime import datetime
import essentia.standard as es

def extract_features(file_path):
    # Loading the file
    y, sr = librosa.load(file_path, sr=None)

    # Extracting features using librosa
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)

    # Extracting features using essentia
    loader = es.MonoLoader(filename=file_path)
    audio = loader()
    rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
    tempo_essentia, _, _, _, _ = rhythm_extractor(audio)
    
    return {
        "Filename": os.path.basename(file_path),
        "Tempo": tempo,
        "Tempo_Essentia": tempo_essentia,
        "Chroma_STFT_Mean": chroma_stft.mean(),
        "Spectral_Centroid_Mean": spectral_centroid.mean()
    }

def process_directory(directory_path):
    features_list = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".wav"):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")
                features = extract_features(file_path)
                features_list.append(features)
                print(f"Features extracted for {file_path}")
    return features_list

# Set the path to your directory with files here
directory_path = "/home/user/Documents/6IX SENSE/TEST MUSIC/5tracks"

# Extracting features from all files in the directory
features_list = process_directory(directory_path)

# Saving features to a CSV file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'features_{timestamp}.csv'
df = pd.DataFrame(features_list)
df.to_csv(output_file, index=False)

print(f"Features saved to {output_file}")

# Sorting tracks by tempo (in ascending order) and saving to a new CSV file
sorted_df = df.sort_values(by='Tempo_Essentia')
sorted_output_file = f'sorted_features_{timestamp}.csv'
sorted_df.to_csv(sorted_output_file, index=False)

print(f"Sorted features saved to {sorted_output_file}")

# Saving the sorted tracklist to a text file
playlist_file = f'sorted_playlist_{timestamp}.txt'
with open(playlist_file, 'w') as f:
    for _, row in sorted_df.iterrows():
        track_info = f"Filename: {row['Filename']}, Tempo: {row['Tempo']}, Tempo_Essentia: {row['Tempo_Essentia']}, Chroma_STFT_Mean: {row['Chroma_STFT_Mean']}, Spectral_Centroid_Mean: {row['Spectral_Centroid_Mean']}\n"
        f.write(track_info)

print(f"Sorted playlist saved to {playlist_file}")
