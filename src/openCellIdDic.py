__author__ = 'yxhung'
import os
import json
import time


os.chdir('../../whoscall')
def listDirFull(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

# 2. Create the dictionary for cellId to latlon
cidDic = {}
cidFiles = listDirFull('openCid')
cidFiles.sort()


start = time.time()
for file in cidFiles:
    with open(file) as Data:
        print(Data.readline()) #skip header
        for line in Data:
            l = line.split(',')
            mcc, mnc, lac, cid = l[1:5]
            (lon, lat) = (l[6:8])
            setCid = mcc+ ','+ mnc+ ','+ lac+ ','+ cid
            setCrd = (lon, lat)
            cidDic[setCid] = setCrd

            # cellIdDic.setdefault(setCid, []).append(setCrd)

done = time.time()
elapsed = done - start
print(elapsed)

# Writing JSON data
with open('openCid/openCidDic.csv', 'w') as outfile:
    json.dump(cidDic, outfile)
print('Done!')