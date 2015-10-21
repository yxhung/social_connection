__author__ = 'yxhung'
import os
import csv
import time

DIRWHOSCALL = '/home/yaxuan/mmnas2/yaxuan/whoscall'
# os.chdir(DIRWHOSCALL)
os.chdir('../../whoscall')

ctrs = os.listdir('call_ctr_all')
ctrs.sort()

# header = 'time_call_end,local_uid,remote_number,remote_is_contact,' \
#          'call_direction,call_is_missed,call_duration,' \
#          'remote_country_code,remote_number_prefix,remote_type,' \
#          'local_number,local_country_code,local_number_prefix,mcc,mnc,lac,cid'

header = 'mcc,mnc,lac,cid\n'
for ctr in ctrs:
    with open('call_ctr_all/'+ ctr) as callData:
        print(ctr + ', Start!')
        callData.readline() #skip header
        cidData = set()
        for line in callData:
            l = line.split(',')
            (mcc, mnc, lac, cid) = l[13:17]
            if (mcc == '-1') or (mnc == '-1') or (lac == '-1') or (cid == '-1'):
                continue

            setCid = mcc+ ','+ mnc+ ','+ lac+ ','+ cid
            cidData.add(setCid)
    with open('uiqCid2/'+ ctr, 'w') as uiqCid:
        uiqCid.write(header)
        for elt in cidData:
            uiqCid.write(elt)
        print(ctr + ', Done!')



