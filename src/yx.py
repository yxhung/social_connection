__author__ = 'yxhung'


def sanitize(time_string):
    if '-' in time_string:
        splitter = '-'
    elif ':' in time_string:
        splitter = ':'
    else:
        return(time_string)

    (mins, secs) = time_string.split(splitter)
    return(mins + '.' + secs)

def open_file(file_name):
    try:
        with open(file_name) as f:
            data = f.readline()
        list_name = data.strip().split(',')
        return list_name
    except IOError as err:
        print('File error:' + str(err))
        return None

"""
# read data to list
try:
    with open('james.txt') as jaf:
        data = jaf.readline()
    james = data.strip().split(',')

    with open('sarah.txt') as saf:
        data = saf.readline()
    sarah = data.strip().split(',')

    with open('julie.txt') as juf:
        data = juf.readline()
    julie = data.strip().split(',')

    with open('mikey.txt') as mif:
        data = mif.readline()
    mikey = data.strip().split(',')
except IOError as err:
    print('File error:' + str(err))
"""

james = open_file('james.txt')
print(sorted(set([sanitize(each_t) for each_t in james]))[0:3])

"""
# clean data
cl_james = []
cl_sarah = []
cl_julie = []
cl_mikey = []

for each_t in james:
    cl_james.append(sanitize(each_t))
for each_t in sarah:
    cl_sarah.append(sanitize(each_t))
for each_t in julie:
    cl_julie.append(sanitize(each_t))
for each_t in mikey:
    cl_mikey.append(sanitize(each_t))

# clean data use one line code
cl_james = [sanitize(each_t) for each_t in james]
cl_sarah = [sanitize(each_t) for each_t in sarah]
cl_julie = [sanitize(each_t) for each_t in julie]
cl_mikey = [sanitize(each_t) for each_t in mikey]



# filter => set()
unique_james = []
unique_julie = []
unique_mikey = []
unique_sarah = []

for each_t in cl_james:
    if each_t not in unique_james:
        unique_james.append(each_t)
print(unique_james[0:3])

for each_t in cl_julie:
    if each_t not in unique_julie:
        unique_julie.append(each_t)
print(unique_julie[0:3])


for each_t in cl_mikey:
    if each_t not in unique_mikey:
        unique_mikey.append(each_t)
print(unique_mikey[0:3])


for each_t in cl_sarah:
    if each_t not in unique_sarah:
        unique_sarah.append(each_t)
"""