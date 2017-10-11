from osenv import path
import numpy as np

properties_2016 = "properties_2016.csv"
properties_2017 = "properties_2017.csv"
train_2016 = "train_2016_v2.csv"
train_2017 = "train_2017.csv"
sample_submission = "sample_submission.csv"
my_submission = "my_submission.csv"
zillow_columns = """
parcelid,airconditioningtypeid,architecturalstyletypeid,basementsqft,bathroomcnt,bedroomcnt,buildingclasstypeid,buildingqualitytypeid,calculatedbathnbr,decktypeid,finishedfloor1squarefeet,calculatedfinishedsquarefeet,finishedsquarefeet12,finishedsquarefeet13,finishedsquarefeet15,finishedsquarefeet50,finishedsquarefeet6,fips,fireplacecnt,fullbathcnt,garagecarcnt,garagetotalsqft,hashottuborspa,heatingorsystemtypeid,latitude,longitude,lotsizesquarefeet,poolcnt,poolsizesum,pooltypeid10,pooltypeid2,pooltypeid7,propertycountylandusecode,propertylandusetypeid,propertyzoningdesc,rawcensustractandblock,regionidcity,regionidcounty,regionidneighborhood,regionidzip,roomcnt,storytypeid,threequarterbathnbr,typeconstructiontypeid,unitcnt,yardbuildingsqft17,yardbuildingsqft26,yearbuilt,numberofstories,fireplaceflag,structuretaxvaluedollarcnt,taxvaluedollarcnt,assessmentyear,landtaxvaluedollarcnt,taxamount,taxdelinquencyflag,taxdelinquencyyear,censustractandblock
"""
my_zillow_columns = """
parcelid,logerror,airconditioningtypeid,architecturalstyletypeid,basementsqft,bathroomcnt,bedroomcnt,buildingclasstypeid,buildingqualitytypeid,calculatedbathnbr,decktypeid,finishedfloor1squarefeet,calculatedfinishedsquarefeet,finishedsquarefeet12,finishedsquarefeet13,finishedsquarefeet15,finishedsquarefeet50,finishedsquarefeet6,fips,fireplacecnt,fullbathcnt,garagecarcnt,garagetotalsqft,hashottuborspa,heatingorsystemtypeid,latitude,longitude,lotsizesquarefeet,poolcnt,poolsizesum,pooltypeid10,pooltypeid2,pooltypeid7,propertycountylandusecode,propertylandusetypeid,propertyzoningdesc,rawcensustractandblock,regionidcity,regionidcounty,regionidneighborhood,regionidzip,roomcnt,storytypeid,threequarterbathnbr,typeconstructiontypeid,unitcnt,yardbuildingsqft17,yardbuildingsqft26,yearbuilt,numberofstories,fireplaceflag,structuretaxvaluedollarcnt,taxvaluedollarcnt,assessmentyear,landtaxvaluedollarcnt,taxamount,taxdelinquencyflag,taxdelinquencyyear,censustractandblock
"""
columns = my_zillow_columns.strip().split(sep=",")
zcolumns = { value: index for (index, value) in enumerate(columns) }

def load_train():
    #join train error with properties
    with open(path+train_2016) as fd:
        lines = [ line.strip().split(",") for line in fd.readlines()[1:]]
    train_error = { values[0]: float(values[1]) for values in lines }
    train_set = train_error.keys()
    train_list = list(train_set)
    train_data = {}
    with open(path+properties_2016) as fd:
        header = fd.readline()
        while True:
            line = fd.readline()
            if not line: break
            values = line.split(",")
            parcelid = values[0]
            if parcelid not in train_error: continue
            train_data[parcelid] = [ parcelid, train_error[parcelid]] + values[1:]
    return train_error, train_set, train_list, train_data

train_error, train_set, train_list, train_data = load_train()
trimmed_set = set([ parcelid for parcelid in train_set if abs(train_error[parcelid]-.1) < .5 ])

def cut(bound):
    errors = [ train_error[parcelid] for parcelid in train_set if abs(train_error[parcelid]-.1) < bound ]
    mean = np.mean(errors)
    std = np.std(errors)
    info = (float("{:.1f}".format(bound)), len(errors), float("{:.7f}".format(mean)), float("{:.7f}".format(std)))
    print(info)

def temp1():
    for i in range(7):
        bound = .7 - i * .1
        cut(bound)

def f7(value):
    return float("{:.7f}".format(value))

def cat_year_1(parcelid):
    try:
        year = int(train_data[parcelid][zcolumns["yearbuilt"]].split(".")[0])
    except:
        return "noyear"
    if year < 1950: return "before 1950"
    for i in range(40):
        if year < 1950 + (i+1) * 2:
            return "{}-{}".format(1950+i*2, 1950+(i+1)*2)
    return "noyear"

def cat_year_2(parcelid):
    try:
        year = int(train_data[parcelid][zcolumns["yearbuilt"]].split(".")[0])
    except:
        return "0: noyear"
    if year < 1950: return "1: before 1950"
    if year < 1970: return "2: 50 and 60"
    if year < 1990: return "3: 70 and 80"
    if year >= 1990: return "4: after 1990"
    return "0: noyear"

def cat_year_3(parcelid):
    try:
        year = int(train_data[parcelid][zcolumns["yearbuilt"]].split(".")[0])
    except:
        return "0: noyear"
    if year < 1958: return "1: before 1958"
    if year < 1966: return "2: 58-66"
    if year < 1974: return "3: 66-74"
    if year < 1984: return "4: 74-84"
    if year < 1990: return "5: 84-90"
    return "6: after 90"

def cat_sqft_1(parcelid):
    try:
        sqft = int(float(train_data[parcelid][zcolumns["calculatedfinishedsquarefeet"]]))
    except:
        return "0: no sqft"
    for i in range(20):
        begin = i * 500
        end = (i+1) * 500
        if sqft < end: return "c{:02d}: {}-{}".format(i+1, begin, end)
    return "big: >10000"

def cat_sqft_2(parcelid):
    try:
        sqft = int(float(train_data[parcelid][zcolumns["calculatedfinishedsquarefeet"]]))
    except:
        return "0: no sqft"
    if sqft < 500: return "small: <500"
    for i in range(40):
        begin = 500 + i * 100
        end = 500 + (i+1) * 100
        if sqft < end: return "c{:02d}: {}-{}".format(i+1, begin, end)
    return "big: >4500"

def bucketing(cat_func):
    buckets = {}
    for parcelid in train_set:
        index = cat_func(parcelid)
        if index not in buckets:
            buckets[index] = set()
        buckets[index].add(parcelid)
    result = [(key, value) for (key, value) in buckets.items()]
    result.sort(key=lambda item: item[0])
    for item in result:
        error1 = [ train_error[parcelid] for parcelid in item[1] ]
        error2 = [ train_error[parcelid] for parcelid in item[1] if parcelid in trimmed_set ]
        mean1 = np.mean(error1)
        mean2 = np.mean(error2)
        std1 = np.std(error1)
        std2 = np.std(error2)
        info = (item[0], len(error1), f7(mean1), f7(std1), len(error2), f7(mean2), f7(std2))
        info = (item[0], len(error2), f7(mean2), f7(std2))
        print(info)

bucketing(cat_sqft_2)

