
  create or replace   view SYNTHEA_DATA.RAW.patient_followup
  
   as (
    WITH discharge_encounters AS (
    SELECT
        "PATIENT" AS patient_id,
        "ID" AS encounter_id,
        "STOP" AS discharge_date
    FROM raw.encounters
    WHERE LOWER("ENCOUNTERCLASS") = 'inpatient'
),

followup_encounters AS (
    SELECT
        "PATIENT" AS patient_id,
        "START" AS followup_date
    FROM raw.encounters
    WHERE LOWER("ENCOUNTERCLASS") IN ('ambulatory', 'outpatient')
),

patient_followups AS (
    SELECT
        d.patient_id,
        d.encounter_id,
        d.discharge_date,
        MIN(f.followup_date) AS first_followup_date,
        DATEDIFF('day', d.discharge_date, MIN(f.followup_date)) AS days_to_followup
    FROM discharge_encounters d
    LEFT JOIN followup_encounters f
        ON d.patient_id = f.patient_id
        AND f.followup_date > d.discharge_date
    GROUP BY d.patient_id, d.encounter_id, d.discharge_date
)

SELECT 
    *,
    CASE 
        WHEN days_to_followup <= 7 THEN TRUE 
        ELSE FALSE 
    END AS timely_followup
FROM patient_followups
  );

