
import os
import sys
import pickle
import bz2

def all_asn():
    #""" Find all the ASN in the radix tree"""
    db="db/latest.pickle"
    temp = bz2.BZ2File(db, "rb")
    rtree = pickle.load(temp)
    nodes = rtree.nodes() 
    asns = {}
    for rnode in nodes:
        asns.add(rnode.data["as"])
    size = len(asns)
    return size

def writeToFile(year, month):
    f = open("datenumasn.txt", "a")
    f.write(str(year) +"-"+ str(month) + "-01  " + all_asn())
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




#loop through each year
#loop through each month
# hard code the day
# verify date 
# if no date call monthly db
# find the number of nodes in the radix tree and add to set 
# write the date and # of asns to file

# 2020-12-01   #asns
