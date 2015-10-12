__author__ = 'yxhung'
import os
import csv
import time
os.chdir('../mmnas2/yaxuan/whoscall')
# list all country code
ctrs = []
with open("country_code_all.txt") as data:
    reader = csv.reader(data, delimiter=' ')
    next(reader)  # skip header row
    ctrs = [line[1] for line in reader]

with open('call_all/call_20150501.csv') as calldata:
        header = calldata.readline() #skip header

# open file for all country f1 = open("cty_cd", w)
od = {} #open file descriptor
for ctr in ctrs:
    od[ctr] = open('call_ctr/'+ ctr + '.csv', 'w')
    od[ctr].write(header)
    #print(od[ctr])
    #open(ctr+'.csv', 'w')

# read filter data line by line
call_filter = os.listdir('call_f')
for file in call_filter:
    with open('call_f/'+file) as calldata:
        calldata.readline() #skip header
        for line in calldata:
            l = line.split(',')
            ctr = l[11]
            od[ctr].write(line)
            #print(line, file = od[ctr])

# close file for all country
for ctr in ctrs:
    od[ctr].close()
