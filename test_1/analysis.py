import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

SIMULATION_TIME_STEP = 0.05  # seconds
filename = './test_1/data.csv'

# Read data from CSV file

def read_data(filename):
    with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
            return data

def plot_state(data):
    
    # Extract velocity in Y direction
    velocity_y = [float(row['velocity_y']) for row in data]
    figure = plt.figure(figsize=(8, 6))
    plt.plot([x * SIMULATION_TIME_STEP for x in range(len(velocity_y))], velocity_y, marker='o')
    plt.xlabel('Time Step')
    plt.ylabel('Velocity (m/s)')
    plt.title('Velocity in Y direction')
    plt.grid()
    plt.show()

    # Extract acceleration in Y direction
    acceleration_y = [float(row['acceleration_y']) for row in data]
    figure = plt.figure(figsize=(8, 6))
    plt.plot([x * SIMULATION_TIME_STEP for x in range(len(acceleration_y))], acceleration_y, marker='o')
    plt.xlabel('Time Step')
    plt.ylabel('Acceleration (m/s^2)')
    plt.title('Acceleration in Y direction')
    plt.grid()
    plt.show()

    # Extract jerk in Y direction
    jerk_y = [float(row['jerk_y']) for row in data]
    figure = plt.figure(figsize=(8, 6))
    plt.plot([x * SIMULATION_TIME_STEP for x in range(len(jerk_y))], jerk_y, marker='o')
    plt.xlabel('Time Step')
    plt.ylabel('Jerk (m/s^3)')
    plt.title('Jerk in Y direction')
    plt.grid()
    plt.show()

    # Extract relative_distance:
    relative_distance = [float(row['relative_distance']) for row in data]
    figure = plt.figure(figsize=(8, 6))
    plt.plot([x * SIMULATION_TIME_STEP for x in range(len(relative_distance))], relative_distance, marker='o')
    plt.xlabel('Time Step')
    plt.ylabel('Relative Distance (m)')
    plt.title('Relative Distance')
    plt.grid()
    plt.show()

def animate_verdicts(data):
    # Extract verdicts
    bbox_top_left_x = [row['bbox_top_left_x'] for row in data]
    bbox_top_left_y = [row['bbox_top_left_y'] for row in data]

    bbox_top_right_x = [row['bbox_top_right_x'] for row in data]
    bbox_top_right_y = [row['bbox_top_right_y'] for row in data]

    bbox_bottom_left_x = [row['bbox_bottom_left_x'] for row in data]
    bbox_bottom_left_y = [row['bbox_bottom_left_y'] for row in data]

    bbox_bottom_right_x = [row['bbox_bottom_right_x'] for row in data]
    bbox_bottom_right_y = [row['bbox_bottom_right_y'] for row in data]

    fig, ax = plt.subplots(figsize=(8, 6))

    def update(frame):
        
        i = frame
        ax.clear()
        ax.scatter(bbox_top_left_x[i], bbox_top_left_y[i], c='r')
        ax.scatter(bbox_top_right_x[i], bbox_top_right_y[i], c='r')
        ax.scatter(bbox_bottom_left_x[i], bbox_bottom_left_y[i], c='r')
        ax.scatter(bbox_bottom_right_x[i], bbox_bottom_right_y[i], c='r')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'iteration {i}')
        ax.grid()

    ani = FuncAnimation(fig, update, frames=len(bbox_top_left_x), repeat=False)
    ani.save('verdicts.gif', writer='Pillow', fps=30)
    plt.show()

def main():
    data = read_data(filename)
    plot_state(data)
    # animate_verdicts(data)

if __name__ == '__main__':
    main()
