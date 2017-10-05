import time
import math

dir = "/Users/T162880/Documents/Programs/zillow/"
dir = "/Programs/kaggle/zillow/"
dir = "/Users/apple/Documents/zillow/data/"
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
        sqft = int(float(value))
    except:
        return 0
    return int(sqft / 200)

def cat_year(value):
    try:
        year = int(value.split(".")[0])
    except:
        return 0
    if year <= 1920: return 1
    return int((year - 1920)/10) + 2

def cat_dollar(value):
    try:
        dollar = int(float(value))
    except:
        return 0
    return int(dollar/50000)

def cat_bath(value):
    try:
        count = int(value)
    except:
        return 0
    if count < 10: return count
    return 10

def cat_bed(value):
    try:
        count = int(value)
    except:
        return 0
    if count < 10: return count
    return 10

def cat_zip(value):
    try:
        zip = int(value)
    except:
        return 0
    result = int(zip / 10)
    return result

def cat_lat(value):
    try:
        n = int(value)
    except:
        return 0
    return int(n / 200000)

def cat_long(value):
    try:
        n = int(value)
    except:
        return 0
    return int(n / 200000)

features = [
          ["yearbuilt", cat_year, ],
          #["calculatedfinishedsquarefeet", cat_sqft, ],
          #["taxvaluedollarcnt", cat_dollar, ],
          #["bathroomcnt", cat_bath, ],
          #["bedroomcnt", cat_bed, ],
          #["regionidzip", cat_zip, ],
          ["latitude", cat_lat, ],
          ["longitude", cat_long, ],
]

def bucket():
    with open(dir+train_2016) as fd: lines = fd.readlines()[1:]
    lines = [ line.strip().split(",") for line in lines if len(line.strip()) != 0 ]
    tdict = { values[0]: float(values[1]) for values in lines }

    bdict = dict()
    with open(dir+properties_2016) as fd: lines = fd.readlines()[1:]
    for line in lines:
        line = line.strip()
        if len(line) == 0: continue
        values = line.split(",")
        parcelid = values[zcolumns["parcelid"]]
        index = tuple([feature[1](values[zcolumns[feature[0]]]) for feature in features])
        if index not in bdict: bdict[index] = { "test_list": [], "train_list": [], "logerrors": [], }
        bdict[index]["test_list"].append(parcelid)
        if parcelid not in tdict: continue
        bdict[index]["train_list"].append(parcelid)
        bdict[index]["logerrors"].append(tdict[parcelid])
    return bdict

def score(ctest, ctrain, tratio, tpoint, tdist):
    dratio = int(abs(tratio-33)/10) + 1
    dist = math.pow(tdist, 1.5) if tdist < 1000 else tdist
    return int(ctrain * dist / dratio)

def bucket_info(bdict):
    for item in bdict.values():
        ctest = len(item["test_list"])
        ctrain = len(item["train_list"])
        if ctrain == 0: continue
        tratio = int(ctest/ctrain)
        tmean = sum(item["logerrors"])/ctrain
        tpoint = int(tmean*10000)
        tdist = int(abs(tmean-.0115)*10000)
        item["info"] = (ctest, ctrain, tratio, tpoint, tdist)
        item["score"] = score(ctest, ctrain, tratio, tpoint, tdist)
        item["train_mean"] = tmean

def selected(bdict):
    print(len(bdict.items()))
    score_list = [(item["score"], index) for index, item in bdict.items() if "score" in item]
    score_list.sort(reverse=True)
    print(len(score_list))
    top = 20
    for item in score_list[:top]: print(item[0], bdict[item[1]]["info"])
    selected = set([ item[1] for item in score_list[:top]])
    ctest = sum([len(bdict[index]["test_list"]) for index in selected])
    ctrain = sum([len(bdict[index]["train_list"]) for index in selected])
    print(ctest, ctrain)
    return selected

def mysubmission(bdict, selected_index):
    with open(dir + my_submission, "w") as fd:
        fd.write("ParcelId,201610,201611,201612,201710,201711,201712\n")
        for index, item in bdict.items():
            logerror = "{:.4f}".format(item["train_mean"]) if index in selected_index else overall_mean
            for parcelid in item["test_list"]:
                fd.write("{p},{a},{a},{a},{a},{a},{a}\n".format(p=parcelid, a=logerror))

def logMessage(message):
    print("[{}] {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))

if __name__ == "__main__":
    logMessage("bucketing")
    bdict = bucket()
    logMessage("select buckets")
    bucket_info(bdict)
    selected_index = selected(bdict)
    #logMessage("writing submission")
    #mysubmission(bdict, selected_index)
    logMessage("done")
    #for item in info: print(item)
    #myinfo.sort(key=lambda item: item[0], reverse=True)
    #for item in myinfo[:30]: print(item, score(*item))
    #print(list(myinfo[0]).append(5))
    #score_info = [ tuple(list(item)+[score(*item)]) for item in myinfo]
    #score_info.sort(key=lambda item: item[5], reverse=True)
    #for item in score_info[:100]: print(item)
    #for item in score_info: print(item)
    #print(sum([item[0] for item in myinfo[:40]]))
    #print(sum([item[1] for item in myinfo[:40]]))
    #myinfo = [ item for item in myinfo if item[0] > 1000]
    #plt.hist([ v[0] for v in myinfo], bins=40)
    #plt.hist([ v[1] for v in myinfo if v[1] < 100], bins=20)
    #plt.hist([ v[2] for v in myinfo if v[2] < 200], bins=20)
    #plt.hist([ v[3] for v in myinfo if v[3] > -10000 and v[3] < 10000], bins=20)
    #plt.hist([ v[4] for v in myinfo if v[4] < 10000], bins=20)
    #plt.show()
