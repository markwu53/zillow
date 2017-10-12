import numpy as np

path = "/Users/apple/Documents/Programs/zillow/"

properties_2016 = "properties_2016.csv"
properties_2017 = "properties_2017.csv"
train_2016 = "train_2016_v2.csv"
train_2017 = "train_2017.csv"
sample_submission = "sample_submission.csv"
my_submission = "my_submission.csv"
zillow_columns = """
parcelid
airconditioningtypeid
architecturalstyletypeid
basementsqft
bathroomcnt
bedroomcnt
buildingclasstypeid
buildingqualitytypeid
calculatedbathnbr
decktypeid
finishedfloor1squarefeet
calculatedfinishedsquarefeet
finishedsquarefeet12
finishedsquarefeet13
finishedsquarefeet15
finishedsquarefeet50
finishedsquarefeet6
fips
fireplacecnt
fullbathcnt
garagecarcnt
garagetotalsqft
hashottuborspa
heatingorsystemtypeid
latitude
longitude
lotsizesquarefeet
poolcnt
poolsizesum
pooltypeid10
pooltypeid2
pooltypeid7
propertycountylandusecode
propertylandusetypeid
propertyzoningdesc
rawcensustractandblock
regionidcity
regionidcounty
regionidneighborhood
regionidzip
roomcnt
storytypeid
threequarterbathnbr
typeconstructiontypeid
unitcnt
yardbuildingsqft17
yardbuildingsqft26
yearbuilt
numberofstories
fireplaceflag
structuretaxvaluedollarcnt
taxvaluedollarcnt
assessmentyear
landtaxvaluedollarcnt
taxamount
taxdelinquencyflag
taxdelinquencyyear
censustractandblock
"""
my_zillow_columns = """
parcelid,logerror,airconditioningtypeid,architecturalstyletypeid,basementsqft,bathroomcnt,bedroomcnt,buildingclasstypeid,buildingqualitytypeid,calculatedbathnbr,decktypeid,finishedfloor1squarefeet,calculatedfinishedsquarefeet,finishedsquarefeet12,finishedsquarefeet13,finishedsquarefeet15,finishedsquarefeet50,finishedsquarefeet6,fips,fireplacecnt,fullbathcnt,garagecarcnt,garagetotalsqft,hashottuborspa,heatingorsystemtypeid,latitude,longitude,lotsizesquarefeet,poolcnt,poolsizesum,pooltypeid10,pooltypeid2,pooltypeid7,propertycountylandusecode,propertylandusetypeid,propertyzoningdesc,rawcensustractandblock,regionidcity,regionidcounty,regionidneighborhood,regionidzip,roomcnt,storytypeid,threequarterbathnbr,typeconstructiontypeid,unitcnt,yardbuildingsqft17,yardbuildingsqft26,yearbuilt,numberofstories,fireplaceflag,structuretaxvaluedollarcnt,taxvaluedollarcnt,assessmentyear,landtaxvaluedollarcnt,taxamount,taxdelinquencyflag,taxdelinquencyyear,censustractandblock
"""
columns = my_zillow_columns.strip().split(sep=",")
zcolumns = { value: index for (index, value) in enumerate(columns) }

from partition_tree import train_set, train_error, train_data

trimmed_train_set = set([ parcelid for parcelid in train_set if abs(train_error[parcelid]) < 0.2 ])

def do(field):
    for parcelid in trimmed_train_set:
        values = train_data[parcelid]
        value = values[zcolumns[field]]
        if value not in category:
            category[value] = set()
        category[value].add(parcelid)
    print(len(category))
    if len(category) > 500:
        return
    result = []
    for key, item in category.items():
        count = len(item)
        v = [ train_error[parcelid] for parcelid in item ]
        mean = np.mean(v)
        std = np.std(v)
        result.append((key, (count, mean, std)))
    result.sort(key=lambda item: item[1][2])
    for item in result:
        if item[1][0] < 50: continue
        assign[item[0]] = item[1]
        print("{}: {}, {:.4f}, {:.4f}".format(item[0], *(item[1])))

def check(field):
    missing = 0
    with open(path+properties_2016) as fd:
        fd.readline()
        while True:
            line = fd.readline()
            if not line: break
            values = line.strip().split(",")
            values = [ values[0], 0 ] + values[1:]
            value = values[zcolumns[field]]
            if value not in category:
                missing += 1
    print(missing)

category = {}
assign = {}
do("regionidcity")

def zipit():
    import zipfile
    with zipfile.ZipFile(path+my_submission+".zip", "w", compression=zipfile.ZIP_DEFLATED) as fd:
        fd.write(path+my_submission)

def ss():
    with open(path+properties_2016) as fd, open(path+my_submission, "w") as fdw:
        fd.readline()
        fdw.write("ParcelId,201610,201611,201612,201710,201711,201712\n")
        while True:
            line = fd.readline()
            if not line: break
            values = line.strip().split(",")
            values = [ values[0], "" ] + values[1:]
            parcelid = values[zcolumns["parcelid"]]
            value = values[zcolumns["regionidcity"]]
            if value not in assign:
                logerror = 0.0115
            else:
                count, logerror, std = assign[value]
                factor = 1.0 - std * 15
                #factor = 1.0 - std
                #factor = 1.0
                logerror = 0.0115 + factor * (logerror - 0.0115)
            e = "{:.4f}".format(logerror)
            fdw.write("{p},{e},{e},{e},{e},{e},{e}\n".format(p=parcelid, e=e))

