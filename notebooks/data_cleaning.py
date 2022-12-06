import pandas as pd
import numpy as np

"""
Apart from dropping rows that seem to contain data entry errors, dropping unused columns and
imputing missing data, clean_claims adds aggregate columns, used in data visualization and ML.
"""
def clean_claims(df:pd.DataFrame):
    '''
    Cleans the dataframe and deals with an imputes missing data. Adds aggregate columns to the dataframe.
    '''
    # deal with coverage first
    df = df[df['totalBuildingInsuranceCoverage'].notna()]
    df = df[df['totalContentsInsuranceCoverage'].notna()]
    df.eval('totalinsurancecoverage = totalBuildingInsuranceCoverage + totalContentsInsuranceCoverage',inplace = True)
    df["totalContentsInsuranceCoverage"]= df.totalContentsInsuranceCoverage.astype(int)
    df["totalBuildingInsuranceCoverage"]= df.totalBuildingInsuranceCoverage.astype(int)
    df["totalinsurancecoverage"]= df.totalinsurancecoverage.astype(int)

    # then move on to amount paid
    df['amountPaidOnBuildingClaim'] = df['amountPaidOnBuildingClaim'].replace(np.nan, 0)
    df['amountPaidOnContentsClaim'] = df['amountPaidOnContentsClaim'].replace(np.nan, 0)
    df['amountPaidOnIncreasedCostOfComplianceClaim'] = df['amountPaidOnIncreasedCostOfComplianceClaim'].replace(np.nan, 0)
    # df["amountPaidOnContentsClaim"]= df.amountPaidOnContentsClaim.astype(int)
    # df["amountPaidOnBuildingClaim"]= df.amountPaidOnBuildingClaim.astype(int)
    df["amountPaidOnIncreasedCostOfComplianceClaim"]= df.amountPaidOnIncreasedCostOfComplianceClaim.astype(int)
    # df["amountPaidOnTotalClaim"]= df.amountPaidonTotalClaim.astype(int)
    df['amountPaidOnBuildingClaim']= np.abs(df['amountPaidOnBuildingClaim'])
    df['amountPaidOnContentsClaim']= np.abs(df['amountPaidOnContentsClaim'])
    df['amountPaidOnIncreasedCostOfComplianceClaim'] = np.abs(df['amountPaidOnIncreasedCostOfComplianceClaim'])
    df.eval('amountPaidOnTotalClaim = amountPaidOnBuildingClaim + amountPaidOnContentsClaim + amountPaidOnIncreasedCostOfComplianceClaim',inplace = True)

    # next deal with the other features
    df['baseFloodElevation'].fillna(0, inplace=True)
    df["baseFloodElevation"]= df.baseFloodElevation.astype(int)
    df["lowestFloorElevation"]= df.lowestFloorElevation.astype(int)
    df.eval('new_elev_diff = lowestFloorElevation - baseFloodElevation',inplace = True)

    df = df.drop('elevationDifference', axis=1)
    df["condominiumIndicator"] = df["condominiumIndicator"].fillna('Not_specified')





