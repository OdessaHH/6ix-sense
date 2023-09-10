import matplotlib.pyplot as plt

# Data for the first line
x1 = [1, 2, 3, 4, 5]
y1 = [2, 4, 1, 3, 5]

# Data for the second line
x2 = [1, 2, 3, 4, 5]
y2 = [5, 3, 2, 4, 1]

# Plot the first line in blue with solid line style
plt.plot(x1, y1, color='blue', linestyle='-', label='Line 1')

# Plot the second line in red with dashed line style
plt.plot(x2, y2, color='red', linestyle='--', label='Line 2')

# Add labels, legend, and show the plot
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.show()
