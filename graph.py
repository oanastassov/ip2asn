import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
plt.style.use('seaborn')

with open('datenumasn.txt') as d:
    lines = d.readlines()
    count = 0
    dates = []
    y = []
    for line in lines:
        date = line.split()[0].split("-")
        year = int(date[0])
        month = int(date[1])
        day = int(date[2]) 
        dates.append(datetime(year = year, month = month, day = day))
        y.append(int(line.split()[1]))
        count = count + 1
plt.plot_date(dates,y,linestyle = "solid", marker = "None")
plt.yscale("log")
plt.show()

