import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px

st.set_page_config(page_title="Patient Care Dashboard", layout="wide")
st.title("📊 Patient Care Coordination Dashboard")
st.caption("Analysis of follow-up care post-discharge (using Synthea synthetic health data)")

# Sidebar – Snowflake connection input
st.sidebar.header("🧩 Snowflake Connection")

sf_user = st.sidebar.text_input("Username", "SIDJAYMEN")
sf_password = st.sidebar.text_input("Password", type="password")
sf_account = st.sidebar.text_input("Account", "ECWVWPV-XDB83330")
sf_database = st.sidebar.text_input("Database", "SYNTHEA_DATA")
sf_schema = st.sidebar.text_input("Schema", "RAW")
sf_warehouse = st.sidebar.text_input("Warehouse", "COMPUTE_WH")

if st.sidebar.button("Connect & Load Data"):
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            user=sf_user,
            password=sf_password,
            account=sf_account,
            warehouse=sf_warehouse,
            database=sf_database,
            schema=sf_schema,
            role="ACCOUNTADMIN",
        )

        # Load and clean data
        query = "SELECT * FROM patient_followup"
        df = pd.read_sql(query, conn)
        df.columns = df.columns.str.upper()

        # Add risk segmentation
        def classify_risk(row):
            if pd.isnull(row.get("FIRST_FOLLOWUP_DATE")):
                return "High Risk"
            elif row.get("DAYS_TO_FOLLOWUP", 999) > 7:
                return "Medium Risk"
            else:
                return "Low Risk"

        df["RISK_LEVEL"] = df.apply(classify_risk, axis=1)

        # Handle boolean field
        if "TIMELY_FOLLOWUP" in df.columns:
            df["TIMELY_FOLLOWUP"] = df["TIMELY_FOLLOWUP"].astype("boolean")
        else:
            st.warning("Column 'TIMELY_FOLLOWUP' not found in your data.")
            df["TIMELY_FOLLOWUP"] = None

        # Sidebar Filters
        st.sidebar.subheader("🔍 Filter Data")

        followup_filter = st.sidebar.selectbox(
            "Follow-up Status",
            options=["All", "Timely", "Missed"],
            index=0
        )

        patient_search = st.sidebar.text_input("Search by Patient ID")

        if followup_filter == "Timely":
            df = df[df["TIMELY_FOLLOWUP"] == True]
        elif followup_filter == "Missed":
            df = df[df["TIMELY_FOLLOWUP"] == False]

        if patient_search:
            df = df[df["PATIENT_ID"].astype(str).str.contains(patient_search, case=False, na=False)]
            
    # 🚨 Optional drill-down for High Risk patients
        high_risk_toggle = st.sidebar.checkbox("🚨 View High Risk Patients Only", value=False)

        if high_risk_toggle:
            df = df[df["RISK_LEVEL"] == "High Risk"]


        # Metrics Section
        st.success(f"✅ Loaded {len(df)} records")
        st.subheader("📈 Overview Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Total Discharges", len(df))
        timely_pct = df["TIMELY_FOLLOWUP"].mean() if not df.empty else 0
        col2.metric("⏱️ Timely Follow-up Rate", f"{timely_pct:.1%}")
        high_risk_count = (df["RISK_LEVEL"] == "High Risk").sum()
        col3.metric("🚨 High Risk Patients", high_risk_count)

        # Section: Days to Follow-up Histogram
        st.subheader("⏱️ Days to Follow-up Distribution")
        if not df.empty and "DAYS_TO_FOLLOWUP" in df.columns:
            fig1 = px.histogram(df, x="DAYS_TO_FOLLOWUP", nbins=15,
                                title="Distribution of Follow-up Gaps (in Days)",
                                labels={"DAYS_TO_FOLLOWUP": "Days to Follow-up"})
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No data available for follow-up timing.")

        # Section: Follow-up Status Pie
        st.subheader("📍 Follow-up Completion Status")
        if not df.empty and "TIMELY_FOLLOWUP" in df.columns:
            fig2 = px.pie(df, names="TIMELY_FOLLOWUP", title="Follow-up within 7 Days",
                          color_discrete_sequence=["green", "red"])
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No data to display follow-up completion.")

        # Section: Risk Breakdown Pie
        st.subheader("🚨 Patient Risk Segmentation")
        if not df.empty and "RISK_LEVEL" in df.columns:
            fig3 = px.pie(df, names="RISK_LEVEL", title="Patient Risk Breakdown",
                          color_discrete_map={
                              "High Risk": "red",
                              "Medium Risk": "orange",
                              "Low Risk": "green"
                          })
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No data to display risk segmentation.")

        # Table Section
        with st.expander("📋 Show Raw Data Table"):
            st.dataframe(df)

    except Exception as e:
        st.error(f"❌ Connection failed: {e}")
