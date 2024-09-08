from flask import Flask, render_template, request, redirect, url_for
import snowflake.connector

app = Flask(__name__)

# Snowflake database connection
conn_params = {
    'user': 'dheepika13',
    'password': 'Dheepika@13',
    'account': 'sx93925.ap-southeast-1',
    'warehouse': 'COMPUTE_WH',
    'database': 'patient',
    'schema': 'patient_details'
}

def get_db_connection():
    conn = snowflake.connector.connect(**conn_params)
    return conn

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # Fetch data for patients and doctors from Snowflake
    conn = get_db_connection()
    cur = conn.cursor()

    # Total patients
    cur.execute("SELECT COUNT(*) FROM patients")
    total_patients = cur.fetchone()[0]

    # New patients (within last 7 days)
    cur.execute("SELECT COUNT(*) FROM patients WHERE REGISTRATION_DATE >= CURRENT_DATE() - INTERVAL '7 DAYS'")
    new_patients = cur.fetchone()[0]

    # Today's appointments (assuming there is an 'appointments' table)
    cur.execute("SELECT COUNT(*) FROM doctors")
    total_doctors = cur.fetchone()[0]

    # New patients (within last 7 days)
    cur.execute("SELECT COUNT(*) FROM doctors WHERE REGISTRATION_DATE >= CURRENT_DATE() - INTERVAL '7 DAYS'")
    new_doctors = cur.fetchone()[0]

    # Fetch recent patients
    cur.execute("SELECT first_name, age, gender, phone_number FROM patients ORDER BY REGISTRATION_DATE DESC LIMIT 4")
    recent_patients = cur.fetchall()

    # Fetch recent doctors
    cur.execute("SELECT doctor_id, first_name, specialization, contact_number FROM doctors ORDER BY REGISTRATION_DATE DESC LIMIT 3")
    recent_doctors = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('dashboard.html', total_patients=total_patients,
                           new_patients=new_patients, total_doctors=total_doctors,new_doctors=new_doctors,
                           recent_patients=recent_patients, recent_doctors=recent_doctors)

@app.route('/register-patient', methods=['POST'])
def register_patient():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    age = request.form['age']
    phone_number = request.form['phone_number']
    address = request.form['address']
    emergency_contact = request.form['emergency_contact']
    emergency_phone = request.form['emergency_phone']
    gender = request.form['gender']
    email = request.form['email']

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO patients (first_name, last_name, date_of_birth, age, phone_number, address, emergency_contact, emergency_phone, gender, email, REGISTRATION_DATE)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
    """, (first_name, last_name, date_of_birth, age, phone_number, address, emergency_contact, emergency_phone, gender, email))

    cur.close()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/register-doctor', methods=['POST'])
def register_doctor():
    doctor_first_name = request.form['doctor_first_name']
    doctor_last_name = request.form['doctor_last_name']
    specialization = request.form['specialization']
    contact_number = request.form['contact_number']
    email = request.form['email']
    address = request.form['address']
    gender = request.form['gender']

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO doctors (first_name, last_name, specialization, contact_number, address, gender, email, REGISTRATION_DATE)
        VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
    """, (doctor_first_name, doctor_last_name, specialization, contact_number, address, gender, email))

    cur.close()
    conn.close()

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
