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
        data[index] += 1 #adds number of changes to the array
    size = len(map)
    for i in range(50):
        output[year].append(data[i]/size)  #gets percentage and puts it in output array
    return output

# def writeToFile(year, month, map):
#     f = open("averageownership.txt", "a")
#     f.write("Average number of ip's owned by an ASN in year " + str(year) + " : " + str(calculate_average(map)) + "\n" + "Average lenth of ip ownership by an ASN in year " + str(year) + " : " + str(timeowned_average(map)) + "\n")
#     f.close()

def to_graph(output, year):
    x = [i for i in range(50)]
    plt.bar(x, output[year])
    plt.show()

startyear = int(sys.argv[1]) - 5
startmonth = int(sys.argv[2])
map = {}
output = [[]for i in range(5)] #[[0 for i in range (5)] for j in range (50)]# makes 2d array of correct size with 0s, then replaces
for i in range(5):
    year = startyear + i
    for j in range(12):
        month = startmonth + j
        verify_date(year, month)
        map = owner(year, month, map)
        print(len(map))
    #writeToFile(year, month, map)
    output = calc_change(map, output, i)
    to_graph(output, i)

# % hasnt changed at all
# graphs of when has changed
# x = range of changes
# y = franctions of ips
# make a new graph for each year