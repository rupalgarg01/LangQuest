from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@_oracle1234",
    database="database1"
)

# Create a cursor object
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('login.html')

# Route to render login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check login credentials against the database
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            # Login successful, redirect to a dashboard or home page
            return redirect("http://127.0.0.1:5500/index.html#Home")
        else:
            # Login failed, render login page with an error message
            return render_template('login.html', error='Invalid email or password')

    # Render the login page
    return render_template('login.html')

# Route to render signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Insert new user into the database
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        db.commit()

        # Redirect to the login page after successful signup
        return redirect(url_for('login'))

    # Render the signup page
    return render_template('signup.html')

# Route for the dashboard or home page
@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

if __name__ == '__main__':
    app.run(debug=True)