import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Подключаемся к базе данных
conn = sqlite3.connect("/home/user/Documents/6IX SENSE/ESSENTIA ANALYZER/databases/tracks_data_20230910_030358.db")
cursor = conn.cursor()

# Запрашиваем данные из базы
cursor.execute("SELECT BPM, Key FROM tracks_data")
data = cursor.fetchall()

# Подготавливаем данные для графика
bpm_values = [item[0] for item in data if item[0] is not None]
key_values = [item[1] for item in data if item[1] is not None]

# Преобразуем ключи (тональности) в числовые значения для отображения на графике
key_numeric_values = []
for key in key_values:
    key_numeric = ord(key[0]) - ord('A') + 1
    if len(key) > 1 and key[1] == '#':
        key_numeric += 0.5
    key_numeric_values.append(key_numeric)

# Создаем новую структуру данных с BPM и числовыми значениями ключей
sorted_data = sorted(zip(bpm_values, key_numeric_values), key=lambda x: x[1])

# Извлекаем отсортированные значения BPM и ключей для построения графика
sorted_bpm_values, sorted_key_numeric_values = zip(*sorted_data)

# Создаем график
plt.figure(figsize=(10, 6))
plt.scatter(bpm_values, key_numeric_values, c='blue', alpha=0.5)
plt.plot(sorted_bpm_values, sorted_key_numeric_values, marker='o', linestyle='-', color='r')
plt.title('BPM vs Key')
plt.xlabel('BPM')
plt.ylabel('Key (numeric)')

# Устанавливаем метки для оси Y (тональности)
plt.yticks(list(range(1, 13)), ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'])

# Соединяем точки линиями
plt.plot(sorted_bpm_values, sorted_key_numeric_values, linestyle='-', color='black')

# Сохраняем график
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
plt.savefig(f"/home/user/Documents/6IX SENSE/ESSENTIA ANALYZER/figures/bpm_vs_key_{current_time}.svg", format="svg")

# Показываем график
plt.grid(True)
plt.show()

# Закрываем соединение с базой данных
conn.close()

# Печать порядка точек
for i, (bpm, key) in enumerate(sorted_data):
    print(f"{i+1}. BPM: {bpm}, Key: {key}")
