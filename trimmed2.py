import numpy as np

path = "/Programs/kaggle/zillow/"
path = "/Users/T162880/Documents/Programs/zillow/"
path = "/Users/apple/Documents/Programs/zillow/"
properties_2016 = "properties_2016.csv"
properties_2017 = "properties_2017.csv"
train_2016 = "train_2016_v2.csv"
train_2017 = "train_2017.csv"
sample_submission = "sample_submission.csv"
my_submission = "my_submission.csv"
zillow_columns = """
parcelid,airconditioningtypeid,architecturalstyletypeid,basementsqft,bathroomcnt,bedroomcnt,buildingclasstypeid,buildingqualitytypeid,calculatedbathnbr,decktypeid,finishedfloor1squarefeet,calculatedfinishedsquarefeet,finishedsquarefeet12,finishedsquarefeet13,finishedsquarefeet15,finishedsquarefeet50,finishedsquarefeet6,fips,fireplacecnt,fullbathcnt,garagecarcnt,garagetotalsqft,hashottuborspa,heatingorsystemtypeid,latitude,longitude,lotsizesquarefeet,poolcnt,poolsizesum,pooltypeid10,pooltypeid2,pooltypeid7,propertycountylandusecode,propertylandusetypeid,propertyzoningdesc,rawcensustractandblock,regionidcity,regionidcounty,regionidneighborhood,regionidzip,roomcnt,storytypeid,threequarterbathnbr,typeconstructiontypeid,unitcnt,yardbuildingsqft17,yardbuildingsqft26,yearbuilt,numberofstories,fireplaceflag,structuretaxvaluedollarcnt,taxvaluedollarcnt,assessmentyear,landtaxvaluedollarcnt,taxamount,taxdelinquencyflag,taxdelinquencyyear,censustractandblock
"""
columns = zillow_columns.strip().split(sep=",")
zcolumns = { value: index for (index, value) in enumerate(columns) }

def load_train():
    with open(path+train_2016) as fd:
        lines = [ line.strip().split(",") for line in fd.readlines()[1:]]
    train_error = { values[0]: float(values[1]) for values in lines }
    train_data = {}
    with open(path+properties_2016) as fd:
        header = fd.readline()
        while True:
            line = fd.readline()
            if not line: break
            values = line.strip().split(",")
            parcelid = values[0]
            if parcelid not in train_error: continue
            train_data[parcelid] = values
    return train_error, train_data

train_error, train_data = load_train()
trimmed_set = set([ parcelid for parcelid in train_error if abs(train_error[parcelid]-.1) < .5 ])
trimmed_set_mean = np.mean([ train_error[parcelid] for parcelid in trimmed_set ])

def f7(value): return float("{:.7f}".format(value))

def bucketing(cat_func, delta):
    buckets = {}
    for parcelid in trimmed_set:
        index = cat_func(parcelid)
        if index not in buckets:
            buckets[index] = set()
        buckets[index].add(parcelid)
    result = [(key, value) for (key, value) in buckets.items()]
    result.sort(key=lambda item: item[0])
    result2 = []
    for item in result:
        error2 = [ delta[parcelid] for parcelid in item[1] ]
        mean2 = np.mean(error2)
        std2 = np.std(error2)
        info = (item[0], len(error2), f7(mean2), f7(std2))
        info = (item[0], int(mean2*10000), len(error2), f7(mean2), f7(std2))
        result2.append(info)
    result2.sort(key=lambda item: item[2], reverse=True)
    for item in result2:
        print(item)

delta_0 = train_error

def f_0(values):
    return trimmed_set_mean

delta_1 = { parcelid: delta_0[parcelid] - f_0(train_data[parcelid]) for parcelid in trimmed_set }

def cat_year_1(parcelid):
    try:
        year = int(train_data[parcelid][zcolumns["yearbuilt"]].split(".")[0])
    except:
        return "noyear"
    if year < 1900: return "before 1900"
    for i in range(65):
        if year < 1900 + (i+1) * 5:
            return "{}-{}".format(1900+i*5, 1900+(i+1)*5)
    return "noyear"

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

def cat_county(parcelid):
    try:
        county = train_data[parcelid][zcolumns["regionidcounty"]]
    except:
        return "0: no county"
    return county

def cat_city(parcelid):
    try:
        city = train_data[parcelid][zcolumns["regionidcity"]]
    except:
        return "0: no city"
    return city

def explore():
    bucketing(cat_city, delta_4)

def feature(field):
    category = {}
    for parcelid in trimmed_set:
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
        #assign[item[0]] = item[1]
        print("{}: {}, {:.4f}, {:.4f}".format(item[0], *(item[1])))

def delta_1_bucketing(values):
    try:
        year = int(values[zcolumns["yearbuilt"]].split(".")[0])
    except:
        return "zero"
    if year >= 1920 and year < 1930: return "1920-1930"
    if year >= 1935 and year < 1960: return "1935-1960"
    if year >= 1960 and year < 1965: return "1960-1965"
    if year >= 1990 and year < 2010: return "1990-2010"
    if year >= 2010 and year < 2015: return "2010-2015"
    return "zero"

def delta_2_bucketing(values):
    try:
        sqft = int(float(values[zcolumns["calculatedfinishedsquarefeet"]]))
    except:
        return "zero"
    if sqft >= 500 and sqft < 1000: return "500-1000"
    if sqft >= 1000 and sqft < 1500: return "1000-1500"
    if sqft >= 2500 and sqft < 3000: return "2500-3000"
    if sqft >= 3000 and sqft < 4500: return "3000-4500"
    if sqft >= 4500 and sqft < 7000: return "4500-7000"
    return "zero"

def delta_3_bucketing(values):
    try:
        city = train_data[parcelid][zcolumns["regionidcity"]]
    except:
        return "zero"
    if city in [
            "46298",
            "52650",
            "54311",
            "5534",
            "40227",
            "25218",
            "34278",
            "12773",
            "47019",
            "47568",
            "45457",
            "24812",
            "33252",
            "34543",
            "51239",
            "54722",
            "25459",
            "24832",
            "32380",
            "13693",
            "37086",
            "33612",
            "20008",
            "396054",
            "12292",
            "14542",
            "38032",
            "14634",
            "53636",
            "24174",
            "24245",
            "24384",
            "50749",
            "26964",
            "4406",
            "10608",
            "11626",
            "54053",
            "5465",
            "46098",
            "33840",
            "34780",
            "44833",
            "25458",
            "48424",
            "37015",
            "17686",
            "51617",
            "50677",
            "10723",
            "32923",
            "19177",
            "45602",
            "6021",
            "30908",
            "41673",
            "10241",
            "10774",
            "42150",
            "45888",
            "118225",
            "22827",
            "9840",
            "44116",
            "51861",
            "52842",
            "17597",
            "26483",
            "39308",
            "10734",
            "37688",
            "33837",
            "17882",
            "47762",
            "45398",
            "40081",
            "14111",
            "25953",
            "12520",
            "10389",
            "46080",
            "54212",
            "13091",
            "40009",
            "53655",
            "42967",
            "118878",
            "29712",
            "6395",
            "396053",
            "55753",
            "396551",
            "53027",
            "27183",
            "32616",
            "46314",
            "27103",
            "39306",
            "26965",
            "33311",
            "396556",
            "54352",
            "54299",
            "39076",
            "47695",
            "118895",
            "33727",
            "46178",
            "29189",
            "118914",
            "47547",
            "18098",
            "15237",
            "118694",
            "118994",
            "13716",
            "16677",
            "113576",
            "30267",
            "396550",
            "116042",
            "40110",
            "54970",
            "118217",
            "18875",
            "56780",
            "114828",
            "21778",
            "30399",
            "36502",
            "113412",
            "118875",
            "16961",
            "16389",
            "272578",
                 ]:
        return city
    return "zero"

def delta_buckets(delta, delta_bucketing):
    buckets = {}
    for parcelid in trimmed_set:
        values = train_data[parcelid]
        bucket = delta_bucketing(values)
        if bucket not in buckets:
            buckets[bucket] = set()
        buckets[bucket].add(parcelid)
    bucket_means = {}
    for bucket, items in buckets.items():
        if bucket == "zero":
            mean = 0.0
        else:
            mean = np.mean([delta[parcelid] for parcelid in items])
        bucket_means[bucket] = mean
    return bucket_means

delta_1_bucket_means = delta_buckets(delta_1, delta_1_bucketing)
delta_2_bucket_means = delta_buckets(delta_2, delta_2_bucketing)
delta_3_bucket_means = delta_buckets(delta_3, delta_3_bucketing)

def f_1(values):
    return delta_1_bucket_means[delta_1_bucketing(values)]

delta_2 = { parcelid: delta_1[parcelid] - f_1(train_data[parcelid]) for parcelid in trimmed_set }

def f_2(values):
    return delta_2_bucket_means[delta_2_bucketing(values)]

delta_3 = { parcelid: delta_2[parcelid] - f_2(train_data[parcelid]) for parcelid in trimmed_set }

def f_3(values):
    return delta_3_bucket_means[delta_3_bucketing(values)]

delta_4 = { parcelid: delta_3[parcelid] - f_3(train_data[parcelid]) for parcelid in trimmed_set }


def f(values):
    #return f_0(values)
    return f_0(values) + f_1(values) + f_2(values) + f_3(values)

def submit():
    with open(path+properties_2016) as fd, open(path+my_submission, "w") as fdw:
        fd.readline()
        fdw.write("ParcelId,201610,201611,201612,201710,201711,201712\n")
        while True:
            line = fd.readline()
            if not line: break
            values = line.strip().split(",")
            parcelid = values[zcolumns["parcelid"]]
            logerror = f(values)
            e = "{:.4f}".format(logerror)
            fdw.write("{p},{e},{e},{e},{e},{e},{e}\n".format(p=parcelid, e=e))

submit()
