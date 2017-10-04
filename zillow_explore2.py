from bokeh.layouts import column
dir = "/Users/apple/Documents/zillow/data/"
dir = "/Users/T162880/Documents/Programs/zillow/"
properties_2016 = "properties_2016.csv"
properties_2017 = "properties_2017.csv"
train_2016 = "train_2016_v2.csv"
train_2017 = "train_2017.csv"
sample_submission = "sample_submission.csv"
my_submission = "my_submission.csv"
zillow_columns = """
parcelid,airconditioningtypeid,architecturalstyletypeid,basementsqft,bathroomcnt,bedroomcnt,buildingclasstypeid,buildingqualitytypeid,calculatedbathnbr,decktypeid,finishedfloor1squarefeet,calculatedfinishedsquarefeet,finishedsquarefeet12,finishedsquarefeet13,finishedsquarefeet15,finishedsquarefeet50,finishedsquarefeet6,fips,fireplacecnt,fullbathcnt,garagecarcnt,garagetotalsqft,hashottuborspa,heatingorsystemtypeid,latitude,longitude,lotsizesquarefeet,poolcnt,poolsizesum,pooltypeid10,pooltypeid2,pooltypeid7,propertycountylandusecode,propertylandusetypeid,propertyzoningdesc,rawcensustractandblock,regionidcity,regionidcounty,regionidneighborhood,regionidzip,roomcnt,storytypeid,threequarterbathnbr,typeconstructiontypeid,unitcnt,yardbuildingsqft17,yardbuildingsqft26,yearbuilt,numberofstories,fireplaceflag,structuretaxvaluedollarcnt,taxvaluedollarcnt,assessmentyear,landtaxvaluedollarcnt,taxamount,taxdelinquencyflag,taxdelinquencyyear,censustractandblock
"""

overall_mean = "0.0115"
low_sample = 500

useful_columns = """
parcelid,
logerror,
architecturalstyletypeid,
basementsqft,
bathroomcnt,
bedroomcnt,
buildingclasstypeid,
buildingqualitytypeid,
calculatedbathnbr,
garagecarcnt,
latitude,
longitude,
lotsizesquarefeet,
regionidzip,
numberofstories,
yearbuilt,
taxvaluedollarcnt,
calculatedfinishedsquarefeet,
"""

zcolumns = { value: index for (index, value) in enumerate(zillow_columns.strip().split(",")) }
ucolumns = { value: index for (index, value) in enumerate("".join([ line.strip() for line in useful_columns.splitlines()]).split(",")) }
ucolumns2 = [ c for c in "".join([ line.strip() for line in useful_columns.splitlines()]).split(",") if len(c) != 0]

def cat_sqrt(value):
    try:
        sqrt = float(value)
    except:
        return 0
    begin = 500
    step = 500
    for i in range(7):
        if sqrt >= float(begin + i * step) and sqrt < float(begin + (i+1) * step):
            return i+1
    return 0

def cat_year(value):
    try:
        year = int(value.split(".")[0])
    except:
        return 0
    if year >= 1920 and year < 1940: return 1
    #if year >= 1930 and year < 1940: return 2
    if year >= 1940 and year < 1960: return 3
    #if year >= 1950 and year < 1960: return 4
    if year >= 1960 and year < 1980: return 5
    #if year >= 1970 and year < 1980: return 6
    if year >= 1980 and year < 2000: return 7
    #if year >= 1990 and year < 2000: return 8
    if year >= 2000 and year < 2010: return 9
    return 0

def cat_dollar(value):
    try:
        dollar = float(value)
    except:
        return 0
    if dollar < 10000.0: return 0
    if dollar > 2000000.0: return 0
    if dollar < 500000.0: return 1
    return 2

features = [
          ["yearbuilt", cat_year, ],
          ["calculatedfinishedsquarefeet", cat_sqrt, ],
          ["taxvaluedollarcnt", cat_dollar, ],
]

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    with open(dir+train_2016) as fd: lines = fd.readlines()[1:]
    tdict = { values[0]: values[:2] for values in [ line.split(",") for line in lines] }
    with open(dir+properties_2016) as fd:
        header = fd.readline()
        while True:
            line = fd.readline()
            if not line: break
            values = line.split(",")
            parcelid = values[zcolumns["parcelid"]]
            if parcelid not in tdict: continue
            tdict[parcelid] += [ values[zcolumns[c]] for c in ucolumns2[2:] ]
    bset = dict()
    for parcelid in tdict:
        values = tdict[parcelid]
        index = tuple([feature[1](values[ucolumns[feature[0]]]) for feature in features])
        if index not in bset: bset[index] = list()
        bset[index].append(tdict[parcelid])
    #for index in sorted: print("{}:{}".format(index, len(bset[index])))
    print("done")
    #logerrors = [ float(values[1]) for values in tdict.values()]
    #logerrors = [ logerror for logerror in logerrors if logerror > -.2 and logerror < .2 ]
    #plt.hist(logerrors, bins=20)
    #plt.show()

    sorted = [ index for index in bset ]; sorted.sort()
    full = [ [ float(item[ucolumns["logerror"]]) for item in bset[index]] for index in sorted ]
    trimmed = [ [logerror for logerror in bucket if logerror > -.2 and logerror < .2] for bucket in full ]
    ctrimmed = [ len(bucket) for bucket in trimmed ]
    bands = [ (-0.2+ii*.04, -0.2+ii*.04+.04) for ii in range(10)]
    bands = [[len([logerror for logerror in bucket if logerror > band[0] and logerror < band[1]]) for bucket in trimmed] for band in bands]
    #plt.plot(range(len(sorted)), ctrimmed, "ro")
    plt.plot(range(len(sorted)), [ float(b)/a for (a, b) in zip(ctrimmed, bands[1])], "bo")
    plt.show()

def plot(bandn):
    x = range(len(sorted))
    y = [1.0/a for a in ctrimmed]
    y1 = [ float(b)/a for (a, b) in zip(ctrimmed, bands[bandn])]
    yy = [ 0.2 if a >= .01 else a for a, b in zip(y, y1)]
    yy1 = [ 0.2 if a >= .01 else b for a, b in zip(y, y1)]

n = [0]

def press(event):
    if event.key == 'x':
        plt.cla()
        my = n[0] % 10
        print(my)
        x = range(len(sorted))
        y = [1.0/a for a in ctrimmed]
        y1 = [ float(b)/a for (a, b) in zip(ctrimmed, bands[my])]
        yy = [ 0.2 if a >= .01 else a for a, b in zip(y, y1)]
        yy1 = [ 0.2 if a >= .01 else b for a, b in zip(y, y1)]
        ax.plot(x, yy1, "bo")
        ax.plot(x, yy, "ro")
        n[0] = n[0] + 1
        print(n[0])

def temp1():
    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_disconnect(6)
    plt.cla()

plot(2)
ax1 = plt.subplot(2, 1, 1)
plt.cla()
ax1.plot(x, yy1, "bo")
ax1.plot(x, yy, "ro")

plot(5)
ax2 = plt.subplot(2, 1, 2)
plt.cla()
ax2.plot(x, yy1, "ro")
ax2.plot(x, yy, "ro")

plt.show()
plt.cla()
