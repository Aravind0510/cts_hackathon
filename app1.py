from flask import Flask, render_template
import pandas as pd
import snowflake.connector

app = Flask(__name__)

# Snowflake connection configuration
conn = snowflake.connector.connect(
    user='SRIMATHI',
    password='Shri@1608',
    account='ev90757.ap-southeast-1',
    warehouse='COMPUTE_WH',
    database='MEC',
    schema='JSON'
)

def run_query(query):
    cur = conn.cursor()
    cur.execute(query)
    df = cur.fetch_pandas_all()
    cur.close()
    return df

@app.route('/')
def index():
    # Sample Queries
    gender_distribution_query = """
    SELECT PATIENT_DETAILS:gender::STRING AS gender, COUNT(*) AS count
    FROM PATIENT_DETAILS
    GROUP BY PATIENT_DETAILS:gender
    """
    df_gender_distribution = run_query(gender_distribution_query)

    total_admission_query = """
    SELECT COUNT(*) AS count
    FROM ADMISSION_DISCHARGE_DATA;
    """
    df_admission = run_query(total_admission_query)

    total_doctors_query = """
    SELECT COUNT(DISTINCT DOCTOR_DETAILS:doctor_id) AS count
    FROM DOCTOR_DETAILS;
    """
    df_doctors = run_query(total_doctors_query)

    admission_outcome_query = """
    SELECT 
        ADMISSION_DISCHARGE_DATA:admission.admission_type::STRING AS admission_type,  
        COUNT(*) AS count
    FROM ADMISSION_DISCHARGE_DATA
    GROUP BY ADMISSION_DISCHARGE_DATA:admission.admission_type
    """
    df_admission_outcome = run_query(admission_outcome_query)

    common_medications_query = """
    SELECT MEDICAL_HISTORIES:medical_history.medications[0].medication_name::STRING AS medication_name, COUNT(*) AS count
    FROM MEDICAL_HISTORIES
    GROUP BY MEDICAL_HISTORIES:medical_history.medications[0].medication_name
    ORDER BY count DESC
    LIMIT 10
    """
    df_common_medications = run_query(common_medications_query)

    surgeries_performed_query = """
    SELECT MEDICAL_HISTORIES:medical_history.surgeries[0].surgery_type::STRING AS surgery_type, COUNT(*) AS count
    FROM MEDICAL_HISTORIES
    GROUP BY MEDICAL_HISTORIES:medical_history.surgeries[0].surgery_type
    """
    df_surgeries_performed = run_query(surgeries_performed_query)


    age_group_distribution_query = """
    SELECT 
        CASE 
            WHEN PATIENT_DETAILS:age::INT BETWEEN 0 AND 18 THEN '0-18'
            WHEN PATIENT_DETAILS:age::INT BETWEEN 19 AND 35 THEN '19-35'
            WHEN PATIENT_DETAILS:age::INT BETWEEN 36 AND 50 THEN '36-50'
            WHEN PATIENT_DETAILS:age::INT BETWEEN 51 AND 65 THEN '51-65'
            ELSE '65+'
        END AS age_group,
        COUNT(*) AS count
    FROM PATIENT_DETAILS
    GROUP BY age_group
    """
    df_age_group_distribution = run_query(age_group_distribution_query)

    upcoming_appointments_query = """
    SELECT COUNT(DISTINCT pd.PATIENT_DETAILS:patient_id::int) AS patient_count
    FROM PATIENT_DETAILS pd
    JOIN UPCOMING_APPOINTMENTS ua
    ON pd.PATIENT_DETAILS:patient_id = ua.UPCOMING_APPOINTMENTS:patient_id,
    LATERAL FLATTEN(input => ua.UPCOMING_APPOINTMENTS:upcoming_appointments) appt
    WHERE EXTRACT(MONTH FROM TO_DATE(appt.value:date::string, 'YYYY-MM-DD')) = EXTRACT(MONTH FROM CURRENT_DATE())
    AND EXTRACT(YEAR FROM TO_DATE(appt.value:date::string, 'YYYY-MM-DD')) = EXTRACT(YEAR FROM CURRENT_DATE());
    """
    df_upcoming_appointments = run_query(upcoming_appointments_query)

 

    total_patients_kpi = df_gender_distribution['COUNT'].sum()
    total_admission_kpi = df_admission['COUNT'].iloc[0]
    total_doctors_kpi = df_doctors['COUNT'].iloc[0]
    upcoming_appointments_kpi = df_upcoming_appointments['PATIENT_COUNT'].iloc[0]

    return render_template('index.html',
                        total_patients=total_patients_kpi,
                        total_doctors=total_doctors_kpi,
                        total_admissions=total_admission_kpi,
                        upcoming_appointments=upcoming_appointments_kpi,
                        gender_distribution=df_gender_distribution.to_dict(orient='records'),
                        age_group_distribution=df_age_group_distribution.to_dict(orient='records'),
                        admission_outcome=df_admission_outcome.to_dict(orient='records'),
                        common_medications=df_common_medications.to_dict(orient='records'),
                        surgeries_performed=df_surgeries_performed.to_dict(orient='records'))



if __name__ == '__main__':
    app.run(debug=True)
