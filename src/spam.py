__author__ = 'yxhung'
# (2) filter the spam
import os
import csv
import time

DIR_WHOSCALL = '../mmnas2/yaxuan/whoscall'
os.chdir(DIR_WHOSCALL)


# os.chdir('/Users/yxhung/Dropbox/workspace/whoscall_local')



def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def listdir_pattern(d, pattern):
    return [os.path.join(d, f) for f in os.listdir(d) if pattern in f]


spams = {}
spam_dirs = listdir_fullpath('call_spam')
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


def detect_not_spam(line):
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


calls = os.listdir('call_all')
for call in calls:
    #start = time.time()

    with open('call_all/' + call) as calldata:
        newcall = open('call_f/' + call, 'w')
        newcall.write(calldata.readline())  # write header
        for line in calldata:
            if detect_not_spam(line):
                newcall.write(line)
        newcall.close()

    #done = time.time()
    #elapsed = done - start
    #print(elapsed)
