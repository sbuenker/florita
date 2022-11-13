# calculate the following by occupancyType/county/state/year observation:
  # average totalBuildingInsuranceCoverage
  # average totalContentsInsuranceCoverage
  # average totalInsurancePremiumOfThePolicy
  # average policyCost
  # average building insurace per policy = average (totalBuildingInsuranceCoverage/policyCount)
  # total policyCount

# step 1. check fraction of missing values for the variables above
SELECT
    ROUND((SUM(CASE WHEN totalBuildingInsuranceCoverage IS NULL THEN 1 ELSE 0 END)/COUNT(*))*100,4)
    AS frac_missing_building_ins_cov,
    ROUND((SUM(CASE WHEN totalContentsInsuranceCoverage IS NULL THEN 1 ELSE 0 END)/COUNT(*))*100,4)
    AS frac_missing_contents_ins_cov,
    ROUND((SUM(CASE WHEN totalInsurancePremiumOfThePolicy IS NULL THEN 1 ELSE 0 END)/COUNT(*))*100,4)
    AS frac_missing_ins_prem,
    ROUND((SUM(CASE WHEN policyCost IS NULL THEN 1 ELSE 0 END)/COUNT(*))*100,4)
    AS frac_missing_policy_cost,
    ROUND((SUM(CASE WHEN policyCount IS NULL THEN 1 ELSE 0 END)/COUNT(*))*100,4)
    AS frac_missing_policy_count
FROM `civic-planet-368014.flood_policies.fema_policies_cleaned`
# 0.0002% of values are missing for totalBuildingInsuranceCoverage
# 0.0034% of values are missing for totalContentsInsuranceCoverage
# no missing values for totalInsurancePremiumOfThePolicy, policyCost, policyCount

# step 2. encode missing values for totalBuildingInsuranceCoverage and totalContentsInsuranceCoverage as zero
WITH cte AS (
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
  FROM `civic-planet-368014.flood_policies.fema_policies_cleaned`
) 

# step 3. calculate all the averages and totals mentioned above
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
  SUM(policyCount) AS tot_pol_cnt
FROM cte
WHERE countyCode IS NOT NULL
GROUP BY countyCode, propertyState, year, buildingType, occupancyType
ORDER BY countyCode, propertyState, year, buildingType, occupancyType