import pandas as pd

"""
Apart from dropping a few rows that seem to contain data entry errors, dropping unused columns and replacing string date columns with numerical year columns, clean_state adds some columns, mostly to facilitate distinguishing mandatory from voluntary insurance policies, 
by separating groups of flood zones (flood insurance being mandatory in zones with designations starting with "A" or "V") and adding an indicator for the policy containing content coverage 
(as opposed to just building coverage), which is voluntary. 
"""
def clean_state(df:pd.DataFrame):
    """
    Enhance DataFrame with convenience columns concerning voluntariness of insurance and drop rows with obviously wrong start date.
    Args:
    df: DataFrame
    Returns:
    DataFrame 
    """
    df.reset_index(drop=True, inplace=True)
    df["start_year"] = df.policyEffectiveDate.str[0:4].astype("int16")
    df = df[df.start_year > 2002]
    df["term_year"] = df.policyTerminationDate.str[0:4].astype("int16")
    df["construction_year"] = df.originalConstructionDate.str[0:4].astype("float16")
    df["originalNB_year"] = df.originalNBDate.str[0:4].astype("float16")
    df.drop(["originalNBDate", "originalConstructionDate", "policyTerminationDate", "policyEffectiveDate", 
       "agricultureStructureIndicator", "baseFloodElevation",
       "basementEnclosureCrawlspace", "cancellationDateOfFloodPolicy", "censusTract", "construction",
       "elevationDifference", "houseOfWorshipIndicator",
       "latitude", "longitude", "locationOfContents", "lowestAdjacentGrade",
       "lowestFloorElevation", "nonProfitIndicator",
       "numberOfFloorsInTheInsuredBuilding", "reportedZipCode", "reportedCity", "obstructionType",
       "policyTermIndicator", "smallBusinessIndicatorBuilding"], axis=1, inplace=True)
    df["genFloodZone"] = df.floodZone.str[0]
    df["pooledFloodZone"] = [x if str(x) not in "XBCD" else "X, B, C, D" for x in df.genFloodZone]
    df["zoneStatus"] = ["Mandatory" if str(x) not in "XBCD" else "Voluntary" for x in df.genFloodZone]
    df["contentInsurance"] = df.totalContentsInsuranceCoverage > 0
    return df