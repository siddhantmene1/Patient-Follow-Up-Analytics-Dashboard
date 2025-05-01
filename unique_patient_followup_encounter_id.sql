
    
    

select
    encounter_id as unique_field,
    count(*) as n_records

from SYNTHEA_DATA.RAW.patient_followup
where encounter_id is not null
group by encounter_id
having count(*) > 1


