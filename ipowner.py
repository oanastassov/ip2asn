#want to see how many times owner of prefix changes. 
#how long does a certain asn own an IP prefix. How can we do this? 
#If figure out a way then try it. 

#Program runs and compares all the asns with all the prefixes. 
#Takes note of each time that the asn for an IP changes. 

#checkes if an ip and an asn are connected. takes note of how long an ip and an asn are connected. keeps track of all ip and asn connections separately. 

#create a dictionary of all ASNS and when IPs belong to them 
#keep track of when the IP became part of that asn and when it stopped belonging to that asn. keep track of the length of time. 
# repeat this for all asns 
#read 
#split
#compare
#store output data

#Data Processing/ reading
#for loop that gets the data at the start time
#for loop that loops through each line in the file
    #Split the data on each line
    #store data in 2D grid (list of lists)
        #increment by one for each set of ip and asn (shows # of months that ownership stayed the same)

#number of non-zero ints in a row = number of times ip ownership changed (if each row represents an ip)
#number in each row/ column intersection = # of months that ownership stayed the same

#hitmap

#set of dictionaries

import os
import sys
import pickle
import bz2

def owner(year, month, map): 
    print("Processing started")
    #""" Find all the ASN and IP prefixes in the radix tree"""
    db="db/rib.%d%02d01.pickle.bz2" %(year,month)
    temp = bz2.BZ2File(db, "rb")
    rtree = pickle.load(temp)
    nodes = rtree.nodes()  
    for rnode in nodes: 
        asn = rnode.data["as"] 
        ip = rnode.prefix  
        if map.get(asn, False):
            if map.get(asn).get(ip, False):
                map[asn][ip] += 1
            else:
                map[asn][ip] = 1
        else:
            map[asn] = {}
            map[asn][ip] = 1
    print("processing done")
    return map
#for each pair of ip asn 
#check if asn is already in outer dict
#if not, add it
#if yes, go into inner dict at that asn and check if ip is there
#if not add it
#if yes then increase counter 

def verify_date(year, month): 
    filename = "db/rib."+str(year)+str(month)+"01.pickle.bz2"
    if not os.path.exists(filename):
        os.system("python3 monthlydb.py " + str(year) + " " + str(month))

def calculate_average(map):
    sum = 0
    for asn in map:
        sum += len(map[asn]) 
    return sum/len(map)

def timeowned_average(map):
    sum = 0
    countip = 0
    for asn in map:
        for ip in map[asn]:
            sum += map[asn][ip]
            countip += 1
    return sum/countip

def writeToFile(year, month, map):
    f = open("averageownership.txt", "a")
    f.write("Average number of ip's owned by an ASN in year " + str(year) + " : " + str(calculate_average(map)) + "\n" + "Average lenth of ip ownership by an ASN in year " + str(year) + " : " + str(timeowned_average(map)) + "\n")
    f.close()

startyear = int(sys.argv[1]) - 10
startmonth = int(sys.argv[2])
map = {}
for i in range(10):
    year = startyear + i
    for j in range(12):
        month = startmonth + j
        verify_date(year, month)
        map = owner(year, month, map)
        print(len(map))
    writeToFile(year, month, map)

