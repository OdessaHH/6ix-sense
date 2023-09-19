import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Подключаемся к базе данных
conn = sqlite3.connect("/home/user/Documents/6IX SENSE/ESSENTIA ANALYZER/databases/tracks_data_20230912_013225.db")
cursor = conn.cursor()

# Запрашиваем данные из базы
cursor.execute("SELECT BPM, Key FROM tracks_data")
data = cursor.fetchall()

# Подготавливаем данные для графика
bpm_values = [item[0] for item in data]
key_values = [item[1] for item in data]

# Преобразуем ключи (тональности) в числовые значения для отображения на графике
key_numeric_values = []
for key in key_values:
    if key is not None:
        key_numeric = ord(key[0]) - ord('A') + 1
        if len(key) > 1 and key[1] == '#':
            key_numeric += 0.5
        key_numeric_values.append(key_numeric)
    else:
        key_numeric_values.append(None)

# Создаем график
plt.figure(figsize=(10, 6))
plt.scatter(bpm_values, key_numeric_values, c='blue', alpha=0.5)
plt.title('BPM vs Key')
plt.xlabel('BPM')
plt.ylabel('Key (numeric)')

# Устанавливаем метки для оси Y (тональности)
plt.yticks(list(range(1, 13)), ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'])

# Показываем график
plt.grid(True)
plt.show()

# Получаем текущее время и форматируем его как строку для использования в имени файла
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
file_name = f"MATPLOTLIB VISUALISATION/graphs/graph-{current_time}.svg"

# Сохраняем график в формате SVG с временной меткой в имени файла
plt.savefig(file_name, format='svg')

# Закрываем соединение с базой данных
conn.close()
