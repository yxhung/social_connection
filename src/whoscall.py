__author__ = 'yxhung'

import os
print(os.getcwd())
os.chdir('../mmnas2/yaxuan/whoscall')
from geopy.geocoders import Nominatim
geolocator = Nominatim()

# (1) use lat/lon coordinates to find out city/country

try:
    with open('../location.csv') as data:
    #with open('location_city_text.txt', 'w') as location_city:
        for each_line in data:
            try:
                (mcc, mnc, cid, lac, lat, lon) = data.readline().split(',')
                location_all = geolocator.reverse(lat, lon)
                print(location_all.address, '\n')
                #print(, file=location_city)
            except ValueError:
                pass

except IOError:
    print('data missing')









