import sqlite3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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

# Extract sorted BPM and key values for graph plotting
sorted_bpm_values_by_bpm, sorted_key_numeric_values_by_bpm, sorted_file_names_by_bpm = zip(*sorted_data_by_bpm)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(bpm_values, key_numeric_values, c='blue', alpha=0.5)
line, = ax.plot([], [], marker='o', linestyle='-', color='r', label='Line sorted by BPM')

# Set labels and title
ax.set_title('BPM vs Key')
ax.set_xlabel('BPM')
ax.set_ylabel('Key (numeric)')

# Set y-ticks for the key axis
ax.set_yticks(list(range(1, 13)))
ax.set_yticklabels(['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'])

# Initialize the line data
x_data, y_data = [], []

def init():
    line.set_data([], [])
    return line,

def update(frame):
    x_data.append(sorted_bpm_values_by_bpm[frame])
    y_data.append(sorted_key_numeric_values_by_bpm[frame])
    line.set_data(x_data, y_data)
    return line,

ani = FuncAnimation(fig, update, frames=range(len(sorted_bpm_values_by_bpm)), init_func=init, blit=True)

# Save the plot as an animated gif
ani.save(f"/home/user/Documents/6IX SENSE/ESSENTIA ANALYZER/figures/bpm_vs_key_animation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.gif", writer='imagemagick')

# Show the plot
plt.grid(True)
plt.show()

# Close the database connection
conn.close()
