from builtins import reversed
from numba.targets.npyfuncs import _NPY_LOGE2
def logerror_mean():
    mean = "0.0115"
    sample_submission = "/Users/apple/Documents/zillow/zillow_submission/sample_submission.csv"
    with open(sample_submission) as fd: lines = fd.readlines()
    header = lines[0].strip()
    lines = lines[1:]
    lines = [ line.split(",")[0] for line in lines ]
    lines = [ "{parcel},{mean},{mean},{mean},{mean},{mean},{mean}".format(parcel=line, mean=mean) for line in lines ]
    lines = [ header ] + lines
    my_submission = "/Users/apple/Documents/zillow/zillow_submission/my_submission.csv"
    with open(my_submission, "w") as fd:
        for line in lines:
            fd.write("{}\n".format(line))
    print("done")

def logerror_taxvalue():
    pass

def explore():
    quant = [
        "0.0954203",
        "0.1659274",
        "0.2249346",
        "0.2806082",
        "0.3380210",
        "0.4000000",
        "0.4748882",
        "0.5899994",
        "0.7941437",
    ]
    rscript = """
a <- subset(dataset_tax, dataset_tax$tax_value_dollar_cnt/1000000 > {} & dataset_tax$tax_value_dollar_cnt/1000000 < {})
mean(a$logerror)
"""
    quant_pair = list(zip(["0"]+quant, quant+["1"]))
    for item in quant_pair: print(item)
    #for item in quant_pair: print(rscript.format(*item))

submission_quant = """
0,0.0954203,0.0157
0.0954203,0.1659274,0.0142
0.1659274,0.2249346,0.0115
0.2249346,0.2806082,0.0121
0.2806082,0.3380210,0.0087
0.3380210,0.4000000,0.0084
0.4000000,0.4748882,0.0059
0.4748882,0.5899994,0.0104
0.5899994,0.7941437,0.0107
0.7941437,1000,0.0139
"""

def zillow_columns():
    with open("zillow_columns") as fd: content = fd.read()
    lines = content.strip().splitlines()
    lines = [ line.strip() for line in lines if len(line.strip()) != 0 ]
    content = "".join(lines)
    columns = content.split(sep=",")
    columns = dict([ (value, index-2) for (index, value) in enumerate(columns)])
    return columns

def zillowcolumns():
    columns = """
parcelid,airconditioningtypeid,architecturalstyletypeid,basementsqft,bathroomcnt,bedroomcnt,buildingclasstypeid,buildingqualitytypeid,calculatedbathnbr,decktypeid,finishedfloor1squarefeet,calculatedfinishedsquarefeet,finishedsquarefeet12,finishedsquarefeet13,finishedsquarefeet15,finishedsquarefeet50,finishedsquarefeet6,fips,fireplacecnt,fullbathcnt,garagecarcnt,garagetotalsqft,hashottuborspa,heatingorsystemtypeid,latitude,longitude,lotsizesquarefeet,poolcnt,poolsizesum,pooltypeid10,pooltypeid2,pooltypeid7,propertycountylandusecode,propertylandusetypeid,propertyzoningdesc,rawcensustractandblock,regionidcity,regionidcounty,regionidneighborhood,regionidzip,roomcnt,storytypeid,threequarterbathnbr,typeconstructiontypeid,unitcnt,yardbuildingsqft17,yardbuildingsqft26,yearbuilt,numberofstories,fireplaceflag,structuretaxvaluedollarcnt,taxvaluedollarcnt,assessmentyear,landtaxvaluedollarcnt,taxamount,taxdelinquencyflag,taxdelinquencyyear,censustractandblock
"""
    columns = columns.strip().split(sep=",")
    return dict([(value, index) for (index, value) in enumerate(columns)])

def calcError(dollar_string, subm_cond):
    try:
        dollar = float(dollar_string)
    except:
        return "0.0115"
    for cond in subm_cond:
        if dollar/1000000 >= float(cond[0]) and dollar/1000000 <= float(cond[1]):
            return cond[2]
    return "0.0115"
 
def submit_quant():
    subm_cond = submission_quant.splitlines()
    subm_cond = [ line.strip().split(sep=",") for line in subm_cond if len(line.strip()) != 0]
    properties_file = "/Users/apple/Documents/zillow/data/properties_2016.csv"
    my_submission = "/Users/apple/Documents/zillow/zillow_submission/my_submission.csv"
    columns = zillow_columns()
    with open(properties_file) as fdr, open(my_submission, "w") as fdw:
        header = fdr.readline()
        fdw.write("ParcelId,201610,201611,201612,201710,201711,201712\n")
        processed = 0
        while True:
            line = fdr.readline()
            if line is None: break
            if len(line.strip()) == 0: continue
            processed = processed + 1
            if processed % 100000 == 0: print(processed)
            column_values = line.split(",")
            parcel = column_values[0]
            dollar = column_values[columns["tax_value_dollar_cnt"]]
            logerror = calcError(dollar, subm_cond)
            line = "{parcel},{mean},{mean},{mean},{mean},{mean},{mean}\n".format(parcel=parcel, mean=logerror)
            fdw.write(line)

def explore_year():
    rscript = """
a <- subset(dataset_year, as.integer(dataset_year$year_built) >= {} & as.integer(dataset_year$year_built) < {})
mean(a$logerror)
"""
    other = """
a <- subset(dataset_year, as.integer(dataset_year$year_built) >= {} | as.integer(dataset_year$year_built) < {})
mean(a$logerror)
"""
    rscripts = [
        rscript.format("1920", "1930"),
        rscript.format("1930", "1940"),
        rscript.format("1940", "1950"),
        rscript.format("1950", "1960"),
        rscript.format("1960", "1970"),
        rscript.format("1970", "1980"),
        rscript.format("1980", "1990"),
        rscript.format("1990", "2000"),
        rscript.format("2000", "2010"),
        other.format("2010", "1920"),
    ]
    print("\n".join(rscripts))

 
def year_error(year_s):
    try:
        year = int(year_s)
    except:
        return "0.0115"
    if year >= 1920 and year < 1930: return "0.0047"
    if year >= 1930 and year < 1940: return "0.0055"
    if year >= 1940 and year < 1950: return "0.0067"
    if year >= 1950 and year < 1960: return "0.0094"
    if year >= 1960 and year < 1970: return "0.0166"
    if year >= 1970 and year < 1980: return "0.0102"
    if year >= 1980 and year < 1990: return "0.0129"
    if year >= 1990 and year < 2000: return "0.0136"
    if year >= 2000 and year < 2010: return "0.0184"
    if year >= 2010 or year < 1920: return "0.0063"
    return "0.0115"

def submit_year():
    properties_file = "/Users/apple/Documents/zillow/data/properties_2016.csv"
    my_submission = "/Users/apple/Documents/zillow/zillow_submission/my_submission.csv"
    columns = zillow_columns()
    with open(properties_file) as fdr, open(my_submission, "w") as fdw:
        header = fdr.readline()
        fdw.write("ParcelId,201610,201611,201612,201710,201711,201712\n")
        processed = 0
        while True:
            line = fdr.readline()
            processed = processed + 1
            if processed % 100000 == 0: print(processed)
            column_values = line.split(",")
            parcel = column_values[0]
            year = column_values[columns["year_built"]]
            year = year.split(sep=".")[0]
            logerror = year_error(year)
            line = "{parcel},{mean},{mean},{mean},{mean},{mean},{mean}\n".format(parcel=parcel, mean=logerror)
            fdw.write(line)

def dollar_temp():
    d = [
    "0.0954203",
    "0.1659274",
    "0.2249346",
    "0.2806082",
    "0.3380210",
    "0.4000000",
    "0.4748882",
    "0.5899994",
    "0.7941437",
        ]
    statements = ["if dollar >= {} and dollar < {}: return {}".format(*value, index+1) for (index, value) in enumerate(zip([0.0]+d, d+[1.0]))]
    print("\n".join(statements))

def dollar_class(dollar):
    """
    return 0 to 10
    """
    try:
        dollar = float(dollar)
    except:
        return 0
    dollar = dollar / 1000000.0
    if dollar < 0.0954203: return 1
    if dollar >= 0.0954203 and dollar < 0.1659274: return 2
    if dollar >= 0.1659274 and dollar < 0.2249346: return 3
    if dollar >= 0.2249346 and dollar < 0.2806082: return 4
    if dollar >= 0.2806082 and dollar < 0.3380210: return 5
    if dollar >= 0.3380210 and dollar < 0.4000000: return 6
    if dollar >= 0.4000000 and dollar < 0.4748882: return 7
    if dollar >= 0.4748882 and dollar < 0.5899994: return 8
    if dollar >= 0.5899994 and dollar < 0.7941437: return 9
    if dollar >= 0.7941437: return 10
    return 0

def year_class(year):
    """
    return 0 to 9
    """
    year = year.split(".")[0]
    try:
        year = int(year)
    except:
        return 0
    if year >= 1920 and year < 1930: return 1
    if year >= 1930 and year < 1940: return 2
    if year >= 1940 and year < 1950: return 3
    if year >= 1950 and year < 1960: return 4
    if year >= 1960 and year < 1970: return 5
    if year >= 1970 and year < 1980: return 6
    if year >= 1980 and year < 1990: return 7
    if year >= 1990 and year < 2000: return 8
    if year >= 2000 and year < 2010: return 9
    return 0

def bucket_year_dollar():
    properties_file = "/Users/T162880/Documents/Programs/zillow/properties_2016.csv"
    train_file = "/Users/T162880/Documents/Programs/zillow/train_2016_v2.csv"

    train_set = set()
    train_dict = dict()
    with open(train_file) as fd:
        header = fd.readline()
        while True:
            line = fd.readline()
            if not line: break
            line = line.strip()
            if len(line) == 0: continue
            values = line.split(",")
            parcelid = values[0]
            train_set.add(parcelid)
            train_dict[parcelid] = float(values[1])

    columns = zillowcolumns()
    bucket = [[[set(), set()] for dr in range(11)] for yr in range(10)]
    with open(properties_file) as fd:
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
            year = values[columns["yearbuilt"]]
            dollar = values[columns["taxvaluedollarcnt"]]
            parcelid = values[columns["parcelid"]]
            #logerror = values[columns["logerror"]]
            yclass = year_class(year)
            dclass = dollar_class(dollar)
            bucket[yclass][dclass][0].add(parcelid)
            if parcelid in train_set:
                bucket[yclass][dclass][1].add((parcelid, train_dict[parcelid]))
    def est(train):
        return "0.0115" if len(train) < 10 else "{:.4f}".format(float(sum([ logerror for (parcelid, logerror) in train])) / len(train))
    ests = [ [ est(bucket[yclass][dclass][1]) for dclass in range(11)] for yclass in range(10)]

    my_submission_file = "/Users/T162880/Documents/Programs/zillow/my_submission.csv"
    with open(my_submission_file, "w") as fd:
        fd.write("ParcelId,201610,201611,201612,201710,201711,201712\n")
        for yclass in range(10):
            for dclass in range(11):
                test = bucket[yclass][dclass][0]
                logerror = ests[yclass][dclass]
                for parcelid in test:
                    fd.write("{p},{a},{a},{a},{a},{a},{a}\n".format(p=parcelid, a=logerror))
    print("done")

    """
    for yr in range(10):
        count = [ (len(item[0]), len(item[1])) for item in bucket[yr]]
        print(count)
[(13276, 0), (44689, 526), (13724, 303), (15439, 380), (12939, 353), (10857, 304), (9364, 316), (9628, 340), (11061, 403), (12222, 438), (18226, 625)]
[(42, 0), (34492, 859), (28035, 584), (30278, 595), (25415, 579), (20055, 496), (15489, 404), (12769, 364), (12623, 423), (12957, 438), (19238, 734)]
[(18, 0), (14305, 373), (11663, 240), (12502, 228), (11477, 214), (9819, 211), (8147, 179), (7146, 199), (7891, 188), (8646, 281), (14198, 502)]
[(20, 0), (44955, 1252), (33966, 681), (39215, 645), (36901, 744), (30864, 707), (25740, 660), (20296, 501), (18754, 495), (17548, 601), (18952, 723)]
[(288, 0), (103393, 3234), (69297, 1631), (74380, 1342), (76411, 1462), (67100, 1548), (64015, 1707), (56974, 1684), (40634, 1232), (30165, 967), (30963, 1097)]
[(3854, 0), (54675, 1510), (51715, 1470), (39581, 913), (42853, 990), (41952, 1040), (39669, 1063), (38942, 1191), (41328, 1248), (36013, 1206), (26837, 947)]
[(9715, 0), (24298, 663), (58464, 1818), (52706, 1759), (48487, 1551), (45298, 1518), (39679, 1422), (36991, 1334), (37587, 1317), (34949, 1220), (25156, 910)]
[(6696, 1), (9889, 325), (42769, 1535), (50763, 2003), (45323, 1832), (41226, 1689), (36299, 1476), (33875, 1334), (33697, 1253), (31492, 1136), (31718, 1176)]
[(4009, 0), (3090, 76), (11925, 444), (17598, 627), (17904, 630), (19052, 715), (20175, 800), (22350, 883), (25606, 973), (27532, 1060), (36566, 1402)]
[(4632, 0), (2317, 48), (3597, 158), (9200, 374), (12321, 515), (13957, 638), (17638, 827), (21734, 1061), (28128, 1337), (31784, 1518), (50145, 2222)]
"""

def bucket_bath():
    properties_file = "/Users/T162880/Documents/Programs/zillow/properties_2016.csv"
    train_file = "/Users/T162880/Documents/Programs/zillow/train_2016_v2.csv"
    my_submission_file = "/Users/T162880/Documents/Programs/zillow/my_submission.csv"
    columns = zillowcolumns()
    with open(properties_file) as fd, open(my_submission_file, "w") as fdw:
        header = fd.readline()
        fdw.write("ParcelId,201610,201611,201612,201710,201711,201712\n")
        ln = 0
        while True:
            line = fd.readline()
            ln = ln + 1
            if ln % 100000 == 0: print(ln)
            if not line: break
            line = line.strip()
            if len(line) == 0: continue
            values = line.split(",")
            bath = values[columns["bathroomcnt"]]
            parcelid = values[columns["parcelid"]]
            try:
                bath = int(bath)
                if bath == 1: logerror = "0.0074"
                elif bath == 2: logerror = "0.0092"
                elif bath == 3: logerror = "0.0146"
                elif bath == 4: logerror = "0.0180"
                else: logerror = "0.0115"
            except:
                logerror = "0.0115"
            fdw.write("{p},{a},{a},{a},{a},{a},{a}\n".format(p=parcelid, a=logerror))
    print("done")
            
def sqrt_class(sqrt):
    try:
        sqrt = float(sqrt)
    except:
        return 0
    begin = 200
    end = 6000
    step = 200
    if sqrt < float(begin) or sqrt >= float(end): return 0
    cls = 1
    sb = begin
    while True:
        if sqrt >= float(sb) and sqrt < float(sb+step): return cls
        cls += 1
        sb += step

def bucket_sqrt():
    #properties_file = "/Users/T162880/Documents/Programs/zillow/properties_2016.csv"
    #train_file = "/Users/T162880/Documents/Programs/zillow/train_2016_v2.csv"
    #my_submission_file = "/Users/T162880/Documents/Programs/zillow/my_submission.csv"
    properties_file = "/Users/apple/Documents/zillow/data/properties_2016.csv"
    train_file = "/Users/apple/Documents/zillow/data/train_2016_v2.csv"
    my_submission_file = "/Users/apple/Documents/zillow/zillow_submission/my_submission.csv"
    columns = zillowcolumns()
    train_dict = dict()
    sqrt_dict = dict()
    with open(train_file) as fd:
        header = fd.readline()
        while True:
            line = fd.readline()
            if not line: break
            line = line.strip()
            if len(line) == 0: continue
            values = line.split(",")
            parcelid = values[0]
            train_dict[parcelid] = float(values[1])
    with open(properties_file) as fd:
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
            parcelid = values[columns["parcelid"]]
            if parcelid in train_dict:
                logerror = train_dict[parcelid]
                sqrt = values[columns["calculatedfinishedsquarefeet"]]
                csqrt = sqrt_class(sqrt)
                if csqrt not in sqrt_dict: sqrt_dict[csqrt] = list()
                sqrt_dict[csqrt].append(float(logerror))
    sqrt_log = {}
    for key in sqrt_dict:
        sqrt_log[key] = "{:.4f}".format(sum(sqrt_dict[key])/len(sqrt_dict[key]))
    print(sqrt_log)
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
            parcelid = values[columns["parcelid"]]
            sqrt = values[columns["calculatedfinishedsquarefeet"]]
            logerror = sqrt_log[sqrt_class(sqrt)]
            fdw.write("{p},{a},{a},{a},{a},{a},{a}\n".format(p=parcelid, a=logerror))
    print("done")

if __name__ == "__main__":
    bucket_sqrt()
