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

if __name__ == "__main__":
    submit_quant()
