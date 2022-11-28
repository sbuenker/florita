# the steps below subset the original FEMA policies dataset to determine voluntary and mandatory purchases of flood insurance
# additionally, the steps also calculate the following by occupancyType/buildingyType/sfha/county/state/year observation:
  # average totalBuildingInsuranceCoverage
  # average totalContentsInsuranceCoverage
  # average totalInsurancePremiumOfThePolicy
  # average policyCost
  # average building insurace per policy = average(totalBuildingInsuranceCoverage/policyCount)
  # average contents insurance per policy = average(totalContentsInsuranceCoverage/policyCount)
  # total policyCount

# step 1. subset data on columns we need; convert countyCode to string; extract year from date
WITH cte AS (
  SELECT
    CAST(countyCode AS STRING) AS countyCode,
    propertyState,
    EXTRACT(year FROM policyEffectiveDate) AS year,
    totalBuildingInsuranceCoverage,
    totalContentsInsuranceCoverage,
    totalInsurancePremiumOfThePolicy,
    policyCost,
    policyCount,
    occupancyType,
    policyTermIndicator,
    originalNBDate,
    cancellationDateOfFloodPolicy,
    policyEffectiveDate,
    policyTerminationDate,
    floodZone
  FROM `civic-planet-368014.flood_policies.fema_policies`
),

# step 2. for 4-digit countyCode, add leading zero; # for 1,2,3-digit countyCode, these are misclassified, therefore remove them from the dataset
cte2 AS (
  SELECT
    CASE
      WHEN CHAR_LENGTH(countyCode)=4 THEN '0' || countyCode
      WHEN CHAR_LENGTH(countyCode) IN (1,2,3) THEN NULL
      ELSE countyCode
    END AS countyCode_str,
    *
  FROM cte
  WHERE countyCode IS NOT NULL
),

# step 3. define building type; either residential, residential-multi, or commercial
cte3 AS (
  SELECT
    CASE
      WHEN occupancyType IN (1,2,11,12,14,15,16) THEN 'Residential' # occupancyType = 1,2,11,12,14,15,16 can be classified as residential 
      WHEN occupancyType IN (3,13) THEN 'Residential-Multi' # occupancyType = 3,13 can be classified as residential-multi family
      WHEN occupancyType IN (4,6,17,18,19) THEN 'Commercial' # occupancyType = 4,6,17,18,19 can be classified as commercial
      ELSE NULL
    END AS buildingType,
    *,
  FROM cte2
  WHERE occupancyType IS NOT NULL
),

# step 4. conditioning of data
# keep policyTermIndicator of 1 year, remove the others
  # makes it easier to identify adoption rates each year
# delete cancellationDateOfFloodPolicy IS NOT NULL
  # cancellation year can be different from termination date, making it hard to identify adoption rates each year

cte4 AS (
  SELECT
    countyCode_str AS countyCode,
    propertyState,
    year,
    totalBuildingInsuranceCoverage,
    totalContentsInsuranceCoverage,
    totalInsurancePremiumOfThePolicy,
    policyCost,
    policyCount,
    occupancyType,
    policyTermIndicator,
    cancellationDateOfFloodPolicy,
    policyEffectiveDate,
    policyTerminationDate,
    buildingType
  FROM cte3
  WHERE
  policyTermIndicator=1 AND
  cancellationDateOfFloodPolicy IS NULL 
), 

# step 5. encode missing values for totalBuildingInsuranceCoverage and totalContentsInsuranceCoverage as zero
cte5 AS (
  SELECT
    CASE
      WHEN totalBuildingInsuranceCoverage IS NULL THEN 0
      ELSE totalBuildingInsuranceCoverage
    END AS totalBuildingInsuranceCoverage_nonull,
    CASE
      WHEN totalContentsInsuranceCoverage IS NULL THEN 0
      ELSE totalContentsInsuranceCoverage
    END AS totalContentsInsuranceCoverage_nonull, 
    *
  FROM cte4
) 

# step 6. calculate all the averages and totals mentioned above
SELECT
  countyCode,
  propertyState,
  year,
  buildingType,
  occupancyType,
  AVG(totalBuildingInsuranceCoverage_nonull) AS avg_bld_ins,
  AVG(totalContentsInsuranceCoverage_nonull) AS avg_con_ins,
  AVG(totalInsurancePremiumOfThePolicy) AS avg_tot_ins,
  AVG(policyCost) AS avg_pol_cost,
  AVG(totalBuildingInsuranceCoverage/policyCount) AS bld_ins_per_pol,
  AVG(totalContentsInsuranceCoverage/policyCount) AS con_ins_per_pol,
  SUM(policyCount) AS tot_pol_cnt
FROM cte5
WHERE countyCode IS NOT NULL
GROUP BY countyCode, propertyState, year, buildingType, occupancyType
ORDER BY countyCode, propertyState, year, buildingType, occupancyType
