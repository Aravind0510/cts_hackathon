from flask import Flask, request, render_template_string
import snowflake.connector

app = Flask(__name__)

# Configure Snowflake connection
def get_snowflake_connection():
    conn = snowflake.connector.connect(
        user='dheepika13',
        password='Dheepika@13',
        account='sx93925.ap-southeast-1',
        warehouse='COMPUTE_WH',
        database='patient',
        schema='patient_details'
    )
    return conn

# Handle Patient Registration
@app.route('/register-patient', methods=['POST'])
def register_patient():
    try:
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

        print(f"Received data: {first_name}, {last_name}, {date_of_birth}, {age}, {phone_number}, {address}, {emergency_contact}, {emergency_phone}, {gender}, {email}")

        conn = get_snowflake_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO patients (first_name, last_name, date_of_birth, age, phone_number, address, emergency_contact, emergency_phone, gender, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (first_name, last_name, date_of_birth, age, phone_number, address, emergency_contact, emergency_phone, gender, email))
        conn.commit()
        return render_template_string("<h3>Patient Registration Successful!</h3>")
    except Exception as e:
        return render_template_string(f"<h3>An error occurred: {e}</h3>")
    finally:
        cursor.close()
        conn.close()


# Handle Doctor Registration
@app.route('/register-doctor', methods=['POST'])
def register_doctor():
    first_name = request.form['doctor_first_name']
    last_name = request.form['doctor_last_name']
    specialization = request.form['specialization']
    contact_number = request.form['contact_number']
    email = request.form['email']
    address = request.form['address']
    gender = request.form['gender']

    conn = get_snowflake_connection()
    cursor = conn.cursor()
    
    try:
        sql = """
        INSERT INTO doctors (first_name, last_name, specialization, contact_number, email, address, gender)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (first_name, last_name, specialization, contact_number, email, address, gender))
        conn.commit()
        return render_template_string("<h3>Doctor Registration Successful!</h3>")
    except Exception as e:
        return render_template_string(f"<h3>An error occurred: {e}</h3>")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
