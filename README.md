# CarePath: Patient Follow-Up Analytics Dashboard

**CarePath** is a real-time healthcare analytics platform designed to monitor post-discharge patient follow-ups, identify gaps in care coordination, and flag high-risk patients. Built using Snowflake, dbt, and Streamlit, it enables healthcare teams and CXOs to make faster, data-driven decisions that can reduce readmission rates and improve patient outcomes.

---

## Problem Statement

In healthcare, post-discharge follow-up is critical to ensuring patient recovery and avoiding costly readmissions. However, tracking whether patients receive timely follow-up care is often manual, error-prone, and delayed.

**CarePath solves this by:**
- Tracking every discharged patient’s follow-up timeline
- Automatically flagging patients who missed follow-up windows
- Classifying patients into **High**, **Medium**, or **Low Risk**
- Presenting a real-time, filterable dashboard for action

---

## Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| **Data Storage** | Snowflake | Scalable, cloud-native data warehouse |
| **Transformation** | dbt | Modular SQL modeling + data quality testing |
| **Visualization** | Streamlit | Interactive UI for filtering and drill-downs |
| **Version Control** | Git + GitHub | Code management and deployment pipeline |

---

## Key KPIs Modeled

- **Timely Follow-Up Rate**: % of patients followed up within 7 days of discharge  
- **Average Days to Follow-Up**: Mean follow-up window across patients  
- **Risk Segmentation**: High, Medium, Low based on follow-up behavior  
- **High-Risk Patient Count**: Patients with zero follow-ups post-discharge  

---

## Features

✅ Filter patients by risk level, follow-up status, or patient ID  
✅ View total discharges, follow-up success rate, and follow-up delays  
✅ Drill down into **High Risk** patients instantly  
✅ Data quality enforced via `dbt test` for nulls, uniqueness, and logic  
✅ Powered by clean, versioned dbt SQL models from raw Synthea data  

---

## Project Structure
- Set up Python env
- Configure Snowflake
- Update profiles.yml inside ~/.dbt/ with your Snowflake account details
- Run dbt models
- Launch the app using Streamlit

---

## Acknowledgments
- Synthea for synthetic patient data
- dbt for the modern data transformation layer
- Streamlit for its simplicity in building quick, powerful UIs

---

## Demo

<img width="1428" alt="Screenshot 2025-05-01 at 4 30 19 AM" src="https://github.com/user-attachments/assets/698c0541-7a57-4ce4-91e1-dc44f4f61ce7" />


<img width="1428" alt="Screenshot 2025-05-01 at 4 31 02 AM" src="https://github.com/user-attachments/assets/857458bf-5bdc-4ca2-b340-0eb91e8f7cf7" />


<img width="1428" alt="Screenshot 2025-05-01 at 4 31 30 AM" src="https://github.com/user-attachments/assets/f7431b5c-97e3-4d4e-8135-9c22b96edb83" />
