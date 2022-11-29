import pandas as pd
import numpy as np
import datetime as dt
import utils.county_demographics

def get_demographics(columns:list, name=False, state=False):
    """
    Make DataFrame with CountyFIPS column and requested demographic columns.
    Args:
    columns: list of tuples of category and concrete value available in county_demographics
    name: add a column with the name of the county
    state: add a column with the state abbreviation of the county
    Returns:
    DataFrame 
    """
    FipsDF = pd.read_csv('../data/fips2county.tsv', sep='\t', header='infer', dtype=str, encoding='latin-1')
    FipsDF.loc[1803, 'CountyName'] = 'Dona Ana' # error with encoding on import of county name 
    FipsDF.loc[1143, 'CountyName'] = 'La Salle Parish' # error with encoding on import of county name 
    FipsDF = FipsDF[(FipsDF.CountyFIPS != '02063') & (FipsDF.CountyFIPS != '02066') & (FipsDF.CountyFIPS != '02158') & ((FipsDF.CountyFIPS != '46102'))] # missing counties
    report = utils.county_demographics.get_report()
    by_code = {}
    for item in report:
        item['CountyFull'] = item['County']
        item['County'] = ''.join(item['County'].split('County')).strip(' ')
        by_code[FipsDF[(FipsDF.CountyName == item['County']) & (FipsDF.StateAbbr == item['State'])].CountyFIPS.values[0]] = item
    df = FipsDF[['CountyFIPS']]
    for column in columns:
        df[column[1]] = [by_code[fips][column[0]][column[1]] for fips in FipsDF.CountyFIPS]
    if name:
        df['County'] =  [by_code[fips]['CountyFull'] for fips in FipsDF.CountyFIPS]
    if state:
        df['State'] =  [by_code[fips]['State'] for fips in FipsDF.CountyFIPS]
    return df

def available_columns(category_key:str=None):
    """
    Print available columns for demographics DataFrames, either for a selected category or all by default.
    Args: 
    category_key=None: string from county_demographics keys 
    Returns: None
    """
    report = utils.county_demographics.get_report()
    if category_key:
        for key in report[1][category_key]:
            print("('{}', '{}')".format(category_key, key))
    else:
        for key, value in report[1].items():
            if type(value) == dict:
                for value in value.keys():
                    print("('{}', '{}')".format(key, value))

def transform_claims_week(df):
    """
    Creates collapsed DataFrame for Claims DataFrame, by year and week
    Args:
    Claims DataFrame
    Returns: Collapsed DataFrame aggregating features by year and week
    """
    df = df[df.yearOfLoss >= 2008]
    df = df.assign(
        timestamp = lambda x: pd.to_datetime(x['dateOfLoss']), 
        year = lambda x: x['timestamp'].dt.year
        week = lambda x: x['timestamp'].dt.isocalendar().week
    )
    agg = df.groupby(['year', 'week', 'state'])[['id', 'policyCount', 'amountPaidOnBuildingClaim', 'amountPaidOnContentsClaim', 'amountPaidOnIncreasedCostOfComplianceClaim']].agg({
        'id': np.count_nonzero, 
        'policyCount': np.sum, 
        'amountPaidOnBuildingClaim': np.sum, 
        'amountPaidOnContentsClaim': np.sum, 
        'amountPaidOnIncreasedCostOfComplianceClaim': np.sum
    })
    return agg_week

def transform_claims_month(df):
    """
    Creates collapsed DataFrame for Claims DataFrame, by year and month
    Args:
    Claims DataFrame
    Returns: Collapsed DataFrame aggregating features by year and month
    """
    df = df[df.yearOfLoss >= 2008]
    df = df.assign(
        timestamp = lambda x: pd.to_datetime(x['dateOfLoss']), 
        year = lambda x: x['timestamp'].dt.year
        month = lambda x: x['timestamp'].dt.month
    )
    agg = df.groupby(['year', 'month', 'state'])[['id', 'policyCount', 'amountPaidOnBuildingClaim', 'amountPaidOnContentsClaim', 'amountPaidOnIncreasedCostOfComplianceClaim']].agg({
        'id': np.count_nonzero, 
        'policyCount': np.sum, 
        'amountPaidOnBuildingClaim': np.sum, 
        'amountPaidOnContentsClaim': np.sum, 
        'amountPaidOnIncreasedCostOfComplianceClaim': np.sum
    })
    return agg_month