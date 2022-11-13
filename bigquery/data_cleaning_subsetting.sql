# the steps below subset the original FEMA policies dataset based on variables needed for analysis

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
      WHEN occupancyType IN (4,6,17,18,19) THEN 'Commercial' # occupancyType = 4,6,17,18,19 can be classified as commertial
      ELSE NULL
    END AS buildingType,
    *,
  FROM cte2
  WHERE occupancyType IS NOT NULL
), 

# step 4. create new columns for fema insurance limits and sfha flood risk
cte4 AS (
  SELECT
    CASE
      WHEN buildingType = 'Residential' THEN 250000 # max flood insurance is $250k.
      WHEN buildingType = 'Residential-Multi' THEN 500000 # max flood insurance is $500k
      WHEN buildingType = 'Commercial' THEN 500000 # max flood insurance is $500k.
      ELSE NULL
    END AS fema_ins_max,
    CASE
      WHEN SUBSTRING(floodZone,1,1) IN ('A','V') THEN 1
      WHEN SUBSTRING(floodZone,1,1) IN ('B','C','X') THEN 0
      ELSE NULL
    END AS sfha_flood_risk,
    *
  FROM cte3
  WHERE floodZone IS NOT NULL
)

# step 5. final conditioning of data
# keep policyTermIndicator of 1 year, remove the others
  # makes it easier to identify adoption rates each year
# delete cancellationDateOfFloodPolicy IS NOT NULL
  # cancellation year can be different from termination date, making it hard to identify adoption rates each year

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
  buildingType,
  fema_ins_max,
  sfha_flood_risk
FROM cte4
WHERE
  policyTermIndicator=1 AND 
  cancellationDateOfFloodPolicy IS NULL 

# only 0.85% of observations lost from filtering in steps 1-5