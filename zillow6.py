dir = "/Users/T162880/Documents/Programs/zillow/"
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
    return int(sqft / 500)

def cat_year(value):
    try:
        year = int(value.split(".")[0])
    except:
        return 0
    if year <= 1920: return 1
    return int((year - 1920)/20) + 2

def cat_dollar(value):
    try:
        dollar = int(float(value))
    except:
        return 0
    return int(dollar/200000)

features = [
          ["yearbuilt", cat_year, ],
          ["calculatedfinishedsquarefeet", cat_sqft, ],
          ["taxvaluedollarcnt", cat_dollar, ],
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
        if index not in bdict: bdict[index] = ([], [], [])
        bdict[index][0].append(parcelid)
        if parcelid not in tdict: continue
        bdict[index][1].append(parcelid)
        bdict[index][2].append(tdict[parcelid])
    return bdict

def score(ctest, ctrain, tratio, tpoint, tdist):
    dratio = abs(tratio-33) if tratio != 33 else 1
    return int(ctrain * tdist / dratio)

def bucket_info(bdict):
    info = []
    for item in bdict.values():
        ctest = len(item[0])
        ctrain = len(item[1])
        if ctrain == 0: continue
        tratio = int(ctest/ctrain)
        tmean = sum(item[2])/ctrain
        tpoint = int(tmean*10000)
        tdist = int(abs(tmean-.0115)*10000)
        info.append((ctest, ctrain, tratio, tpoint, tdist))
    return info

if __name__ == "__main__":
    bdict = bucket()
    info = bucket_info(bdict)
    #for item in info: print(item)
    #myinfo.sort(key=lambda item: item[0], reverse=True)
    #for item in myinfo[:30]: print(item, score(*item))
    #print(list(myinfo[0]).append(5))
    score_info = [ tuple(list(item)+[score(*item)]) for item in myinfo]
    score_info.sort(key=lambda item: item[5], reverse=True)
    for item in score_info[:30]: print(item)
    #print(sum([item[0] for item in myinfo[:40]]))
    #print(sum([item[1] for item in myinfo[:40]]))
    #myinfo = [ item for item in myinfo if item[0] > 1000]
    #plt.hist([ v[0] for v in myinfo], bins=40)
    #plt.hist([ v[1] for v in myinfo if v[1] < 100], bins=20)
    #plt.hist([ v[2] for v in myinfo if v[2] < 200], bins=20)
    #plt.hist([ v[3] for v in myinfo if v[3] > -10000 and v[3] < 10000], bins=20)
    #plt.hist([ v[4] for v in myinfo if v[4] < 10000], bins=20)
    #plt.show()
