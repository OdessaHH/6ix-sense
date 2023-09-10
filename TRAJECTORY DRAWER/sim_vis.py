
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
sorted_data_by_key = sorted(zip(bpm_values, key_numeric_values, file_names), key=lambda x: x[1])
sorted_data_by_bpm = sorted(zip(bpm_values, key_numeric_values, file_names), key=lambda x: x[0])

# Extract sorted BPM and key values for graph plotting
sorted_bpm_values_by_key, sorted_key_numeric_values_by_key, sorted_file_names_by_key = zip(*sorted_data_by_key)
sorted_bpm_values_by_bpm, sorted_key_numeric_values_by_bpm, sorted_file_names_by_bpm = zip(*sorted_data_by_bpm)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(bpm_values, key_numeric_values, c='blue', alpha=0.5)
line_by_key, = ax.plot([], [], marker='o', linestyle='-', color='r', label='Line sorted by Key')
line_by_bpm, = ax.plot([], [], marker='o', linestyle='-', color='g', label='Line sorted by BPM')

# Set labels and title
ax.set_title('BPM vs Key')
ax.set_xlabel('BPM')
ax.set_ylabel('Key (numeric)')

# Set y-ticks for the key axis
ax.set_yticks(list(range(1, 13)))
ax.set_yticklabels(['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'])

# Initialize the line data
x_data_by_key, y_data_by_key = [], []
x_data_by_bpm, y_data_by_bpm = [], []

def init():
    line_by_key.set_data([], [])
    line_by_bpm.set_data([], [])
    return line_by_key, line_by_bpm,

def update(frame):
    x_data_by_key.append(sorted_bpm_values_by_key[frame])
    y_data_by_key.append(sorted_key_numeric_values_by_key[frame])
    line_by_key.set_data(x_data_by_key, y_data_by_key)
    
    x_data_by_bpm.append(sorted_bpm_values_by_bpm[frame])
    y_data_by_bpm.append(sorted_key_numeric_values_by_bpm[frame])
    line_by_bpm.set_data(x_data_by_bpm, y_data_by_bpm)
    
    return line_by_key, line_by_bpm,

ani = FuncAnimation(fig, update, frames=range(len(sorted_bpm_values_by_key)), init_func=init, blit=True)

# Save the plot as an animated gif
ani.save(f"/home/user/Documents/6IX SENSE/ESSENTIA ANALYZER/figures/bpm_vs_key_animation_combined_{datetime.now().strftime('%Y%m%d_%H%M%S')}.gif", writer='imagemagick')

# Show the plot
plt.grid(True)
plt.legend()
plt.show()


# Close the database connection
conn.close()

# ... (rest of your script)

# Close the database connection
conn.close()



# ... (rest of your script)

def key_to_letter(key_numeric):
    keys = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    return keys[int(key_numeric) - 1] if key_numeric is not None else None

# Close the database connection
conn.close()

# Print the order of connection by BPM
print("Order of connection by BPM:")
for i, (file_name, key, bpm) in enumerate(sorted_data_by_bpm):
    try:
        bpm_value = round(float(bpm), 2)
    except ValueError:
        bpm_value = bpm
    print(f"{i+1}. BPM: {round(file_name,2)} , Key: {key_to_letter(key)} : {bpm_value} ")

# Print a blank line between the two lists
print()

# Print a blank line between the two lists
print()

# Print the order of connection by key
print("Order of connection by Key:")
for i, (file_name, key, bpm) in enumerate(sorted_data_by_key):
    try:
        bpm_value = round(float(bpm), 2)
    except ValueError:
        bpm_value = bpm
    print(f"{i+1}. Key: {key_to_letter(key)} , BPM: {round(file_name,2)}  : {bpm_value} ")

# Print a blank line between the two lists
print()

