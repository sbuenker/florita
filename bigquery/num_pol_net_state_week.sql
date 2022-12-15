# the steps below:
    # subset the original FEMA policies dataset based on variables needed to determine voluntary purchases of flood insurance
    # calculate the purchases, terminations and net policies bought in any given week in any given state

# input: FEMA NFIP Policies dataset: https://www.fema.gov/openfema-data-page/fima-nfip-redacted-policies-v1 
  # FEMA data uploaded to Google Cloud Storage and imported as SQL dataset in BigQuery
# output: generates SQL table which is subsequently saved as "num_pol_net_state_week.csv" 

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
),

# step 5. conditioning of data
# keep policyTermIndicator of 1 year, remove the others
  # makes it easier to identify adoption rates each year
# delete cancellationDateOfFloodPolicy IS NOT NULL
  # cancellation year can be different from termination date, making it hard to identify adoption rates each year
# keep observations where flood insurance purchase is not mandatory:
  # sfha_food_risk=0 OR totalContentsInsuranceCoverage>0
cte5 AS (
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
    (sfha_flood_risk=0 OR totalContentsInsuranceCoverage>0) AND
    cancellationDateOfFloodPolicy IS NULL
),

# step 6. determine which policies are bought in any given week
pol_eff AS (
  SELECT
    year AS year_eff,
    EXTRACT(week FROM policyEffectiveDate) AS week_eff,
    propertyState,
    SUM(policyCount) AS num_policies_eff,
  FROM cte5
  WHERE year>=2009
  GROUP BY 1, 2, 3
  ORDER BY 1, 2, 3
), 

# step 7. determine which policies are terminated in any given week
pol_term AS (
  SELECT
    EXTRACT(year FROM policyTerminationDate) AS year_term,
    EXTRACT(week FROM policyTerminationDate) AS week_term,
    propertyState,
    SUM(policyCount) As num_policies_term
  FROM cte5
  WHERE EXTRACT(year FROM policyTerminationDate)>=2009
    GROUP BY 1, 2, 3
    ORDER BY 1, 2, 3
),

# step 8. combine policies which are bought and policies which are terminated
# calculate net bought policies in any given week
pol AS (
  SELECT
    pol_eff.year_eff AS year,
    pol_eff.week_eff AS week,
    pol_eff.propertyState,
    pol_eff.num_policies_eff,
    pol_term.num_policies_term AS num_policies_term,
    (pol_eff.num_policies_eff - pol_term.num_policies_term) as num_policies_net
  FROM pol_eff
  LEFT JOIN pol_term
  ON pol_eff.year_eff = pol_term.year_term AND 
     pol_eff.week_eff = pol_term.week_term AND
     pol_eff.propertyState = pol_term.propertyState
  ORDER BY 1, 2, 3
),

# step 9. encode null values from num_policies_term as zero
pol2 AS (
  SELECT
    *,
    CASE
      WHEN num_policies_term IS NULL THEN 0
      ELSE num_policies_term
    END AS num_policies_term_2
  FROM pol
)

# step 10. final dataset of number of policies bought, terminated and net policies by year, week, propertyState
SELECT
  year,
  week,
  propertyState,
  num_policies_eff AS num_policies_bought,
  num_policies_term_2 AS num_policies_term,
  num_policies_eff - num_policies_term_2 AS num_policies_net
FROM pol2
