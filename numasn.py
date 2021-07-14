import os
import sys
import pickle
import bz2

def all_asn(year, month):
    #""" Find all the ASN in the radix tree"""
    db="db/rib.%d%02d01.pickle.bz2" %(year,month)
    temp = bz2.BZ2File(db, "rb")
    rtree = pickle.load(temp)
    nodes = rtree.nodes() 
    asns = set()
    for rnode in nodes: 
        asns.add(rnode.data["as"]) 
    size = len(asns)
    return size

def writeToFile(year, month):
    f = open("datenumasn.txt", "a")
    f.write(str(year) +"-"+ str(month).zfill(2) + "-01  " + str(all_asn(year, month)) + "\n")
    f.close()


def verify_date(year, month): 
    filename = "db/rib."+str(year)+str(month)+"01.pickle.bz2"
    if not os.path.exists(filename):
        os.system("python3 monthlydb.py " + str(year) + " " + str(month))

startyear = int(sys.argv[1]) - 10
startmonth = int(sys.argv[2])

for i in range(10):
    year = startyear + i
    for j in range(12):
        month = startmonth + j
        verify_date(year, month)
        writeToFile(year, month)
        print("The " + str(year) +" and " + str(month) + " is completed")
