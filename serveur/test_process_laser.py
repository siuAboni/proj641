import matplotlib.pyplot as plt
import numpy as np
import csv

import os

dirname = os.path.dirname(__file__)

plt.style.use('_mpl-gallery-nogrid')

X = []
Y = []

filename_front = os.path.join(dirname, "../data/laser/laser_data_front.csv")
filename_left = os.path.join(dirname, "../data/laser/laser_data_left.csv")
filename_right = os.path.join(dirname, "../data/laser/laser_data_right.csv")

with open(filename_front) as csvfile:
    reader = csv.DictReader(csvfile)
    #reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        for i in range (1, 16):
            X.append(float(row['Seg0' + str(i) + "X"]))
            Y.append(float(row['Seg0' + str(i) + "Y"]))

X = np.array(X)
Y = np.array(Y)

# size and color:
sizes = np.random.uniform(15, 80, len(X))
colors = np.random.uniform(15, 80, len(X))

# plot
fig, ax = plt.subplots()

ax.scatter(X, Y, s=sizes, c=colors, vmin=0, vmax=100)

ax.set(xlim=(-20, 20), xticks=np.arange(1, 8),
       ylim=(-20, 20), yticks=np.arange(1, 8))

ax.set_aspect('equal')
ax.grid(True, which='both')

ax.axhline(y=0, color='red')
ax.axvline(x=0, color='blue')

plt.show()