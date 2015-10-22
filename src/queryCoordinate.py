__author__ = 'yxhung'

import os
import json
import time

os.chdir('../../whoscall')

def str2Bool(v):
  return v.lower() in ("yes", "true", "t", "1")

# Reading openCellId database
with open('openCid/openCidDic.csv') as infile:
    cellIdDic = json.load(infile)
print('Read Dic Done!')


# global lat, lon
header = 'mcc,mnc,lac,cid,lat,lon\n'
cidFiles = os.listdir('uiqCid')
cidFiles.sort()


for cidFile in cidFiles:
# cidFile = cidFiles[0]
    with open('uiqCid/'+ cidFile) as cidData:
        print(cidFile + ', Start!')

        cidData.readline() #skip header

        # open new file to save the query data
        corData = open('uiqCidCord/'+ cidFile, 'w')
        corData.write(header)
        i = 1
        j = 1
        for line in cidData:
            i += 1
            l = line.rstrip('\n').split(',')
            (mcc, mnc, lac, cid) = l
            setCid = mcc+ ','+ mnc+ ','+ lac+ ','+ cid
            # query coordinate
            if cellIdDic.get(setCid) is None:
                corData.write(setCid + ',None,None\n')
                j += 1
                continue
            setCrd = cellIdDic[setCid]
            lon, lat = setCrd
            corData.write(setCid + ',' + lat + ',' + lon + '\n')


        print(j, i, '\n')

        corData.close()
