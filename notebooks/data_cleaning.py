import pandas as pd

"""
Apart from dropping rows that seem to contain data entry errors, dropping unused columns and
imputing missing data, clean_claims adds aggregate columns, used in data visualization and ML.
"""
def clean_claims(df:pd.DataFrame):
    
