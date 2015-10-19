__author__ = 'yxhung'
import os
import json
import urllib
import urllib.request
import urllib.error
from urllib.error import URLError, HTTPError
os.chdir('../../whoscall')
# query url setting

geoUrl = 'http://nominatim.openstreetmap.org/reverse'
cidUrl = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCDlo0xkOqsGUZ13d83ve7YNiZq3AQmQWw'


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
    # resp = urllib.request.urlopen(req)
    # response = resp.read().decode('utf8')
    # response = json.loads(response)
    # (latitude, longitude) = response.get('location').get('lat'), response.get('location').get('lng')
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
        # return location


# response = {}
# try:
#     resp = urllib.request.urlopen(req)
# except HTTPError as e:
#     print('Error code: ', e.code, e.reason)
# else:
#     response = resp.read().decode('utf8')
#     response = json.loads(response)
# finally:
#     location = response.get('location')
#     (latitude, longitude) = location.get('lat'), location.get('lng')
#

# mcc mnc      cid   lac     lat       lon
# 460   0    14021 22305 30.8772 120.41900

# url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCDlo0xkOqsGUZ13d83ve7YNiZq3AQmQWw'
# values = {
#     "cellTowers": [
#         {
#             "cellId": 14021,
#             "locationAreaCode": 22305,
#             "mobileCountryCode": 460,
#             "mobileNetworkCode": 0
#         },
#     ]
# }
# data = json.dumps(values).encode('utf8')
# req = urllib.request.Request(url, data, headers={'content-type': 'application/json'})
# resp = urllib.request.urlopen(req)
# result = resp.read().decode('utf8')
# json.loads(result)
# json.loads(result)['location']['lng']




# useragent="RCurl", referer="http://www.omegahat.org"
def revGeolocate(latitude, longitude):
    url = '%s?format=json&accept-language=en-US&email=yxhung@gmail.com' \
          '&lat=%s&lon=%s' % (geoUrl, str(latitude), str(longitude))
    response = urllib.request.urlopen(url).read().decode('utf8')
    response = json.loads(response)
    address = response['address']
    (ccd, ctr, sta, std, reg, cty, cit, ctd) = (address.get('country_code'),
                                            address.get('country'),
                                            address.get('state'),
                                            address.get('state_district'),
                                            address.get('region'),
                                            address.get('county'),
                                            address.get('city'),
                                            address.get('city_district'))
    return ccd, ctr, sta, std, reg, cty, cit, ctd



header = 'mcc,mnc,lac,cid,lat,lon,ccd,ctr,sta,std,reg,cty,cit,ctd'
cidFiles = os.listdir('uiqCid')
cidFiles.sort()
for cidFile in cidFiles:
    with open('uiqCid/'+ cidFile) as cidData:
        print(cidFile + ', Start!')
        cidData.readline() #skip header

        corData = open('uiqCidCord/'+ cidFile, 'w')
        corData.write(header+'\n')

        for line in cidData:
            l = line.rstrip('\n').split(',')
            print(l)
            (mcc, mnc, lac, cid) = l
            # query coordinate
            # (latitude, longitude) = queryCoordinate(cid, lac, mnc, mcc)
            response = queryCoordinate(cid, lac, mnc, mcc)
            if len(response) == 0:
                continue

            (latitude, longitude) = response.get('location').get('lat'), response.get('location').get('lng')
            print(latitude, longitude)

            # reverse geocoding
            (ccd, ctr, sta, std, reg, cty, cit, ctd) = revGeolocate(latitude, longitude)
            print(ccd, ctr)

            l.extend((latitude, longitude, ccd, ctr, sta, std, reg, cty, cit, ctd))
            newLine = ",".join(map(str, l))
            corData.write(newLine + '\n')

        corData.close()

        print(cidFile + ', Done!')