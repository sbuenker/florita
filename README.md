# Flood Insurance in the U.S. - Exploring New Market Opportunities

[Sebastian Buenker](https://github.com/sbuenker)

[Yasemin Erguezel](https://github.com/yaseminerguezel)

[Salil Pachare](https://github.com/saliloquy)

[Dorothee Schmitt](https://github.com/d-k-sch)

## Table of Contents
(Fill this out)
## Overview
Extreme weather events are occurring more frequently in recent years. To identify profitable insurance markets, we investigate regions with low adoption rates for flood insurance, yet are at high risk. We also classify insurance claims as likely to be approved, in order to optimise capital planning of insurers entering the market.

* Explain who our stakeholder is. 
* For replication of this project, refer to the installation file here:
* For the presentation delivered as part of the Neue Fische Graduation event, click here: 

## Research Questions
* What are our two main research questions? Take this from the presentation. 

## Data Sources
The data on policies from the [FEMA website](link) from x. Approximately x million. Discuss the main variables that we use. 

The data on claims from the [FEMA website](link) from x. Approximately x million. Discuss the main variables that we use. 

The data from US census bureau. Discuss which variables we use. 

For data cleaning/collapsing, refer to the following:
* Big Query stuff for policies
* Claims data cleaning
* Utils for helper functions

## Exploratory Data Analysis
![no of claims over the years]()

![$ damage of claims over the years]()

![flood insurance claims by region]()

![flood adoption policies]()

![flood overinsurance and underinsurance]()

There are five main findings from the figures above:

1.

2.

3. 

4. 

5.

For more exploratory data analysis refer to the following notebooks:

* EDA Claims (notebook)
* States EDA (notebook)
* Dynamic maps (notebook) and github pages link that shows the tooltips (link).
* Link to Dashboard

## Prediction of Insurance Claims Approvals
* Description of why we are doing this. 
* What is it that we are predicting? Which is the 1 variable and 0 variable.
### Feature Used and Feature Engineering
* Which groups of features do we include in ML model?
* Why we do not include year variables?
* Why we include zip codes as a feature? Rivers etc. 
* One hot encoding - which features do we make as dummy variables
* Which features do we use standard scalar.

### Model Training and Testing
* No regular time series data here.
* Train test split
* Stratification of sample to ensure that same ratio of claim approvals and non-approvals in both the train and test samples. 

### Model Metrics
* Description of True Positives and true negatives and what they mean in insurance context.
* Description of False Positives and what they mean in insurance context.
* Description of False Negatives and what they mean in insurance context.

### Model Results
For insurance claims classification, we run three models: 
  
    (1) Logistic regression without any hyperparameter tuning. This is our baseline model. 
  
    (2) Random Forest with hyperparameter tuning.
  
    (3) XGBoost with hyperparameter tuning.

Our approach for grid search for the optimal hyperparameters is to choose a random sample of the train data after the train-test split, run a randomized grid search and apply the chosen hyperparameters to the full test data.


  |Model|Accuracy (Test)|Weighted-Average F1-Score (Test)|
  |---|---|---|
  |Logistic Regression|||
  |Random Forest|||
  |XGBoost|||

For the actual hyperparameters used in the Random Forest and XGBoost, please refer to [#insertlinktonotebook]. 

### Error Analysis
* Plot confusion matrix for baseline logistic regression model.
* Plot confusion matrix for chosen XGBoost model.
* Brief comparison of the results. Which model has higher true positives and true negatives, and lower false positives and false negatives.

### Business Implications of ML Results
To calculate the monetary loss under the baseline logistic regression and under the XGBoost model, we make the following assumptions:
* Since we are doing claims classification and not encoding any time-series features, we implicitly assume that all claims are paid out contemporaneously.
* Average claim size for false positive classifications is the same as false negative classifications.
* Assume that our stakeholder can borrow at the risk-free rate (assume **2% p.a.**) when capital on their balance sheet is not enough to meet claim payouts. This is the case when we predict a claim as non-approval, but it actually approved (**false negative**).
* Assume that our stakeholder forgoes the S&P500 average market return (assume **7% p.a.**) when they hold too much capital on their balance sheet. This is the case whe we over-predict claim approvals, that is, we predict a claim as approved, but it is actually not approved (**false positive**).

Do the following calculation for the logistic model and the XGBoost model.
* Average FP ($) = no. of FP x average claim size x (1 + 0.07)
* Average FN ($) = no. of FN x average claim size x (1 + 0.02)
* Add the above two to get the total monetary loss for incorrect classifications. The difference between this for XGBoost and Logistic Regression is the savings per year due to the better model.
## Recommendations
* Enter certain markets which are under-served, that is, claims payout is high (proxy for high flood risk) and voluntary adoption rates are low. Use map as motivation. 
* Increase coverage rates of voluntarily under-insured people with flood insurance. Use map as motivation.
* XGBoost model for prediction of insurance claims classification. 

## Further Work
* We would like to examine whether the number of flood insurance policies bought can be explained using historic insurance claims. 
    * The motivation of this comes from our data analysis which shows that after regional flood events, there is a contemporaneous increase in insurance claims and a future increase in voluntary flood insurance policies bought in the region.
    * There is no significant increase in claims and voluntary flood insurance policies bought in other regions not affected by the flood event.
    * For analysis after the Louisiana Floods in 2016, refer to [link to Doro's notebook on state analysis].

* We would like to estimate the elasticity of flood insurance adoption with respect to insurance premiums. 
    * The purpose of this analysis is to see how responsive the purchase of voluntary flood insurance is to changes in insurance premiums.
    * This analysis can yield new public policy insights, for example, are there certain regions that the government should subsidize if flood insurance adoption rates are very elastic? 
    * To estimate the elasticity, we would use techniques from CausalML.

