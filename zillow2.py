#properties_file = "/Users/apple/Documents/zillow/data/properties_2016.csv"
#train_file = "/Users/apple/Documents/zillow/data/train_2016_v2.csv"
#my_submission_file = "/Users/apple/Documents/zillow/zillow_submission/my_submission.csv"
properties_file = "/Users/T162880/Documents/Programs/zillow/properties_2016.csv"
train_file = "/Users/T162880/Documents/Programs/zillow/train_2016_v2.csv"
my_submission_file = "/Users/T162880/Documents/Programs/zillow/my_submission.csv"
zillow_columns = """
parcelid,airconditioningtypeid,architecturalstyletypeid,basementsqft,bathroomcnt,bedroomcnt,buildingclasstypeid,buildingqualitytypeid,calculatedbathnbr,decktypeid,finishedfloor1squarefeet,calculatedfinishedsquarefeet,finishedsquarefeet12,finishedsquarefeet13,finishedsquarefeet15,finishedsquarefeet50,finishedsquarefeet6,fips,fireplacecnt,fullbathcnt,garagecarcnt,garagetotalsqft,hashottuborspa,heatingorsystemtypeid,latitude,longitude,lotsizesquarefeet,poolcnt,poolsizesum,pooltypeid10,pooltypeid2,pooltypeid7,propertycountylandusecode,propertylandusetypeid,propertyzoningdesc,rawcensustractandblock,regionidcity,regionidcounty,regionidneighborhood,regionidzip,roomcnt,storytypeid,threequarterbathnbr,typeconstructiontypeid,unitcnt,yardbuildingsqft17,yardbuildingsqft26,yearbuilt,numberofstories,fireplaceflag,structuretaxvaluedollarcnt,taxvaluedollarcnt,assessmentyear,landtaxvaluedollarcnt,taxamount,taxdelinquencyflag,taxdelinquencyyear,censustractandblock
"""

def zillowcolumns():
    columns = zillow_columns.strip().split(sep=",")
    return dict([(value, index) for (index, value) in enumerate(columns)])

zcolumns = zillowcolumns()

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

def train_dict():
    with open(train_file) as fd: lines = fd.readlines()[1:]
    lines = [ line.strip().split(",") for line in lines if len(line.strip()) != 0 ]
    tdict = { values[0]: float(values[1]) for values in lines }
    return tdict

features = [
          ["yearbuilt", cat_year, ],
          ["calculatedfinishedsquarefeet", cat_sqrt, ],
]

def bucket_mean():
    bset = dict()
    tdict = train_dict()
    with open(properties_file) as fd: lines = fd.readlines()[1:]
    for line in lines:
        line = line.strip()
        if len(line) == 0: continue
        values = line.split(",")
        parcelid = values[zcolumns["parcelid"]]
        if parcelid not in tdict: continue
        index = tuple([feature[1](values[zcolumns[feature[0]]]) for feature in features])
        if index not in bset: bset[index] = list()
        bset[index].append(tdict[parcelid])
    bmean = { index: "0.0115" if len(elist) < 20
             else "{:.4f}".format(sum(elist)/float(len(elist)))
             for index, elist in bset.items() }
    return bmean

def bucket():
    bmean = bucket_mean()
    print(bmean)
    with open(properties_file) as fd, open(my_submission_file, "w") as fdw:
        fdw.write("ParcelId,201610,201611,201612,201710,201711,201712\n")
        header = fd.readline()
        ln = 0
        while True:
            line = fd.readline()
            ln = ln + 1
            if ln % 100000 == 0: print(ln)
            if not line: break
            line = line.strip()
            if len(line) == 0: continue
            values = line.split(",")
            parcelid = values[zcolumns["parcelid"]]
            bucket_index = tuple([ feature[1](values[zcolumns[feature[0]]]) for feature in features ])
            logerror = bmean[bucket_index] if bucket_index in bmean else "0.0115"
            fdw.write("{p},{a},{a},{a},{a},{a},{a}\n".format(p=parcelid, a=logerror))

if __name__ == "__main__":
    bucket()
    print("done")
