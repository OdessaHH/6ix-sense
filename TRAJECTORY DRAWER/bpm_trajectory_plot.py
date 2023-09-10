import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Подключаемся к базе данных
conn = sqlite3.connect("/home/user/Documents/6IX SENSE/ESSENTIA ANALYZER/databases/tracks_data_20230910_030358.db")
cursor = conn.cursor()

# Запрашиваем данные из базы
cursor.execute("SELECT id, BPM, Key FROM tracks_data")
data = cursor.fetchall()

# Подготавливаем данные для графика
bpm_values = [item[1] for item in data]
key_values = [item[2] for item in data]

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

# Собираем данные в список кортежей и сортируем по BPM
plot_data = sorted([(bpm, key) for bpm, key in zip(bpm_values, key_numeric_values) if bpm is not None and key is not None], key=lambda x: x[0])

# Создаем график
plt.figure(figsize=(10, 6))
plt.scatter(bpm_values, key_numeric_values, c='blue', alpha=0.5)

# Рисуем линию, соединяющую все точки от самой медленной до самой быстрой
if plot_data:
    plt.plot([x[0] for x in plot_data], [x[1] for x in plot_data], c='red')

plt.title('BPM vs Key')
plt.xlabel('BPM')
plt.ylabel('Key (numeric)')

# Устанавливаем метки для оси Y (тональности)
plt.yticks(list(range(1, 13)), ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'])

# Путь к папке, где будут сохраняться фигуры
output_directory = "/home/user/Documents/6IX SENSE/ESSENTIA ANALYZER/figures/"

# Получаем текущее время для создания уникального имени файла
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')

# Проверяем, существует ли папка, и создаем ее, если нет
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Сохраняем график
plt.savefig(os.path.join(output_directory, f"bpm_vs_key_{current_time}.svg"), format="svg")

# Показываем график
plt.grid(True)
plt.show()

"""# Сохраняем координаты в базу данных
for i, (bpm, key_numeric) in enumerate(plot_data):
    cursor.execute("UPDATE tracks_data SET graph_x = ?, graph_y = ? WHERE BPM = ? AND Key = ?", (i, key_numeric, bpm, key_values[key_numeric_values.index(key_numeric)]))
conn.commit()"""

# Закрываем соединение с базой данных
conn.close()
# Создаем новую структуру данных с BPM и числовыми значениями ключей
sorted_data = sorted(zip(bpm_values, key_numeric_values), key=lambda x: x[0])

# Печать порядка точек
for i, (bpm, key) in enumerate(sorted_data):
    print(f"{i+1}. BPM: {bpm}, Key: {key}")