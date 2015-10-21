__author__ = 'yxhung'
import os
import csv
import time

DIRWHOSCALL = '/home/yaxuan/mmnas2/yaxuan/whoscall'
os.chdir(DIRWHOSCALL)
# list all country code
ctrs = []
with open("country_code_all.txt") as data:
    reader = csv.reader(data, delimiter=' ')
    next(reader)  # skip header row
    ctrs = [line[1] for line in reader]

with open('call_all/call_20150501.csv') as calldata:
        header = calldata.readline()

# open file for all country f1 = open("cty_cd", w)
od = {} #open file descriptor
for ctr in ctrs:
    od[ctr] = open('call_ctr_all/'+ ctr + '.csv', 'a')
    # od[ctr].write(header)
    #print(od[ctr])
    #print(od[ctr])
    #open(ctr+'.csv', 'w')

# read filter data line by line
calls = os.listdir('call_f')
calls.sort()
#partCalls = calls[0:30]

for call in calls:
    # start = time.time()
    with open('call_f/'+ call) as callData:
        print(call + ', Start!')
        callData.readline() #skip header
        for line in callData:
            l = line.split(',')
            ctr = l[11]
            if od.get(ctr) is None:
                continue
            od[ctr].write(line)
        print('Done!')
    # done = time.time()
    # elapsed = done - start
    # print(elapsed)

# close file for all country
for ctr in ctrs:
    od[ctr].close()
