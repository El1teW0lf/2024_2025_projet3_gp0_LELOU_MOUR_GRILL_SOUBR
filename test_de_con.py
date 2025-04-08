import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Generate random data
N = 47
data = [random.randint(1, 100) for _ in range(N)]

# Bubble sort generator — yields data after every swap
def bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(n - 1 - i):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                yield data.copy()  # Yield a snapshot after each swap

# Set up plot
fig, ax = plt.subplots()
bar_rects = ax.bar(range(len(data)), data, align="edge", color="skyblue")
ax.set_title("Bubble Sort Visualization")
ax.set_xlim(0, N)
ax.set_ylim(0, max(data) + 10)
text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

# Update function for animation
def update(data):
    for rect, val in zip(bar_rects, data):
        rect.set_height(val)
    text.set_text("Sorting...")

# Create the animation
anim = animation.FuncAnimation(fig, update, frames=bubble_sort(data),
                               repeat=False, blit=False, interval=100)

plt.show()
