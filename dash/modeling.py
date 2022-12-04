#from aix360.algorithms.rbm import LogisticRuleRegression, FeatureBinarizer
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn import tree
from sklearn import metrics
from sklearn.model_selection import cross_val_score
#from xgboost import XGBClassifier
#from scipy.stats import f_oneway
#from scipy.stats import chi2_contingency
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Load and preprocess dataset
date_cols = ['asOfDate','dateOfLoss','originalConstructionDate','originalNBDate']
df = pd.read_csv("/Users/sbuenker/neuefische/florita/data/claims/FimaNfipClaims.csv", parse_dates=date_cols, dtype={'countyCode': 'str', 'reportedZipcode': 'str'})

num_features = ['baseFloodElevation','policyCount','elevationDifference','lowestAdjacentGrade','lowestFloorElevation','amountPaidOnBuildingClaim',\
                'amountPaidOnContentsClaim','amountPaidOnIncreasedCostOfComplianceClaim','totalBuildingInsuranceCoverage','totalContentsInsuranceCoverage']
geo_features = ['latitude','longitude','countyCode','state']
df = df[num_features + geo_features]
targets = ['amountPaidOnBuildingClaim','amountPaidOnContentsClaim','amountPaidOnIncreasedCostOfComplianceClaim']
for c in targets:
    df[c] = df[c].abs()
df.eval('total_coverage = totalBuildingInsuranceCoverage + totalContentsInsuranceCoverage', inplace=True)
df.eval('total_claims = amountPaidOnBuildingClaim + amountPaidOnContentsClaim', inplace=True)
df['claim_accepted'] = np.where(df.total_claims.isnull(), 0, 1)

# for k, v in num2desc.items():
#     df[k] = df[k].replace(v)

y = df.pop("claim_accepted")
dfTrain, dfTest, yTrain, yTest = train_test_split(df, y, random_state=42, stratify=y)

# fb = FeatureBinarizer(negations=True, returnOrd=True)
# dfTrain, dfTrainStd = fb.fit_transform(dfTrain)
# dfTest, dfTestStd = fb.transform(dfTest)

# # Train model
# lrr = LogisticRuleRegression(lambda0=0.005, lambda1=0.001, useOrd=True)
# lrr.fit(dfTrain, yTrain, dfTrainStd)