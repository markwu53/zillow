import random

path = "/Users/T162880/Documents/Programs/zillow/"
path = "/Programs/kaggle/zillow/"
path = "/Users/apple/Documents/Programs/zillow/"
properties_2016 = "properties_2016.csv"
properties_2017 = "properties_2017.csv"
train_2016 = "train_2016_v2.csv"
train_2017 = "train_2017.csv"
sample_submission = "sample_submission.csv"
my_submission = "my_submission.csv"
my_train = "my_train.csv"
my_test = "my_test.csv"
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

test_count = 10000

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

#split train test
def random_test_set():
    rset = set()
    while len(rset) < test_count:
        rset.add(random.randrange(len(train_list)))
    return { train_list[i] for i in rset }

#level 0
train_mean = sum(train_error.values()) / len(train_error)

def assign_test_error(test_set):
    test_error = { parcelid: train_mean for parcelid in test_set }
    return test_error

#level 0 assigns train_mean to test set
#take 100 times score mean
def score_it():
    total_error = 0.0
    for i in range(100):
        test_set = random_test_set()
        test_error = assign_test_error(test_set)
        total_error += sum([abs(test_error[parcelid] - train_error[parcelid]) for parcelid in split_test])
    score = int((total_error / 100) * 10000)
    print(score)

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

levels = [
          #[["calculatedfinishedsquarefeet", cat_sqft, ], ["yearbuilt", cat_year, ],],
          [["yearbuilt", cat_year, ],],
          [["calculatedfinishedsquarefeet", cat_sqft, ]],
          [["longitude", cat_long, ], ["latitude", cat_lat, ],],
          [["longitude", cat_long2, ], ["latitude", cat_lat2, ],],
]

def indexing(values):
    index = tuple([tuple([coord[1](values[zcolumns[coord[0]]]) for coord in level]) for level in levels])
    return index

index_dict = {}
for parcelid in train_data:
    index = indexing(train_data[parcelid])
    if index not in index_dict:
        index_dict[index] = set()
    index_dict[index].add(parcelid)

def train_level_1():
    pass
