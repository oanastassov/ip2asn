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

plot1 = plt.subplot2grid((3, 3), (0, 0), rowspan=2, colspan=2)
plot2 = plt.subplot2grid((3, 3), (2, 0), rowspan=2, colspan=2)

plot1.plot(dates,y,linestyle = "solid", marker = "None")
plot1.set_title('# ASNs over Time')

plot2.plot(dates,y,linestyle = "solid", marker = "None")
plot2.set_title('Logarithmic Scale of # ASNs over Time')

plt.tight_layout()
plt.yscale("log")
plt.show()
