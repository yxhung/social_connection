__author__ = 'yxhung'
import os
import json
import urllib.request
import urllib.error
from urllib.error import HTTPError
import time
# os.chdir('../../whoscall')

# query url setting
geoUrl = 'http://nominatim.openstreetmap.org/reverse'

cidUrl = 'https://www.googleapis.com/geolocation/v1/geolocate?key='
apiKey = 'AIzaSyCDlo0xkOqsGUZ13d83ve7YNiZq3AQmQWw'
cidUrl = cidUrl+apiKey

def queryCoordinate(cid, lac, mnc, mcc):
    cidStr = {
        "cellTowers": [
            {
                "cellId": int(cid),
                "locationAreaCode": int(lac),
                "mobileCountryCode": int(mcc),
                "mobileNetworkCode": int(mnc)
            }

        ]
    }
    queryBody = json.dumps(cidStr).encode('utf8')
    req = urllib.request.Request(cidUrl, queryBody, headers={'content-type': 'application/json'})

    response = {}
    try:
        resp = urllib.request.urlopen(req)
    except HTTPError as e:
        print('Error code: ', e.code, e.reason)
    else:
        response = resp.read().decode('utf8')
        response = json.loads(response)
    finally:
        return response


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


def writeFile(l, latitude, longitude, ccd, ctr, sta, std, reg, cty, cit, ctd, file):
    l.extend((latitude, longitude, ccd, ctr, sta, std, reg, cty, cit, ctd))
    newLine = ",".join(map(str, l))
    file.write(newLine + '\n')


header = 'mcc,mnc,lac,cid,lat,lon,ccd,ctr,sta,std,reg,cty,cit,ctd'
cidFiles = os.listdir('uiqCid')
cidFiles.sort()
for cidFile in cidFiles:
    with open('uiqCid/'+ cidFile) as cidData:
        print(cidFile + ', Start!')

        cidData.readline() #skip header

        # open new file to save the query data
        corData = open('uiqCidCord/'+ cidFile, 'w')
        corData.write(header+'\n')

        for line in cidData:
            l = line.rstrip('\n').split(',')
            (mcc, mnc, lac, cid) = l
            # reset query data
            latitude = longitude = ccd = ctr = sta = std = reg = cty = cit = ctd = None

            # query coordinate
            # (latitude, longitude) = queryCoordinate(cid, lac, mnc, mcc)
            crdResp = queryCoordinate(cid, lac, mnc, mcc)
            if len(crdResp) == 0:
                writeFile(l, latitude, longitude, ccd, ctr, sta, std, reg, cty, cit, ctd, corData)
                continue

            (latitude, longitude) = crdResp.get('location').get('lat'), crdResp.get('location').get('lng')

            # reverse geocoding
            # (ccd, ctr, sta, std, reg, cty, cit, ctd) = revGeolocate(latitude, longitude)
            addResp = revGeolocate(latitude, longitude)
            if len(crdResp) == 0:
                writeFile(l, latitude, longitude, ccd, ctr, sta, std, reg, cty, cit, ctd, corData)
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

            writeFile(l, latitude, longitude, ccd, ctr, sta, std, reg, cty, cit, ctd, corData)

        corData.close()

        print(cidFile + ', Done!')