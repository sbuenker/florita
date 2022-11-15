import pandas as pd
import county_demographics

def get_demographics(columns:list):
    """
    Make DataFrame with CountyFIPS column and requested demograpic columns.
    Args:
    columns: list of tuples of category and concrete value available in county_demopgraphics
    Returns:
    DataFrame 
    """
    FipsDF = pd.read_csv("fips2county.tsv", sep='\t', header='infer', dtype=str, encoding='latin-1')
    FipsDF.loc[1803, "CountyName"] = "Dona Ana"
    FipsDF.loc[1143, "CountyName"] = "La Salle Parish"
    FipsDF = FipsDF[(FipsDF.CountyFIPS != '02063') & (FipsDF.CountyFIPS != '02066') & (FipsDF.CountyFIPS != '02158') & ((FipsDF.CountyFIPS != '46102'))]
    report = county_demographics.get_report()
    by_code = {}
    for item in report:
        item["County"] = "".join(item["County"].split("County")).strip(" ")
        by_code[FipsDF[(FipsDF.CountyName == item["County"]) & (FipsDF.StateAbbr == item["State"])].CountyFIPS.values[0]] = item
    df = FipsDF[["CountyFIPS"]]
    for column in columns:
        df[column[1]] = [by_code[fips][column[0]][column[1]] for fips in FipsDF.CountyFIPS]
    return df

def available_columns(category_key:str=None):
    """
    Print available columns for demographics DataFrames, either for a selected category or all by default.
    Args: 
    category_key=None: string from county_demographics keys 
    Returns: None
    """
    report = county_demographics.get_report()
    if category_key:
        for key in report[1][category_key]:
            print("('{}', '{}')".format(category_key, key))
    else:
        for key, value in report[1].items():
            if type(value) == dict:
                for value in value.keys():
                    print("('{}', '{}')".format(key, value))