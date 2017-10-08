import time
import math

dir = "/Users/T162880/Documents/Programs/zillow/"
dir = "/Programs/kaggle/zillow/"
dir = "/Users/apple/Documents/Programs/zillow/"
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

def zillowcolumns():
    columns = zillow_columns.strip().split(sep=",")
    return dict([(value, index) for (index, value) in enumerate(columns)])

zcolumns = zillowcolumns()

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
    points.sort()
    for p in points:
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
              # add step 3 points
              ]
    points.sort()
    for p in points:
        if value < points[p]: return p
    return 0

features = [
          ["calculatedfinishedsquarefeet", cat_sqft, ],
          ["yearbuilt", cat_year, ],
          ["longitude", cat_long, ],
          ["latitude", cat_lat, ],
]

def logMessage(message):
    print("[{}] {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))

def step0():
    step0_submission = "{}_step_0.csv".format(my_submission.split(sep=".")[0])
    with open(dir + sample_submission) as fd:
        parcelids = [ line.split(",")[0] for line in fd.readlines()[1:]]
    with open(dir + step0_submission, "w") as fd:
        fd.write("ParcelId,201610,201611,201612,201710,201711,201712\n")
        for parcelid in parcelids: fd.write("{p},{e},{e},{e},{e},{e},{e}\n".format(p=parcelid, e="0.0115"))

def drag_factor(ctest, ctrain):
    if ctrain >= 5000:
        cscore = 1.0
    else:
        cscore = 0.5 + int(ctrain / 1000) / 10
    ratio = int(ctest/ctrain)
    if ratio <= 33:
        rscore = 1.0
    else:
        rdist = ratio - 33
        if rdist <= 10:
            rscore = -0.1 * (ratio - 33) + 1.1
        else:
            rscore = 1/rdist
    factor = 0.7 + 0.1 * cscore * rscore
    return factor

def drag_factor(ctest, ctrain):
    #result = 0.9 if ctrain > 100 else 0.5
    result = 0.1
    return result

def drag(berror, ctest, ctrain, terror):
    factor = drag_factor(ctest, ctrain)
    result = berror + factor * (terror - berror)
    return result

def showBucket(bdict):
    keys = [ key for key in bdict.keys()]
    keys.sort()
    for key in keys:
        ctest, ctrain, error = bdict[key]
        print(key, (ctest, ctrain, int(ctest/ctrain), float("{:.4f}".format(drag_factor(ctest, ctrain))), float("{:.4f}".format(error))))

def step():
    base_submission = "{}_step_2.csv".format(my_submission.split(sep=".")[0])
    target_submission = "{}_step_3.csv".format(my_submission.split(sep=".")[0])

    logMessage("begin")
    with open(dir + base_submission) as fd:
        lines = [line.strip().split(",") for line in fd.readlines()[1:]]
        base = { values[0]: float(values[1]) for values in lines }
    with open(dir+train_2016) as fd:
        lines = [line.strip().split(",") for line in fd.readlines()[1:]]
        tdict = { values[0]: float(values[1]) for values in lines }

    logMessage("building bucket info")
    bdict = {}
    with open(dir+properties_2016) as fd:
        header = fd.readline()
        while True:
            line = fd.readline()
            if not line: break
            values = line.strip().split(",")
            parcelid = values[zcolumns["parcelid"]]
            index = tuple([feature[1](values[zcolumns[feature[0]]]) for feature in features])
            if index not in bdict: bdict[index] = (0, 0, 0.0)
            (ctest, ctrain, tsum) = bdict[index]
            ctest = ctest + 1
            if parcelid in tdict:
                ctrain = ctrain + 1
                tsum = tsum + tdict[parcelid]
            bdict[index] = (ctest, ctrain, tsum)
        bdict = { index: (item[0], item[1], item[2]/item[1]) for index, item in bdict.items() if item[1] != 0 }

    showBucket(bdict)

    logMessage("writing step result")
    with open(dir + target_submission, "w") as fdw, open(dir+properties_2016) as fd:
        fdw.write("ParcelId,201610,201611,201612,201710,201711,201712\n")
        header = fd.readline()
        while True:
            line = fd.readline()
            if not line: break
            values = line.strip().split(",")
            parcelid = values[zcolumns["parcelid"]]
            index = tuple([feature[1](values[zcolumns[feature[0]]]) for feature in features])
            berror = base[parcelid]
            error = drag(berror, *(bdict[index])) if index in bdict else berror
            e = "{:.4f}".format(error)
            fdw.write("{p},{e},{e},{e},{e},{e},{e}\n".format(p=parcelid, e=e))

if __name__ == "__main__":
    step()
    logMessage("done")
