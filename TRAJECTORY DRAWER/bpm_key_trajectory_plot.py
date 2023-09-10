import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Connect to the database
conn = sqlite3.connect("/home/user/Documents/6IX SENSE/ESSENTIA ANALYZER/databases/tracks_data_20230910_030358.db")
cursor = conn.cursor()

# Request data from the database
cursor.execute("SELECT id, BPM, Key FROM tracks_data")
data = cursor.fetchall()

# Prepare data for the plot
bpm_values = [item[1] for item in data]
key_values = [item[2] for item in data]

# Convert keys to numerical values for displaying on the plot
key_numeric_values = []
for key in key_values:
    if key is not None:
        key_numeric = ord(key[0]) - ord('A') + 1
        if len(key) > 1 and key[1] == '#':
            key_numeric += 0.5
        key_numeric_values.append(key_numeric)
    else:
        key_numeric_values.append(None)

# Create two sorted data structures, one sorted by BPM and the other by key
sorted_data_by_bpm = sorted([(bpm, key) for bpm, key in zip(bpm_values, key_numeric_values) if bpm is not None and key is not None], key=lambda x: x[0])
sorted_data_by_key = sorted([(bpm, key) for bpm, key in zip(bpm_values, key_numeric_values) if bpm is not None and key is not None], key=lambda x: x[1])

# Extract sorted BPM and key values to plot
sorted_bpm_values_by_bpm, sorted_key_numeric_values_by_bpm = zip(*sorted_data_by_bpm)
sorted_bpm_values_by_key, sorted_key_numeric_values_by_key = zip(*sorted_data_by_key)

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(bpm_values, key_numeric_values, c='blue', alpha=0.5)
plt.plot(sorted_bpm_values_by_bpm, sorted_key_numeric_values_by_bpm, marker='o', linestyle='-', color='r', label='Line sorted by BPM')
plt.plot(sorted_bpm_values_by_key, sorted_key_numeric_values_by_key, marker='o', linestyle='-', color='g', label='Line sorted by Key')

# Set plot properties
plt.title('BPM vs Key')
plt.xlabel('BPM')
plt.ylabel('Key (numeric)')
plt.yticks(list(range(1, 13)), ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'])
plt.legend()
plt.grid(True)

# Save the plot
output_directory = "/home/user/Documents/6IX SENSE/ESSENTIA ANALYZER/figures/"
current_time = datetime.now().strftime('%Y%m%d_%H-%M-%S')
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
plt.savefig(os.path.join(output_directory, f"bpm_vs_key_{current_time}.svg"), format="svg")

# Show the plot
plt.show()

# Print the order of the points
print("Sorted by BPM:")
for i, (bpm, key) in enumerate(sorted_data_by_bpm):
    print(f"{i+1}. BPM: {bpm}, Key: {key}")

print("\nSorted by Key:")
for i, (bpm, key) in enumerate(sorted_data_by_key):
    print(f"{i+1}. BPM: {bpm}, Key: {key}")

# Close the connection to the database
conn.close()
