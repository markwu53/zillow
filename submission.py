import numpy as np
import zipfile
import time

path = "/Users/apple/Documents/Programs/zillow/"
path = "/Programs/kaggle/zillow/"
path = "/Users/Public/Documents/Kaggle/zillow/"
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
push_factor = 0.1
function_export = "function_export.log"

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
    ["regionidzip", myint, list(range(96000, 97400, 20)), ],
    ["latitude", myint, list(range(33200000, 35000000, 18000)), ],
    ["longitude", myint, list(range(-119500000, -117500000, 20000)), ],
]

exported_functions = [
(6, 23, 0.021878510849856699, 0.0069949560481733959),
(6, 23, 0.01969065976487103, 0.006295460443356056),
(6, 22, 0.018332068571962144, 0.0057099938717803398),
(6, 22, 0.016498861714765927, 0.0051389944846023054),
(1, 13, 0.0033608636953752755, 0.011080078791355953),
(6, 23, 0.013854407218678462, 0.0038381958660292483),
(1, 12, 0.0018599205715527512, 0.009031224665716174),
(8, 15, 0.00041476213326163588, 0.0077612875188291606),
(6, 22, 0.012022742979837922, 0.0023766956178015502),
(1, 14, 0.0012843696201831, 0.0081959121650442435),
(8, 9, -0.0034105827715017983, 0.0057033025285424524),
(6, 18, 0.012388401227770971, 0.0014309213641049345),
(1, 12, -0.00024092009011979484, 0.0059271173954356382),
(6, 20, 0.0099319752182384022, 0.00090529226484333653),
(1, 14, -1.7401995243582474e-05, 0.0059799322161162276),
(8, 9, -0.0041349088392995653, 0.0039751035889922558),
(3, 4, -0.00023397883378505549, 0.0052512662768498522),
(6, 23, 0.0073882782499912368, -1.8670664443304057e-06),
(1, 12, -0.001064497036820773, 0.0040088264770082186),
(6, 15, 0.010681898476384899, -4.7090184666517908e-05),
(8, 9, -0.004306091176720879, 0.0028811617931877387),
(3, 4, -0.0008180280072211635, 0.0041263419286947456),
(6, 15, 0.0094858450087148653, -0.00030416684239623423),
(1, 22, -0.00043859823682496719, 0.0084204220394175633),
(8, 9, -0.0041394507688326419, 0.0022666670066715023),
(6, 23, 0.0052158521211843204, -0.00063677892741398963),
(1, 12, -0.0015827570507743192, 0.0027570717269949354),
(1, 22, -0.00060374840593476343, 0.0072480827045043467),
(6, 15, 0.0079893142144047118, -0.00062994792496416879),
(10, 73, -0.0010897715440836033, 0.0033171435711499358),
(8, 8, -0.0043738842802921989, 0.0016543782925063557),
(3, 4, -0.0011660490301725395, 0.0027674114374724602),
(6, 34, 0.0027608857315189008, -0.0012662558995581107),
(1, 22, -0.00076944053147122654, 0.0062985991916131422),
(6, 15, 0.0069257290008590397, -0.00076046816583128613),
(0, 58, -0.0023390776006195105, 0.0016545861554479754),
(1, 12, -0.0015725736121416933, 0.0018975070747408026),
(6, 34, 0.0023851246285119831, -0.0012599897886001045),
(10, 73, -0.0011213967685306568, 0.0025285789790820056),
(1, 22, -0.0008069102080196527, 0.005518098510869934),
]

use_iteration = 20

def approx_function_1(values, iteration):
    pushes = []
    for func in exported_functions[:iteration]:
        feature = features[func[0]]
        value = feature[1](values[zcolumns[feature[0]]])
        splitting_point = feature[2][func[1]]
        target = func[2] if value < splitting_point else func[3]
        pushes.append(push_factor * target)
    return np.sum(pushes)

def approx_function_2(values):
    set_value = 0.0
    for feature_index, feature in enumerate(features):
        value = feature[1](values[zcolumns[feature[0]]])
        early_break = False
        for index, point in enumerate(feature_splittings[feature_index]):
            if value < feature[2][point]:
                set_value += feature_set_values[feature_index][index]
                early_break = True
                break
        if not early_break:
            set_value += feature_set_values[feature_index][-1]
    return push_factor * set_value

def combine_function(iteration):
    use_functions = exported_functions[:iteration]
    feature_splittings = [set() for feature in features]
    for item in use_functions:
        feature_splittings[item[0]].add(item[1])
    feature_splittings = [list(item) for item in feature_splittings]
    for item in feature_splittings:
        item.sort()
    feature_set_values = [[0.0]*(len(item)+1) for item in feature_splittings]
    for item in use_functions:
        feature_index = item[0]
        this_point = item[1]
        for index, point in enumerate(feature_splittings[feature_index]):
            if point <= this_point:
                feature_set_values[feature_index][index] += item[2]
            else:
                feature_set_values[feature_index][index] += item[3]
        feature_set_values[feature_index][-1] += item[3]
    return feature_splittings, feature_set_values

def logMessage(message):
    print("[{}] {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))

def submit():
    with open(path+properties_2016) as fd, open(path+my_submission, "w") as fdw:
        fd.readline()
        fdw.write("ParcelId,201610,201611,201612,201710,201711,201712\n")
        lcount = 0
        while True:
            line = fd.readline()
            if not line: break
            lcount += 1
            if lcount % 100000 == 0:
                logMessage(lcount)
            values = line.strip().split(",")
            parcelid = values[zcolumns["parcelid"]]
            logerror = approx_function_2(values)
            e = "{:.4f}".format(logerror)
            fdw.write("{p},{e},{e},{e},{e},{e},{e}\n".format(p=parcelid, e=e))

def zipit():
    with zipfile.ZipFile(path+my_submission+".zip", "w", compression=zipfile.ZIP_DEFLATED) as fd:
        fd.write(path+my_submission)

feature_splittings, feature_set_values = combine_function(use_iteration)
submit()
#zipit()
