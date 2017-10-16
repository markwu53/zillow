import numpy as np
import random
import time

path = "/Users/T162880/Documents/Programs/zillow/"
path = "/Users/apple/Documents/Programs/zillow/"
path = "/Programs/kaggle/zillow/"
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
cv_count = 18000
push_factor = 0.03

def myint(value_str):
    try:
        value = int(float(value_str))
    except:
        return 0
    return value

def convert_bathroom(value_str):
    try:
        value = int(float(value_str)*2)
    except:
        return 0
    return value

features = [
    ["yearbuilt", myint, list(range(1900, 2019)), ],
    ["calculatedfinishedsquarefeet", myint, list(range(300, 6000, 100)) + list(range(6000, 10000, 200)) + list(range(10000, 20000, 500))],
    ["bedroomcnt", myint, list(range(1, 15)), ],
    ["bathroomcnt", convert_bathroom, list(range(1, 10)), ],
    ["lotsizesquarefeet", myint, list(range(1000, 4000, 1000)) + list(range(4000, 10000, 200)) + list(range(10000, 100000, 500))],
    ["taxvaluedollarcnt", myint, list(range(50000, 600000, 10000)) + list(range(600000, 1200000, 20000)) + list(range(1200000, 2000000, 50000)) + list(range(2000000, 10000000, 1000000))],
    ["taxamount", myint, list(range(500, 10000, 100)) + list(range(10000, 20000, 200)) + list(range(20000, 50000, 1000))],
    ["landtaxvaluedollarcnt", myint, list(range(50000, 600000, 10000)) + list(range(600000, 1200000, 20000)) + list(range(1200000, 2000000, 50000)) + list(range(2000000, 10000000, 1000000))],
    #"regionidcity",
    #"regionidzip",
    #"latitude",
    #"longitude",
]

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

def train_cv_split():
    rset = set()
    while len(rset) < cv_count:
        rset.add(random.randrange(len(trimmed_list)))
    cv_set = set([trimmed_list[i] for i in rset])
    train_set = set([parcelid for parcelid in train_error if abs(train_error[parcelid] - .1) < .5]) - cv_set
    return train_set, cv_set

def find_best_splitting_feature(residual):
    residual_mean = np.mean(list(residual.values()))
    feature_search_result = []
    for feature_name, convert, feature_step in features:
        buckets = [set() for point in feature_step]
        for parcelid in train_set:
            for index, point in enumerate(feature_step):
                feature_value = train_data[parcelid][zcolumns[feature_name]]
                if convert(feature_value) < point:
                    buckets[index].add(parcelid)
                    break
        buckets_info = [np.sum([residual[parcelid]-residual_mean for parcelid in bucket]) for bucket in buckets]
        buckets_info = [ np.sum(buckets_info[:i+1]) for i in range(len(buckets_info)) ]
        argmax = np.argmax(np.abs(buckets_info))
        feature_search_result.append((feature_name, buckets_info[argmax], argmax, len(feature_step), feature_step[argmax]))
    gains = [ abs(item[1]) for item in feature_search_result ]
    selected_feature_index = np.argmax(gains)
    splitting_index = feature_search_result[selected_feature_index][2]
    feature_search_result.sort(key=lambda item: abs(item[1]), reverse=True)
    for item in feature_search_result: print(item)
    return selected_feature_index, splitting_index

def logMessage(message):
    print("[{}] {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))

def train():
    residual = { parcelid: train_error[parcelid] for parcelid in train_set }
    sme = np.sum(np.square(list(residual.values())))
    print(sme)
    iteration = 0
    while True:
        iteration += 1
        logMessage("doing {}".format(iteration))
        selected_feature_index, splitting_index = find_best_splitting_feature(residual)
        left_set = set()
        for parcelid in train_set:
            feature = features[selected_feature_index]
            feature_value = feature[1](train_data[parcelid][zcolumns[feature[0]]])
            splitting_point = feature[2][splitting_index]
            if feature_value < splitting_point:
                left_set.add(parcelid)
        right_set = train_set - left_set
        left_mean = np.mean([residual[parcelid] for parcelid in left_set])
        right_mean = np.mean([residual[parcelid] for parcelid in right_set])
        approx_functions.append((selected_feature_index, splitting_index, left_mean, right_mean))
        for parcelid in residual:
            target = left_mean if parcelid in left_set else right_mean
            residual[parcelid] = residual[parcelid] - push_factor * target
        sme = np.sum(np.square(list(residual.values())))
        print(sme)

train_error, train_data = load_train()
trimmed_list = list(set([parcelid for parcelid in train_error if abs(train_error[parcelid] - .1) < .5]))
train_set, cv_set = train_cv_split()
approx_functions = []
train()
