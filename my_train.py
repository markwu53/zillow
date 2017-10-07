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

def train_1():
    """
    set train data mean error as test error
    L1 score: 6639220
    """
    with open(dir+my_train) as fd:
        lines = [ line.strip().split(",") for line in fd.readlines()[1:]]
        errors = [ float(values[zcolumns["logerror"]]) for values in lines ]
        mean_error = sum(errors) / len(errors)
    print(mean_error)
    with open(dir+my_test) as fd:
        lines = [ line.strip().split(",") for line in fd.readlines()[1:]]
        errors = [ float(values[zcolumns["logerror"]]) for values in lines ]
        total_error = sum([abs(error-mean_error) for error in errors])
    print(total_error)
    score = int(float("{:.4f}".format(total_error)) * 10000)
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
    for p in range(len(points)):
        if value < points[p]: return p
    return 0

features = [
          ["calculatedfinishedsquarefeet", cat_sqft, ],
          ["yearbuilt", cat_year, ],
          #["longitude", cat_long, ],
          #["latitude", cat_lat, ],
]

if __name__ == "__main__":
    train()
    print("done")
