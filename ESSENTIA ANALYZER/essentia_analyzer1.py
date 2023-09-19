import os
import essentia.standard as es
from tqdm import tqdm
import time
import sqlite3
from datetime import datetime

# Получить текущее время и форматировать его как строку
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
db_folder = "/home/user/Documents/6IX SENSE/ESSENTIA ANALYZER/databases"
db_name = f'{db_folder}/tracks_data_{current_time}.db'

# Подключаемся к базе данных (или создаем новую, если ее нет)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()


# Создаем новую таблицу для хранения данных треков
cursor.execute('''
CREATE TABLE IF NOT EXISTS tracks_data (
    id INTEGER PRIMARY KEY,
    file_name TEXT,
    BPM REAL,
    Key TEXT
)
''')

# Определяем директорию с входными файлами
#input_dir = "/home/user/Documents/Privat/DJ HELP/wav converted"
input_dir = "/home/user/Documents/6IX SENSE/5tracks"

# Функция для расчета BPM с помощью Essentia
def calculate_bpm(wav_file):
    loader = es.MonoLoader(filename=wav_file)
    audio = loader()

    rhythm_extractor = es.RhythmExtractor2013()
    bpm, *_ = rhythm_extractor(audio) # Изменено на распаковку с игнорированием остальных значений

    return bpm


# Функция для извлечения метаданных аудио с использованием Essentia
def extract_metadata(audio_file):
    loader = es.MonoLoader(filename=audio_file)
    audio = loader()

    bpm = calculate_bpm(audio_file)
    
    key_extractor = es.KeyExtractor()
    key_info = key_extractor(audio)
    key = key_info[0]

    return {'BPM': bpm, 'Key': key, 'File': audio_file}

# Функция для перечисления всех WAV-файлов во входном каталоге и извлечения метаданных
def list_and_extract_audio():
    audio_files = []
    
    wav_files = []
    for dirpath, _, filenames in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith(".wav"):
                wav_files.append(os.path.join(dirpath, filename))

    with tqdm(total=len(wav_files), desc="Processing Files") as pbar:
        for wav_file in wav_files:
            metadata = extract_metadata(wav_file)
            audio_files.append(metadata)
            pbar.update(1)

    return audio_files

# Функция для сохранения данных в базу данных
def save_to_database(data):
    for item in data:
        file_name = os.path.basename(item['File'])
        cursor.execute("INSERT INTO tracks_data (file_name, BPM, Key) VALUES (?, ?, ?)", (file_name, item['BPM'], item['Key']))
    
    # Сохраняем изменения
    conn.commit()

if __name__ == "__main__":
    start_time = time.time()

    audio_files = list_and_extract_audio()

    if not audio_files:
        print("No WAV files found in the specified directory.")
    else:
        save_to_database(audio_files)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        num_tracks = len(audio_files)
        print(f"Processed and saved data of {num_tracks} tracks in {elapsed_time:.2f} seconds.")

    # Закрываем соединение с базой данных
    conn.close()
