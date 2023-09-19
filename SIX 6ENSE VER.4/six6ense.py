# This version of six6ense.py is for extracting data from a directory of wav files
# BPM, tempo, chroma, spectral centroid, spectral contrast

import os
import librosa
import pandas as pd
from datetime import datetime
import essentia.standard as es

def extract_features(file_path):
    try:
        # Loading the file
        y, sr = librosa.load(file_path, sr=None)

        # Extracting features using librosa
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

        # Extracting features using essentia
        loader = es.MonoLoader(filename=file_path)
        audio = loader()
        rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
        bpm, _, _, _, _,= rhythm_extractor(audio)

        # Getting the file name
        file_name = os.path.basename(file_path)
        
        print(f"Processed file: {file_name}")
        print(f"Tempo: {tempo}, BPM: {bpm}, Chroma STFT Mean: {chroma_stft.mean()}, Spectral Centroid Mean: {spectral_centroid.mean()}, Spectral Contrast Mean: {spectral_contrast.mean()}")

        return {"File_Name": file_name, "Tempo": tempo, "BPM_Essentia": bpm, "Chroma_STFT_Mean": chroma_stft.mean(), "Spectral_Centroid_Mean": spectral_centroid.mean(), "Spectral_Contrast_Mean": spectral_contrast.mean()}
    
    except Exception as e:
        print(f"Could not process file {file_path}: {e}")
        return None

def process_directory(directory_path):
    features_list = []
    for file in os.listdir(directory_path):
        if file.endswith(".wav"):
            file_path = os.path.join(directory_path, file)
            features = extract_features(file_path)
            if features:
                features_list.append(features)
    
    return features_list

if __name__ == "__main__":
    directory_path = '/home/user/Documents/6IX SENSE/TEST MUSIC/5tracks'  # Specify the correct path to your directory with files here
    features_list = process_directory(directory_path)

    if features_list:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        df = pd.DataFrame(features_list)
        df.to_csv(f'data_{timestamp}.csv', index=False)
        print("Feature extraction completed and data saved!")
    else:
        print("No data to save.")
