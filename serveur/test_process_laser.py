import matplotlib.pyplot as plt
import numpy as np
import csv

import os
import json

dirname = os.path.dirname(__file__)

plt.style.use('_mpl-gallery-nogrid')

X = []
Y = []

filename_front = os.path.join(dirname, "../data/laser/laser_data_front.csv")
filename_left = os.path.join(dirname, "../data/laser/laser_data_left.csv")
filename_right = os.path.join(dirname, "../data/laser/laser_data_right.csv")

with open(filename_front) as front_file, open(filename_left) as left_file, open(filename_right) as right_file:
    front_reader = csv.DictReader(front_file)
    left_reader = csv.DictReader(left_file)
    right_reader = csv.DictReader(right_file)

    for row in front_reader:
        for i in range (1, 16):
            t = json.loads(row['Seg0' + str(i)])
            X.append(t[0])
            Y.append(t[1])
    for row in left_reader:
        for i in range (1, 16):
            t = json.loads(row['Seg0' + str(i)])
            X.append(t[0])
            Y.append(t[1])
    for row in right_reader:
        for i in range (1, 16):
            t = json.loads(row['Seg0' + str(i)])
            X.append(t[0])
            Y.append(t[1])

X = np.array(X)
Y = np.array(Y)

# size and color:
sizes = np.random.uniform(15, 80, len(X))
colors = np.random.uniform(15, 80, len(X))

# plot
fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(10)

ax.scatter(X, Y, s=sizes, c=colors, vmin=0, vmax=100, alpha=0.7, cmap='plasma')

ax.set(xlim=(-20, 20), xticks=np.arange(1, 8),
       ylim=(-20, 20), yticks=np.arange(1, 8))

ax.set_aspect('equal')
ax.grid(True, which='both')

ax.axhline(y=0, color='red')
ax.axvline(x=0, color='blue')

plt.show()