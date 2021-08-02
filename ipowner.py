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

