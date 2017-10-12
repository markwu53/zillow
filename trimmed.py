from osenv import path
import numpy as np

properties_2016 = "properties_2016.csv"
properties_2017 = "properties_2017.csv"
train_2016 = "train_2016_v2.csv"
train_2017 = "train_2017.csv"
sample_submission = "sample_submission.csv"
my_submission = "my_submission.csv"
zillow_columns = """
parcelid,airconditioningtypeid,architecturalstyletypeid,basementsqft,bathroomcnt,bedroomcnt,buildingclasstypeid,buildingqualitytypeid,calculatedbathnbr,decktypeid,finishedfloor1squarefeet,calculatedfinishedsquarefeet,finishedsquarefeet12,finishedsquarefeet13,finishedsquarefeet15,finishedsquarefeet50,finishedsquarefeet6,fips,fireplacecnt,fullbathcnt,garagecarcnt,garagetotalsqft,hashottuborspa,heatingorsystemtypeid,latitude,longitude,lotsizesquarefeet,poolcnt,poolsizesum,pooltypeid10,pooltypeid2,pooltypeid7,propertycountylandusecode,propertylandusetypeid,propertyzoningdesc,rawcensustractandblock,regionidcity,regionidcounty,regionidneighborhood,regionidzip,roomcnt,storytypeid,threequarterbathnbr,typeconstructiontypeid,unitcnt,yardbuildingsqft17,yardbuildingsqft26,yearbuilt,numberofstories,fireplaceflag,structuretaxvaluedollarcnt,taxvaluedollarcnt,assessmentyear,landtaxvaluedollarcnt,taxamount,taxdelinquencyflag,taxdelinquencyyear,censustractandblock
"""
my_zillow_columns = """
parcelid,logerror,airconditioningtypeid,architecturalstyletypeid,basementsqft,bathroomcnt,bedroomcnt,buildingclasstypeid,buildingqualitytypeid,calculatedbathnbr,decktypeid,finishedfloor1squarefeet,calculatedfinishedsquarefeet,finishedsquarefeet12,finishedsquarefeet13,finishedsquarefeet15,finishedsquarefeet50,finishedsquarefeet6,fips,fireplacecnt,fullbathcnt,garagecarcnt,garagetotalsqft,hashottuborspa,heatingorsystemtypeid,latitude,longitude,lotsizesquarefeet,poolcnt,poolsizesum,pooltypeid10,pooltypeid2,pooltypeid7,propertycountylandusecode,propertylandusetypeid,propertyzoningdesc,rawcensustractandblock,regionidcity,regionidcounty,regionidneighborhood,regionidzip,roomcnt,storytypeid,threequarterbathnbr,typeconstructiontypeid,unitcnt,yardbuildingsqft17,yardbuildingsqft26,yearbuilt,numberofstories,fireplaceflag,structuretaxvaluedollarcnt,taxvaluedollarcnt,assessmentyear,landtaxvaluedollarcnt,taxamount,taxdelinquencyflag,taxdelinquencyyear,censustractandblock
"""
columns = my_zillow_columns.strip().split(sep=",")
zcolumns = { value: index for (index, value) in enumerate(columns) }

def load_train():
    #join train error with properties
    with open(path+train_2016) as fd:
        lines = [ line.strip().split(",") for line in fd.readlines()[1:]]
    train_error = { values[0]: float(values[1]) for values in lines }
    train_set = train_error.keys()
    train_list = list(train_set)
    train_data = {}
    with open(path+properties_2016) as fd:
        header = fd.readline()
        while True:
            line = fd.readline()
            if not line: break
            values = line.split(",")
            parcelid = values[0]
            if parcelid not in train_error: continue
            train_data[parcelid] = [ parcelid, train_error[parcelid]] + values[1:]
    return train_error, train_set, train_list, train_data

train_error, train_set, train_list, train_data = load_train()
trimmed_set = set([ parcelid for parcelid in train_set if abs(train_error[parcelid]-.1) < .5 ])
trimmed_set_mean = np.mean([ train_error[parcelid] for parcelid in trimmed_set ])

def step_0(parcelid):
    return trimmed_set_mean

def submit():
    with open(path+properties_2016) as fd, open(path+my_submission, "w") as fdw:
        fd.readline()
        fdw.write("ParcelId,201610,201611,201612,201710,201711,201712\n")
        while True:
            line = fd.readline()
            if not line: break
            values = line.strip().split(",")
            values = [ values[0], "" ] + values[1:]
            parcelid = values[zcolumns["parcelid"]]
            index = index_item(values)
            index1 = (index[0], )
            ratio = 1.0
            if index1 in topn:
                ratio = topn[index1]
            logerror = 0.0115 * ratio
            e = "{:.4f}".format(logerror)
            fdw.write("{p},{e},{e},{e},{e},{e},{e}\n".format(p=parcelid, e=e))
    pass

delta_1 = { parcelid: train_error[parcelid] - step_0(parcelid) for parcelid in trimmed_set }
delta_2 = { parcelid: train_error[parcelid] - step_1(parcelid) for parcelid in trimmed_set }

def explore(cat_func, delta):
    buckets = {}
    for parcelid in trimmed_set:
        index = cat_func(parcelid)
        if index not in buckets:
            buckets[index] = set()
        buckets[index].add(parcelid)
    result = [(key, value) for (key, value) in buckets.items()]
    result.sort(key=lambda item: item[0])
    for item in result:
        error = [ delta[parcelid] for parcelid in item[1]]
        mean = np.mean(error)
        std = np.std(error)
        info = (item[0], int(mean*10000), len(error), f7(mean), f7(std))
        print(info)

explore(cat_year_2, delta_1)

def step_1_bucketing():
    buckets = {}
    for parcelid in trimmed_set:
        index = cat_year_2(parcelid)
        if index not in buckets:
            buckets[index] = set()
        buckets[index].add(parcelid)
    buckets_mean = {}
    for index, bucket in buckets.items():
        delta = [ delta_1[parcelid] for parcelid in bucket ]
        mean = np.mean(delta)
        buckets_mean[index] = mean
    return buckets, buckets_mean

step_1_buckets, step_1_buckets_mean = step_1_bucketing()

def step_1(parcelid):
    index = cat_year_2(parcelid)
    value = step_0(parcelid) + step_1_buckets_mean[index]
    return value

def cut(bound):
    errors = [ train_error[parcelid] for parcelid in train_set if abs(train_error[parcelid]-.1) < bound ]
    mean = np.mean(errors)
    std = np.std(errors)
    info = (float("{:.1f}".format(bound)), len(errors), float("{:.7f}".format(mean)), float("{:.7f}".format(std)))
    print(info)

def temp1():
    for i in range(7):
        bound = .7 - i * .1
        cut(bound)

def f7(value):
    return float("{:.7f}".format(value))

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

def cat_year_2(parcelid):
    try:
        year = int(train_data[parcelid][zcolumns["yearbuilt"]].split(".")[0])
    except:
        return "0: noyear"
    if year < 1920: return "1: <1920"
    if year < 1930: return "2: 1920-1930"
    if year < 1935: return "3: 1930-1935"
    if year < 1960: return "4: 1935-1960"
    if year < 1965: return "5: 1960-1965"
    if year < 1980: return "6: 1965-1980"
    if year < 1985: return "7: 1980-1985"
    if year < 1990: return "8: 1985-1990"
    if year < 2010: return "9: 1990-2010"
    return "10: >2010"

def cat_year_3(parcelid):
    try:
        year = int(train_data[parcelid][zcolumns["yearbuilt"]].split(".")[0])
    except:
        return "0: noyear"
    if year < 1958: return "1: before 1958"
    if year < 1966: return "2: 58-66"
    if year < 1974: return "3: 66-74"
    if year < 1984: return "4: 74-84"
    if year < 1990: return "5: 84-90"
    return "6: after 90"

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

def cat_sqft_2(parcelid):
    try:
        sqft = int(float(train_data[parcelid][zcolumns["calculatedfinishedsquarefeet"]]))
    except:
        return "0: no sqft"
    if sqft < 500: return "small: <500"
    for i in range(40):
        begin = 500 + i * 100
        end = 500 + (i+1) * 100
        if sqft < end: return "c{:02d}: {}-{}".format(i+1, begin, end)
    return "big: >4500"

def cat_sqft_3(parcelid):
    try:
        sqft = int(float(train_data[parcelid][zcolumns["calculatedfinishedsquarefeet"]]))
    except:
        return "0: no sqft"
    if sqft < 600: return "1: small <600"
    if sqft < 2000: return "2: 600-2000"
    if sqft < 2700: return "3: 2000-2700"
    if sqft < 3100: return "4: 2700-3100"
    if sqft < 3900: return "5: 3100-3900"
    return "6: big: >3900"

def cat_year_sqft_1(parcelid):
    cat_year = cat_year_3(parcelid)
    cat_sqft = cat_sqft_3(parcelid)
    return (cat_year, cat_sqft)

def bucketing(cat_func):
    buckets = {}
    for parcelid in train_set:
        index = cat_func(parcelid)
        if index not in buckets:
            buckets[index] = set()
        buckets[index].add(parcelid)
    result = [(key, value) for (key, value) in buckets.items()]
    result.sort(key=lambda item: item[0])
    for item in result:
        error1 = [ train_error[parcelid] for parcelid in item[1] ]
        error2 = [ train_error[parcelid] for parcelid in item[1] if parcelid in trimmed_set ]
        mean1 = np.mean(error1)
        mean2 = np.mean(error2)
        std1 = np.std(error1)
        std2 = np.std(error2)
        info = (item[0], len(error1), f7(mean1), f7(std1), len(error2), f7(mean2), f7(std2))
        info = (item[0], len(error2), f7(mean2), f7(std2))
        print(info)

def graphit(cat_func):
    buckets = {}
    for parcelid in train_set:
        index = cat_func(parcelid)
        if index not in buckets:
            buckets[index] = set()
        buckets[index].add(parcelid)
    gf = {}
    for index in buckets:
        error2 = [ train_error[parcelid] for parcelid in buckets[index] if parcelid in trimmed_set ]
        mean2 = np.mean(error2)
        std2 = np.std(error2)
        count2 = len(error2)
        index1, index2 = index
        index1 = int(index1.split(":")[0])
        index2 = int(index2.split(":")[0])
        gf[(index1, index2)] = (mean2, count2)
    return gf

def zf(x, y):
    return [ [gf[point][0] for point in zip(*item)] for item in zip(x, y) ]

def zfc(x, y):
    return [ [gf[point][1] for point in zip(*item)] for item in zip(x, y) ]

def temp2():
    x = np.arange(1, 7)
    y = np.arange(1, 7)
    X, Y = np.meshgrid(x, y)
    Z = zf(X, Y)
    ZC = zfc(X, Y)

    bucketing(cat_year_sqft_1)
    gf = graphit(cat_year_sqft_1)

    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.RdBu,linewidth=0, antialiased=False)
    surfc = ax.plot_surface(X, Y, ZC, rstride=1, cstride=1, cmap=cm.RdBu,linewidth=0, antialiased=False)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

