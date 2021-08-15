import os
import sys
import pickle
import bz2
import matplotlib.pyplot as plt
import numpy as np

def owner(year, month, map): 
    #""" Find all the ASN and IP prefixes in the radix tree"""
    db="db/rib.%d%02d01.pickle.bz2" %(year,month)
    temp = bz2.BZ2File(db, "rb")
    rtree = pickle.load(temp)
    nodes = rtree.nodes()  
    for rnode in nodes: 
        asn = rnode.data["as"] 
        ip = rnode.prefix  
        if map.get(ip, False):
            if map.get(ip).get(asn, False):
                map[ip][asn] += 1
            else:
                map[ip][asn] = 1
        else:
            map[ip] = {}
            map[ip][asn] = 1
    return map

def verify_date(year, month): 
    filename = "db/rib."+str(year)+str(month)+"01.pickle.bz2"
    if not os.path.exists(filename):
        os.system("python3 monthlydb.py " + str(year) + " " + str(month))

def calc_change(map, output, year):
    data = [0 for i in range (50)]
    for ip in map:
        index = len(ip)
        if index > 50: 
            continue 
        data[index] += 1 
    size = len(map)
    for i in range(50):
        output[year].append(data[i]/size)  
    return output

def average_change(year, output):
    total = 0
    for i in range(50):
        total += output[year][i]*i
    average_changes = total/len(map)
    print("Average Changes " + str(average_changes))
    return average_changes

def writeToFile(output, year, startyear):
    f = open("ownership.txt", "a")
    f.write("Year " + str(startyear + year) + " :  Average change: " + str(average_change(year, output)) + "\n")
    f.write("Year " + str(startyear + year) + " : " + "percentage of ips that changed 0 times: " + str(output[year][0]*100) + "\n")
    for j in range(50):
        if output[year][j] != 0:
            f.write("percentage of ips that changed " + str(j) + " times is: " + str(output[year][j]*100) + "\n")
    f.close()

startyear = int(sys.argv[1]) - 5
startmonth = int(sys.argv[2])
map = {}
output = [[]for i in range(5)] 
for i in range(5):
    year = startyear + i
    for j in range(12):
        month = startmonth + j
        verify_date(year, month)
        map = owner(year, month, map)
        print("length of map " + str(len(map)))
    output = calc_change(map, output, i)
    for j in range(50):
        if output[i][j] != 0:
            print("percentage of ips that changed " + str(j) + " times is: " + str(output[i][j]*100))
    writeToFile(output, i, startyear)


