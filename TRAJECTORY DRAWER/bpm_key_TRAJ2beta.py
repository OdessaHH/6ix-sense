import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Connect to the database
conn = sqlite3.connect("/home/user/Documents/6IX SENSE/ESSENTIA ANALYZER/databases/tracks_data_20230910_030358.db")
cursor = conn.cursor()

# Request data from the database
cursor.execute("SELECT BPM, Key, file_name FROM tracks_data")
data = cursor.fetchall()

# Prepare data for the plot
bpm_values = [item[0] for item in data if item[0] is not None]
key_values = [item[1] for item in data if item[1] is not None]
file_names = [item[2] for item in data if item[2] is not None]

# Convert keys (tonalities) to numerical values for displaying on the graph
key_numeric_values = []
for key in key_values:
    if key:
        key_numeric = ord(key[0]) - ord('A') + 1
        if len(key) > 1 and key[1] == '#':
            key_numeric += 0.5
        key_numeric_values.append(key_numeric)
    else:
        key_numeric_values.append(None)

# Create a new data structure with BPM and numeric key values
sorted_data_by_bpm = sorted(zip(bpm_values, key_numeric_values, file_names), key=lambda x: x[0])
sorted_data_by_key = sorted(zip(bpm_values, key_numeric_values, file_names), key=lambda x: x[1])

# Extract sorted BPM and key values for graph plotting
sorted_bpm_values_by_bpm, sorted_key_numeric_values_by_bpm, sorted_file_names_by_bpm = zip(*sorted_data_by_bpm)
sorted_bpm_values_by_key, sorted_key_numeric_values_by_key, sorted_file_names_by_key = zip(*sorted_data_by_key)

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(bpm_values, key_numeric_values, c='blue', alpha=0.5)
plt.plot(sorted_bpm_values_by_bpm, sorted_key_numeric_values_by_bpm, marker='o', linestyle='-', color='r', label='Line sorted by BPM')
plt.plot(sorted_bpm_values_by_key, sorted_key_numeric_values_by_key, marker='o', linestyle='-', color='g', label='Line sorted by Key')

# Adding labels to the points (Note: Adjust the dx and dy values to position the labels properly)
dx = 1
dy = 0.5
for i, (bpm, key, file_name) in enumerate(zip(bpm_values, key_numeric_values, file_names)):
    if bpm is not None and key is not None and file_name is not None:
        plt.text(bpm+dx, key+dy, file_name, fontsize=8)

# Set labels and title
plt.title('BPM vs Key')
plt.xlabel('BPM')
plt.ylabel('Key (numeric)')

# Set y-ticks for the key axis
plt.yticks(list(range(1, 13)), ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'])

# Save the plot
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
plt.savefig(f"/home/user/Documents/6IX SENSE/ESSENTIA ANALYZER/figures/bpm_vs_key_{current_time}.svg", format="svg")

# Show the plot
plt.grid(True)
plt.show()

# Close the database connection
conn.close()
