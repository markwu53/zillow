import xgboost as xgb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


path = "/Programs/kaggle/zillow/"
path = "/Users/apple/Documents/Programs/zillow/"
path = "/home/T162880/Programs/zillow/"
path = "/Users/T162880/Documents/Programs/zillow/"
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

def myint(value_str):
    try:
        value = int(float(value_str))
    except:
        return -1
    return value

def convert_bathroom(value_str):
    try:
        value = int(float(value_str)*2)
    except:
        return 0
    return value

features = [
    ["yearbuilt", myint, ],
    ["calculatedfinishedsquarefeet", myint, ],
    ["bedroomcnt", myint, ],
    ["bathroomcnt", convert_bathroom, ],
    ["lotsizesquarefeet", myint, ],
    ["taxvaluedollarcnt", myint, ],
    ["taxamount", myint, ],
    ["landtaxvaluedollarcnt", myint, ],
    #"regionidcity",
    ["regionidzip", myint, ],
    ["latitude", myint, ],
    ["longitude", myint, ],
]

with open(path+train_2016) as fd:
    lines = fd.readlines()[1:]
    lines = [ line.strip().split(",") for line in lines ]
    train_errors = { values[0]: float(values[1]) for values in lines }
train_data = []
train_labels = []
with open(path+properties_2016) as fd:
    fd.readline()
    while True:
        line = fd.readline()
        if not line: break
        values = line.strip().split(",")
        parcelid = values[0]
        if parcelid in train_errors:
            train_data.append([feature[1](values[zcolumns[feature[0]]]) for feature in features])
            train_labels.append(train_errors[parcelid])

train_split = train_data[:70000]
train_label_split = train_labels[:70000]
test_split = train_data[70000:]
test_label_split = train_labels[70000:]
trimmed_train = []
trimmed_label = []
for index, values in enumerate(train_split):
    """
    if values[0] < 1850: continue
    if values[1] < 100 or values[1] > 100000: continue
    if values[2] < 1 or values[2] > 10: continue
    if values[3] < 1 or values[3] > 10: continue
    if values[4] < 100 or values[4] > 500000: continue
    if values[5] < 1000 or values[5] > 10000000: continue
    """
    trimmed_train.append(values)
    trimmed_label.append(train_label_split[index])

dtrain =xgb.DMatrix(np.array(trimmed_train), label=np.array(trimmed_label))
dtest =xgb.DMatrix(np.array(test_split), label=np.array(test_label_split))

param = {
    "max_depth": 4,
    "eta": .01,
    "silent": 1,
    #"objective": "binary:logistic",
}

# specify validations set to watch performance
watchlist  = [(dtest,'eval'), (dtrain,'train')]
#watchlist  = [(dtrain,'train')]
num_round = 1200
bst = xgb.train(param, dtrain, num_round, watchlist)


# this is prediction
preds = bst.predict(dtest)
labels = dtest.get_label()
a = sum(1 for i in range(len(preds)) if int(preds[i]>0.5)!=labels[i])
x = [ i for i in range(len(preds)) if int(preds[i]>0.5)==labels[i]]
print ('error=%f' % ( sum(1 for i in range(len(preds)) if int(preds[i]>0.5)!=labels[i]) /float(len(preds))))
bst.save_model('0001.model')
# dump model
bst.dump_model('dump.raw.txt')
# dump model with feature map
#bst.dump_model('dump.nice.txt','featmap.txt')

# save dmatrix into binary buffer
dtest.save_binary('dtest.buffer')
# save model
bst.save_model('xgb.model')
# load model and data in
bst2 = xgb.Booster(model_file='xgb.model')
dtest2 = xgb.DMatrix('dtest.buffer')
preds2 = bst2.predict(dtest2)
# assert they are the same
assert np.sum(np.abs(preds2-preds)) == 0

# alternatively, you can pickle the booster
pks = pickle.dumps(bst2)
# load model and data in
bst3 = pickle.loads(pks)
preds3 = bst3.predict(dtest2)
# assert they are the same
assert np.sum(np.abs(preds3-preds)) == 0

###
# build dmatrix from scipy.sparse
print ('start running example of build DMatrix from scipy.sparse CSR Matrix')
labels = []
row = []; col = []; dat = []
i = 0
for l in open(train_file):
    arr = l.split()
    labels.append(int(arr[0]))
    for it in arr[1:]:
        k,v = it.split(':')
        row.append(i); col.append(int(k)); dat.append(float(v))
    i += 1
csr = scipy.sparse.csr_matrix((dat, (row,col)))
dtrain = xgb.DMatrix(csr, label = labels)
watchlist  = [(dtest,'eval'), (dtrain,'train')]
bst = xgb.train(param, dtrain, num_round, watchlist)

print ('start running example of build DMatrix from scipy.sparse CSC Matrix')
# we can also construct from csc matrix
csc = scipy.sparse.csc_matrix((dat, (row,col)))
dtrain = xgb.DMatrix(csc, label=labels)
watchlist  = [(dtest,'eval'), (dtrain,'train')]
bst = xgb.train(param, dtrain, num_round, watchlist)

print ('start running example of build DMatrix from numpy array')
# NOTE: npymat is numpy array, we will convert it into scipy.sparse.csr_matrix in internal implementation
# then convert to DMatrix
npymat = csr.todense()
dtrain = xgb.DMatrix(npymat, label = labels)
watchlist  = [(dtest,'eval'), (dtrain,'train')]
bst = xgb.train(param, dtrain, num_round, watchlist)

