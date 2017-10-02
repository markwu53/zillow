from builtins import reversed
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

if __name__ == "__main__":
    submit_year()
