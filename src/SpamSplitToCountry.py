__author__ = 'yxhung'

import os
import csv
DIR_WHOSCALL = '../mmnas2/yaxuan/whoscall'
os.chdir(DIR_WHOSCALL)
#os.chdir('/Users/yxhung/Dropbox/workspace/whoscall_local')


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def listdir_pattern(d, pattern):
    return [os.path.join(d,f) for f in os.listdir(d) if pattern in f]

def detect_not_spam(line):
    l = line.split(',')
    if(len(l) != 17):
        return False
    ctr = l[11]
    local_num = l[10]
    remote_num = l[2]
    if spams.get(ctr) is None:
        return True
    if spams[ctr].get(local_num) is None and spams[ctr].get(remote_num) is None:
        return True
    else:
        return False

# 1 create the spam dic
spams = {}
spam_dirs = listdir_fullpath('call_spam')
try:
    for each_spam in spam_dirs:

        spam = {}
        with open(each_spam, newline='') as data_spam:
            reader = csv.reader(data_spam, delimiter=',')
            next(reader)  # skip header row
            #spam = {rows[2]:rows[3] for rows in reader}
            for line in reader:
                lnum, ctr, md5num, ct = line
                spam[md5num] = ct

        spams[ctr] = spam
except IOError:
    print('data missing')


# get all country
ctrs = []
with open("country_code_all.txt") as data:
    reader = csv.reader(data, delimiter=' ')
    next(reader)  # skip header row
    ctrs = [line[1] for line in reader]

# get call header
with open('call_all/call_20150501.csv') as calldata:
        header = calldata.readline() #skip header

# open file for all country
od = {} #open file descriptor
for ctr in ctrs:
    od[ctr] = open('call_ctr/'+ ctr + '.csv', 'w')
    od[ctr].write(header)
    #print(od[ctr])
    #open(ctr+'.csv', 'w')

# read origin data line by line
calls = os.listdir('call_all')
for call in calls:
    with open('call_all/'+ call) as calldata:

        calldata.readline() #skip header
        for line in calldata:
            if detect_not_spam(line):
                od[ctr].write(line)
            """
            l = line.split(',')
            if(len(l) != 17):
                next()

            ctr = l[11]
            local_num = l[10]
            remote_num = l[2]
            if (local_num not in spams[ctr]) & (remote_num not in spams[ctr]):
                od[ctr].write(line)
            """


# close file for all country
for ctr in ctrs:
    od[ctr].close()
