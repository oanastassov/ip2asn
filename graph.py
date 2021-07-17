import matplotlib.pyplot as plt
import numpy as np

with open('datenumasn.txt') as d:
    lines = d.readlines()
    x = [line.split()[0] for line in lines]
    y = [line.split()[1] for line in lines]
plt.plot(x,y)
plt.show()
