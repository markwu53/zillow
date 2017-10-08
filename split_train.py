import random

dir = "/Users/T162880/Documents/Programs/zillow/"
dir = "/Programs/kaggle/zillow/"
dir = "/Users/apple/Documents/Programs/zillow/"
properties_2016 = "properties_2016.csv"
properties_2017 = "properties_2017.csv"
train_2016 = "train_2016_v2.csv"
train_2017 = "train_2017.csv"
sample_submission = "sample_submission.csv"
my_submission = "my_submission.csv"
my_train = "my_train.csv"
my_test = "my_test.csv"
zillow_columns = """
parcelid,airconditioningtypeid,architecturalstyletypeid,basementsqft,bathroomcnt,bedroomcnt,buildingclasstypeid,buildingqualitytypeid,calculatedbathnbr,decktypeid,finishedfloor1squarefeet,calculatedfinishedsquarefeet,finishedsquarefeet12,finishedsquarefeet13,finishedsquarefeet15,finishedsquarefeet50,finishedsquarefeet6,fips,fireplacecnt,fullbathcnt,garagecarcnt,garagetotalsqft,hashottuborspa,heatingorsystemtypeid,latitude,longitude,lotsizesquarefeet,poolcnt,poolsizesum,pooltypeid10,pooltypeid2,pooltypeid7,propertycountylandusecode,propertylandusetypeid,propertyzoningdesc,rawcensustractandblock,regionidcity,regionidcounty,regionidneighborhood,regionidzip,roomcnt,storytypeid,threequarterbathnbr,typeconstructiontypeid,unitcnt,yardbuildingsqft17,yardbuildingsqft26,yearbuilt,numberofstories,fireplaceflag,structuretaxvaluedollarcnt,taxvaluedollarcnt,assessmentyear,landtaxvaluedollarcnt,taxamount,taxdelinquencyflag,taxdelinquencyyear,censustractandblock
"""
my_zillow_columns = """
parcelid,logerror,airconditioningtypeid,architecturalstyletypeid,basementsqft,bathroomcnt,bedroomcnt,buildingclasstypeid,buildingqualitytypeid,calculatedbathnbr,decktypeid,finishedfloor1squarefeet,calculatedfinishedsquarefeet,finishedsquarefeet12,finishedsquarefeet13,finishedsquarefeet15,finishedsquarefeet50,finishedsquarefeet6,fips,fireplacecnt,fullbathcnt,garagecarcnt,garagetotalsqft,hashottuborspa,heatingorsystemtypeid,latitude,longitude,lotsizesquarefeet,poolcnt,poolsizesum,pooltypeid10,pooltypeid2,pooltypeid7,propertycountylandusecode,propertylandusetypeid,propertyzoningdesc,rawcensustractandblock,regionidcity,regionidcounty,regionidneighborhood,regionidzip,roomcnt,storytypeid,threequarterbathnbr,typeconstructiontypeid,unitcnt,yardbuildingsqft17,yardbuildingsqft26,yearbuilt,numberofstories,fireplaceflag,structuretaxvaluedollarcnt,taxvaluedollarcnt,assessmentyear,landtaxvaluedollarcnt,taxamount,taxdelinquencyflag,taxdelinquencyyear,censustractandblock
"""

train_count = 90275
test_count = 10000

def test_split():
    with open(dir+train_2016) as fd:
        train_data = [ line.strip().split(",") for line in fd.readlines()[1:]]
    for _ in range(20):
        rset = set()
        while len(rset) < test_count: rset.add(random.randrange(train_count))
        mean = sum([float(train_data[i][1]) for i in rset]) / 10000
        print("{:.4f}".format(mean))

def split_data():
    rset = set()
    while len(rset) < test_count:
        rset.add(random.randrange(train_count))

    with open(dir+train_2016) as fd:
        lines = [ line.strip().split(",") for line in fd.readlines()[1:]]
        dict_train = { values[0]: values[1] for index, values in enumerate(lines) if index not in rset }
        dict_test = { values[0]: values[1] for index, values in enumerate(lines) if index in rset }
    print(len(dict_train))
    with open(dir+properties_2016) as fdr, open(dir+my_train, "w") as fdw1, open(dir+my_test, "w") as fdw2:
        fdr.readline()
        fdw1.write("{}\n".format(my_zillow_columns.strip()))
        fdw2.write("{}\n".format(my_zillow_columns.strip()))
        while True:
            line = fdr.readline()
            if not line: break
            values = line.strip().split(",")
            parcelid = values[0]
            if parcelid in dict_train:
                fdw1.write("{}\n".format(",".join([parcelid]+[dict_train[parcelid]]+values[1:])))
            if parcelid in dict_test:
                fdw2.write("{}\n".format(",".join([parcelid]+[dict_test[parcelid]]+values[1:])))

if __name__ == "__main__":
    #split_data()
    test_split()
    print("done")
