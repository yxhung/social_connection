__author__ = 'yxhung'
# (2) filter the spam
import os
import csv
import time

DIRWHOSCALL = '/home/yaxuan/mmnas2/yaxuan/whoscall'
os.chdir(DIRWHOSCALL)

def listDirFull(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def listDirPattern(d, pattern):
    return [os.path.join(d, f) for f in os.listdir(d) if pattern in f]


def detectNotSpam(line):
    l = line.split(',')
    if (len(l) != 17):
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

def strToBool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError # evil ValueError that doesn't tell you what the wrong value was

# 1 create the spam dic
spams = {}
spam_dirs = listDirFull('call_spam')
try:
    for each_spam in spam_dirs:

        spam = {}
        with open(each_spam, newline='') as data_spam:
            reader = csv.reader(data_spam, delimiter=',')
            next(reader)  # skip header row
            # spam = {rows[2]:rows[3] for rows in reader}

            for line in reader:
                lnum, ctr, md5num, ct = line
                spam[md5num] = ct

        spams[ctr] = spam
except IOError:
    print('data missing')

print('Create spam list, Done!')



# setting the part
calls = os.listdir('call_all')
calls.sort()

import configparser
config = configparser.ConfigParser()
config.read('/home/yaxuan/mmnas2/yaxuan/python/social_connection/conf/config')

o1t1 = config['DEFAULT']['o1t1']
o1t2 = config['DEFAULT']['o1t2']
o1t3 = config['DEFAULT']['o1t3']
o1t4 = config['DEFAULT']['o1t4']

o2t1 = config['DEFAULT']['o2t1']
o2t2 = config['DEFAULT']['o2t2']
o2t3 = config['DEFAULT']['o2t3']

o3t1 = config['DEFAULT']['o3t1']
o3t2 = config['DEFAULT']['o3t2']
o3t3 = config['DEFAULT']['o3t3']

if strToBool(o1t1):
    partCalls = calls[0:10]
if strToBool(o1t2):
    partCalls = calls[10:20]
if strToBool(o1t3):
    partCalls = calls[20:30]
if strToBool(o1t4):
    partCalls = calls[30:40]

if strToBool(o2t1):
    partCalls = calls[40:50]
if strToBool(o2t2):
    partCalls = calls[50:60]
if strToBool(o2t3):
    partCalls = calls[60:70]

if strToBool(o3t1):
    partCalls = calls[70:80]
if strToBool(o3t2):
    partCalls = calls[80:90]
if strToBool(o3t3):
    partCalls = calls[90:99]

print('Set the part files, Done!')

# read origin data line by line and filter the spam num
for call in partCalls:
    #start = time.time()
    with open('call_all/' + call) as calldata:
        print(call + ', Start!')
        newcall = open('call_f/' + call, 'w')
        newcall.write(calldata.readline())  # write header
        for line in calldata:
            if detectNotSpam(line):
                newcall.write(line)
        newcall.close()
        print('Done!')

    #done = time.time()
    #elapsed = done - start
    #print(elapsed)
