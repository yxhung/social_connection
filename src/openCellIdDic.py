__author__ = 'yxhung'
import os
import json
import time


os.chdir('../../whoscall')
def listDirFull(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

# 2. Create the dictionary for cellId to latlon
cellIdDic = {}
cellIdFiles = listDirFull('openCellId')
cellIdFiles.sort()


start = time.time()
for file in cellIdFiles:
    with open(file) as Data:
        print(Data.readline()) #skip header
        # i = 0
        for line in Data:
            # i += 1
            # if i>10:
            #     break
            # print(line,'\n')
            l = line.split(',')
            (mcc, mnc, lac, cid) = (l[1:5])
            (lon, lat) = (l[6:8])
            setCid = mcc+ ','+ mnc+ ','+ lac+ ','+ cid
            setCrd = (lon, lat)
            cellIdDic[setCid] = setCrd

            # cellIdDic.setdefault(setCid, []).append(setCrd)

done = time.time()
elapsed = done - start
print(elapsed)

# Writing JSON data
with open('openCellId/cellIdDic.csv', 'w') as outfile:
    json.dump(cellIdDic, outfile)
print('Done!')