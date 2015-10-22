__author__ = 'yxhung'

import os
import json
import urllib.request
import urllib.error
from urllib.error import HTTPError
import re
import time
# from geopy.geocoders import Nominatim
# geolocator = Nominatim()
os.chdir('../../whoscall')


# query url setting
geoUrl = 'http://nominatim.openstreetmap.org/reverse'


def revGeolocate(latitude, longitude):
    time.sleep(1)
    url = '%s?format=json&accept-language=en-US&email=yxhung@gmail.com' \
          '&lat=%s&lon=%s' % (geoUrl, str(latitude), str(longitude))
    response = {}
    try:
        resp = urllib.request.urlopen(url)
    except HTTPError as e:
        print('Error code: ', e.code, e.reason)
    else:
        response = resp.read().decode('utf8')
        response = json.loads(response)
    finally:
        return response

def writeFile(l, ccd, ctr, sta, std, reg, cty, cit, ctd, file):
    l.extend((ccd, ctr, sta, std, reg, cty, cit, ctd))
    newLine = ",".join(map(str, l))
    file.write(newLine + '\n')

# global lat, lon
header = 'mcc,mnc,lac,cid,lat,lon,ccd,ctr,sta,std,reg,cty,cit,ctd\n'
cidFiles = os.listdir('uiqCidCord')
cidFiles.sort()


for cidFile in cidFiles:
# cidFile = cidFiles[0]
    with open('uiqCidCord/'+ cidFile) as cidData:
        print(cidFile + ', Start!')

        cidData.readline() #skip header

        # open new file to save the query data
        ctyData = open('uiqCidCty/'+ cidFile, 'w')
        ctyData.write(header)

        i = 1
        j = 1
        for line in cidData:
            i += 1
            l = line.rstrip('\n').split(',')
            # if len(l) == 4:
            #     continue
            (mcc, mnc, lac, cid, lat, lon) = l
            print((mcc, mnc, lac, cid, lat, lon))

            if lat == 'None' or lon == 'None':
                writeFile(l, ccd, ctr, sta, std, reg, cty, cit, ctd, ctyData)
                continue


            # reset query data
            ccd = ctr = sta = std = reg = cty = cit = ctd = None


            # location = geolocator.reverse((lat,lon)).raw
            # if location.get('address') is None:
            #     writeFile(l, ccd, ctr, sta, std, reg, cty, cit, ctd, ctyData)
            #     continue
            # address = location['address']

            addResp = revGeolocate(lat, lon)
            if len(addResp) == 0:
                writeFile(l, ccd, ctr, sta, std, reg, cty, cit, ctd, ctyData)
                continue

            if re.search('error', str(addResp)):
                print('error: Unable to geocode')
                writeFile(l, ccd, ctr, sta, std, reg, cty, cit, ctd, ctyData)
                continue

            address = addResp['address']

            (ccd, ctr, sta, std, reg, cty, cit, ctd) = (address.get('country_code'),
                                            address.get('country'),
                                            address.get('state'),
                                            address.get('state_district'),
                                            address.get('region'),
                                            address.get('county'),
                                            address.get('city'),
                                            address.get('city_district'))

            writeFile(l, ccd, ctr, sta, std, reg, cty, cit, ctd, ctyData)
            # del ccd, ctr, sta, std, reg, cty, cit, ctd

        print(j, i, '\n')

        ctyData.close()
