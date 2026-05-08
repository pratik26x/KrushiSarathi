"""KrushiSarathi — farmer financial inclusion, soil testing, and crop recommendation web app."""
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

import joblib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL — same credentials as init_database.py / setup_mysql.sql
_DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "farmers_db",
    "connection_timeout": 5,
}

db = None
cursor = None


def init_db_connection():
    """Open or refresh MySQL connection (handles idle disconnect)."""
    global db, cursor
    try:
        if db is not None and db.is_connected():
            db.ping(reconnect=True, attempts=3, delay=1)
            return
    except mysql.connector.Error:
        pass
    db = mysql.connector.connect(**_DB_CONFIG)
    cursor = db.cursor()


def ensure_db_connection():
    """Ensure DB is reachable for routes that require it."""
    init_db_connection()


model = joblib.load('crop_recommendation_model.pkl')


# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"

@app.route('/dataAnalysis')
def dataAnalysis():
    return render_template('dataAnalysis.html')

@app.route('/soilTesting')
def soilTesting():
    return render_template('soilTesting.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/cropRecommendation')
def cropRecommendation():
    return render_template('cropRecommendation.html')

@app.route('/recommendationForm')
def recommendationForm():
    return render_template('recommendationForm.html')

@app.route('/loans')
def loans():
    return render_template('loans.html')

@app.route('/loanDetails')
def loanDetails():
    return render_template('loanDetails.html')

@app.route('/schemes')
def schemes():
    return render_template('schemes.html')

@app.route('/savings')
def savings():
    return render_template('' \
    'savings.html')



# feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

@app.route('/recommendationForm', methods=['GET', 'POST'])
def get_crop_recommendation():
    if request.method == 'POST':
        nitrogen = float(request.form['nitrogen'])
        phosphorous = float(request.form['phosphorous'])
        potassium = float(request.form['potassium'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        input_data = [[nitrogen, phosphorous, potassium, temperature, humidity, ph, rainfall]]

        predicted_crop = model.predict(input_data)[0]

        return render_template('recommendationResult.html', predicted_crop=predicted_crop)
    
    return render_template('recommendationForm.html')


@app.route('/recommendationResult')
def recommendation_result():
    return render_template('recommendationResult.html')

# Signup route
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']

#         # Insert user into the database
#         try:
#             cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
#             db.commit()
#             flash('You have successfully signed up!')
#             return redirect(url_for('login'))
#         except mysql.connector.errors.IntegrityError:
#             flash('Email already exists. Please use another email.')
#             return redirect(url_for('signup'))

#     return render_template('signup.html')


# Login Route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
#         user = cursor.fetchone()

#         if user:
#             flash('Login Successful!')
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Invalid credentials. Please sign up first.')
#             return redirect(url_for('signup'))
        
#     return render_template('signup.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        # Inserting user into the database
        try:
            ensure_db_connection()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
            db.commit()
            flash('You have successfully signed up!', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f'Database error: {err}', 'error')
            return redirect(url_for('signup'))
        except mysql.connector.errors.IntegrityError:
            flash('Email already exists. Please login', 'error')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetching user from the database
        try:
            ensure_db_connection()
        except mysql.connector.Error as err:
            flash(f'Database error: {err}', 'error')
            return redirect(url_for('signup'))
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            session['logged_in'] = True
            session['username'] = user[1]
            session['user_id'] = user[0]
            # flash('Login Successful!', 'success')

            return render_template('index.html')
        else:
            flash('Invalid credentials.', 'error')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return render_template('index.html')


@app.route('/confirm_appointment', methods=['POST'])
def confirm_appointment():
    if 'user_id' not in session:
        # If user is not logged in
        return jsonify({'status': 'error', 'message': 'Please log in to book an appointment.'})

    user_id = session['user_id']
    data = request.get_json()

    lab_name = data['labName']
    contact_person = data['contactPerson']
    visit_date = datetime.strptime(data['visitDate'], '%Y-%m-%d').date()
    contact_number = data['contactNumber']

    # Inserting appointment data into the database
    query = '''
        INSERT INTO appointments (user_id, lab_name, contact_person, visit_date, contact_number)
        VALUES (%s, %s, %s, %s, %s)
    '''
    
    try:
        ensure_db_connection()
        cursor.execute(query, (user_id, lab_name, contact_person, visit_date, contact_number))
        db.commit()
    except mysql.connector.Error as err:
        return jsonify({'status': 'error', 'message': str(err)})
    
    return jsonify({'status': 'success'})




if __name__ == "__main__":
    app.run(debug=True, port=5001)
