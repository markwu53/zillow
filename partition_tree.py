import random
from osenv import path

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

def train_split(base_count):
    #split train test
    rset = set()
    while len(rset) < base_count:
        rset.add(random.randrange(len(train_list)))
    base_set = { train_list[i] for i in rset }
    test_set = train_set - base_set
    return base_set, test_set

def cat_sqft(value):
    try:
        value = int(float(value))
    except:
        return 0
    if value < 1000: return 1
    if value < 2000: return 2
    if value < 3000: return 3
    if value < 4000: return 4
    return 5

def cat_year(value):
    try:
        value = int(value.split(".")[0])
    except:
        return 0
    if value < 1950: return 1
    if value < 1970: return 2
    if value < 1990: return 3
    if value < 2000: return 4
    return 5

def cat_long(value):
    try:
        value = int(value)
    except:
        return 0
    points = [
              -119500000,
              -119000000,
              -118500000,
              -118000000,
              -117500000,
              ]
    points = list(set(points))
    points.sort()
    for p in range(len(points)):
        if value < points[p]: return p
    return 0

def cat_lat(value):
    try:
        value = int(value)
    except:
        return 0
    points = [
              33400000,
              33730000,
              33900000,
              34160000,
              34500000,
              ]
    points = list(set(points))
    points.sort()
    for p in range(len(points)):
        if value < points[p]: return p
    return 0

def cat_long2(value):
    try:
        value = int(value)
    except:
        return 0
    points = [
              -119500000,
              -119000000,
              # add step 3 points
              -118750000,
              -118500000,
              # add step 3 points
              -118250000,
              -118000000,
              # add step 3 points
              -117750000,
              -117500000,
              ]
    points = list(set(points))
    points.sort()
    for p in range(len(points)):
        if value < points[p]: return p
    return 0

def cat_lat2(value):
    try:
        value = int(value)
    except:
        return 0
    points = [
              33400000,
              33730000,
              33900000,
              34160000,
              34500000,
              ]
    points = list(set(points))
    points.sort()
    for p in range(len(points)):
        if value < points[p]: return p
    return 0

def indexing_data(data):
    index_dict = {}
    for parcelid in data:
        index = []
        for level in levels:
            coords = []
            for coord in level:
                cat_coord = coord[1](train_data[parcelid][zcolumns[coord[0]]])
                coords.append(cat_coord)
            index.append(tuple(coords))
        index = tuple(index)
        if index not in index_dict:
            index_dict[index] = set()
        index_dict[index].add(parcelid)
    return index_dict

def get_level_info(index_dict):
    level_dicts = []
    for n in range(len(levels)):
        level_dict = {}
        for index in index_dict:
            level_index = tuple(index[:n+1])
            if level_index not in level_dict:
                level_dict[level_index] = (0, 0.0)
            count, total = level_dict[level_index]
            for parcelid in index_dict[index]:
                count += 1
                total += train_error[parcelid]
                level_dict[level_index] = (count, total)
        level_dict = { key: (count, total/count) for key, (count, total) in level_dict.items() }
        level_dicts.append(level_dict)
    return level_dicts

levels = [
          #[["calculatedfinishedsquarefeet", cat_sqft, ], ["yearbuilt", cat_year, ],],
          [["longitude", cat_long, ], ["latitude", cat_lat, ],],
          [["calculatedfinishedsquarefeet", cat_sqft, ]],
          [["yearbuilt", cat_year, ],],
          [["longitude", cat_long2, ], ["latitude", cat_lat2, ],],
]

base_count = 45000

def doit():
    base_set, test_set = train_split(base_count)
    base_mean = sum([ train_error[parcelid] for parcelid in base_set ]) / len(base_set)
    index_base_set = indexing_data(base_set)
    index_test_set = indexing_data(test_set)
    base_set_level_info = get_level_info(index_base_set)
    test_set_level_info = get_level_info(index_test_set)
    index0 = list(base_set_level_info[0].keys())
    index0.sort()
    for index in index0:
        if index not in test_set_level_info[0]: continue
        bcount, bmean = base_set_level_info[0][index]
        tcount, tmean = test_set_level_info[0][index]
        print("{}: ({}, {}, {:.4f}, {:.4f}, {:.4f})".format(index, bcount, tcount, base_mean, bmean, tmean))

