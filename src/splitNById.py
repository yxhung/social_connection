__author__ = 'yxhung'

import os
import shutil
os.chdir('../../whoscall')
# original file => N files
# ogFiles = set('TW', 'BR', 'HK', 'KR')
# ogFile = 'TW'
# N = 200

header = 'time_call_end,local_uid,remote_number,remote_is_contact,' \
         'call_direction,call_is_missed,call_duration,' \
         'remote_country_code,remote_number_prefix,remote_type,' \
         'local_number,local_country_code,local_number_prefix,mcc,mnc,lac,cid'

def splitN(src, N):
    # open N files for splitting big file
    ogFile = src.split('/')[1].split('.')[0]
    if not os.path.exists('call_ctr_n/'+ ogFile):
        os.makedirs('call_ctr_n/'+ ogFile)
    if N == 1:
        shutil.copyfile(src, 'call_ctr_n/'+ ogFile +'/'+ ogFile + '.csv')
        return

    od = {} #open file descriptor
    for n in list(range(0,N)):
        od[n] = open('call_ctr_n/'+ ogFile +'/'+ ogFile +'_'+ str(n) + '.csv', 'w')
        od[n].write(header)

    # scan the big file and split by id to save file
    with open(src) as callData:
        # print(ctr + ', Start!')
        callData.readline() #skip header
        for line in callData:
            l = line.split(',')
            uid = l[1]
            od[hash(uid)%N].write(line)
    # close N files
    for n in list(range(0,N)):
        od[n].close()

def listDirFull(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

ctrs = listDirFull('call_ctr_all')
ctrs.sort()

G = 1000000000
for ctr in ctrs:
    fileSize = os.path.getsize(ctr)
    if fileSize > G:
        N  = int(round(fileSize/G, 0))
    else:
        N = 1
    splitN(ctr, N)
    print(ctr, fileSize, N)

