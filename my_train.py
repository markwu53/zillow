dir = "/Users/T162880/Documents/Programs/zillow/"
dir = "/Programs/kaggle/zillow/"
dir = "/Users/apple/Documents/Programs/zillow/"
my_train = "my_train.csv"
my_test = "my_test.csv"

my_zillow_columns = """
parcelid,logerror,airconditioningtypeid,architecturalstyletypeid,basementsqft,bathroomcnt,bedroomcnt,buildingclasstypeid,buildingqualitytypeid,calculatedbathnbr,decktypeid,finishedfloor1squarefeet,calculatedfinishedsquarefeet,finishedsquarefeet12,finishedsquarefeet13,finishedsquarefeet15,finishedsquarefeet50,finishedsquarefeet6,fips,fireplacecnt,fullbathcnt,garagecarcnt,garagetotalsqft,hashottuborspa,heatingorsystemtypeid,latitude,longitude,lotsizesquarefeet,poolcnt,poolsizesum,pooltypeid10,pooltypeid2,pooltypeid7,propertycountylandusecode,propertylandusetypeid,propertyzoningdesc,rawcensustractandblock,regionidcity,regionidcounty,regionidneighborhood,regionidzip,roomcnt,storytypeid,threequarterbathnbr,typeconstructiontypeid,unitcnt,yardbuildingsqft17,yardbuildingsqft26,yearbuilt,numberofstories,fireplaceflag,structuretaxvaluedollarcnt,taxvaluedollarcnt,assessmentyear,landtaxvaluedollarcnt,taxamount,taxdelinquencyflag,taxdelinquencyyear,censustractandblock
"""
columns = my_zillow_columns.strip().split(sep=",")
zcolumns = { value: index for (index, value) in enumerate(columns) }

def score(result):
    total_error = sum([abs(errors[0]-errors[1]) for errors in result.values()])
    score = int(float("{:.4f}".format(total_error)) * 10000)
    print(score)

def train_0():
    #6618160
    result = { values[0]: [float(values[1]), 0.0] for values in test_data }
    return result

def train_1():
    """
    set train data mean error as test error
    L1 score: 6639220
    """
    train_errors = [ float(values[zcolumns["logerror"]]) for values in train_data ]
    mean_error = sum(train_errors) / len(train_errors)
    result = { values[0]: [float(values[1]), mean_error] for values in test_data }
    return result

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
    points.sort()
    #points = list(range(-119500000, -117500000, 100000))
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
    points.sort()
    #points = list(range(33400000, 34500000, 100000))
    for p in range(len(points)):
        if value < points[p]: return p
    return 0

features_1 = [
          ["calculatedfinishedsquarefeet", cat_sqft, ],
          ["yearbuilt", cat_year, ],
]

features_2 = [
          ["calculatedfinishedsquarefeet", cat_sqft, ],
          ["yearbuilt", cat_year, ],
          ["longitude", cat_long, ],
          ["latitude", cat_lat, ],
]

"""
    factor = 0.9 #6629480
    factor = 0.8 #6627191
    factor = 0.7 #6625595
    factor = 0.6 #6624706
    factor = 0.5 #6624632
    factor = 0.4 #6625623
    factor = 0.3 #6627802
    factor = 0.2 #6630838
    factor = 0.1 #6634646
    factor = 0.0 #6639220
    """
 
def train_2(factor, oresult):
    bdict = {}
    for values in train_data:
        index = tuple([feature[1](values[zcolumns[feature[0]]]) for feature in features])
        if index not in bdict: bdict[index] = (0, 0.0)
        (ctrain, tsum) = bdict[index]
        ctrain += 1
        tsum += float(values[zcolumns["logerror"]])
        bdict[index] = (ctrain, tsum)
    for index in bdict:
        (ctrain, tsum) = bdict[index]
        bdict[index] = (ctrain, tsum/ctrain)

    nresult = { parcelid: [values[0], values[1]] for parcelid, values in oresult.items() }
    for values in test_data:
        parcelid = values[zcolumns["parcelid"]]
        index = tuple([feature[1](values[zcolumns[feature[0]]]) for feature in features])
        if index in bdict:
            old = oresult[parcelid][1]
            new = bdict[index][1]
            nresult[parcelid][1] = old + factor * (new - old)
    return nresult

if __name__ == "__main__":
    with open(dir+my_train) as fd:
        train_data = [ line.strip().split(",") for line in fd.readlines()[1:]]
    with open(dir+my_test) as fd:
        test_data = [ line.strip().split(",") for line in fd.readlines()[1:]]
    result = train_1()
    score(result)
    features = features_1
    result = train_2(0.5, result)
    score(result)
    features = features_2
    tresult = train_2(0.9, result)
    score(tresult)
    tresult = train_2(0.8, result)
    score(tresult)
    tresult = train_2(0.7, result)
    score(tresult)
    tresult = train_2(0.6, result)
    score(tresult)
    tresult = train_2(0.5, result)
    score(tresult)
    tresult = train_2(0.4, result)
    score(tresult)
    tresult = train_2(0.3, result)
    score(tresult)
    tresult = train_2(0.2, result)
    score(tresult)
    tresult = train_2(0.1, result)
    score(tresult)
    tresult = train_2(0.0, result)
    score(tresult)
    print("done")
