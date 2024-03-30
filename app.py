import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from crop_details import get_crop_details
from flask import render_template, send_file
from io import BytesIO
from reportlab.pdfgen import canvas
from flask import make_response
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for
import sqlite3


from weather_module import get_weather_data, get_average_annual_rainfall

# Create flask app
flask_app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))


def create_table():
    conn = sqlite3.connect('user4.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                land REAL NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                prediction TEXT)''')  # Add the prediction field
    conn.commit()
    conn.close()


create_table()
# Route for login page
@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('user4.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()
        conn.close()
        if user:
            return redirect(url_for('house'))
        else:
            return 'Login failed. Please try again.'
    return render_template('login.html')


# Route for registration page
@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        address = request.form['address']
        land = request.form['land']
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('user4.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, age, phone, address, land, email, password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (name, age, phone, address, land, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')


@flask_app.route("/homepage.html")
def house():
    return render_template("homepage.html")


@flask_app.route("/index.html")
def prediction():
    return render_template("index.html")


@flask_app.route("/contact.html")
def contact():
    return render_template("contact.html")

@flask_app.route('/user_profile')
def user_profile():
    # Connect to the database
    conn = sqlite3.connect('user4.db')
    cursor = conn.cursor()

    # Fetch user information from the database
    cursor.execute("SELECT * FROM users")
    user_data = cursor.fetchone()  # Assuming only one user for simplicity

    # Close the database connection
    conn.close()

    # Pass the user data to the template for rendering
    return render_template('user_profile.html', user=user_data)


@flask_app.route("/dashboard.html")
def dashboard():
    return render_template("dashboard.html")

@flask_app.route("/dashboard1.html")
def dashboard1():
    return render_template("dashboard1.html")

@flask_app.route("/about.html")
def about_us():
    return render_template("about.html")

@flask_app.route("/help.html")
def help():
    return render_template("help.html")

@flask_app.route("/q1.html")
def q1():
    return render_template("q1.html")
@flask_app.route("/value.html")
def value():
    return render_template("value.html")




@flask_app.route("/")
def mainhome():
    return render_template("mainhome.html")

@flask_app.route("/download_pdf", methods=["POST"])
def download_pdf():
    # Get the prediction and other variables from the form data
    prediction = request.form.get("prediction")
    life_span = request.form.get("life_span")
    total_cost = request.form.get("total_cost")
    fertilizers = request.form.get("fertilizers")
    season = request.form.get("season")
    vl = request.form.get("vl")

    # Create the PDF document
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Define custom styles for the content
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading1"]
    body_style = styles["BodyText"]

    # Add content to the PDF
    content = []

    # Add a title
    title_text = "Crop Prediction Results"
    content.append(Paragraph(title_text, title_style))
    content.append(Spacer(1, 20))

    # Add prediction details
    content.append(Paragraph("Prediction:", heading_style))
    content.append(Paragraph(prediction, body_style))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Life Span:", heading_style))
    content.append(Paragraph(life_span, body_style))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Total Cost:", heading_style))
    content.append(Paragraph(total_cost, body_style))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Fertilizers:", heading_style))
    content.append(Paragraph(fertilizers, body_style))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Season:", heading_style))
    content.append(Paragraph(season, body_style))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Video link:", heading_style))
    content.append(Paragraph(vl, body_style))

    doc.build(content)

    # Create a response with the PDF file
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=prediction.pdf"
    response.headers["Content-type"] = "application/pdf"

    return response

from flask import jsonify
dataset_path="A:\ml_project\A_A_R.csv"

@flask_app.route('/get_aar/<city>')
def get_aar(city):
    avg_rainfall = round((get_average_annual_rainfall(city, dataset_path)),2)
    return jsonify({'avg_rainfall': avg_rainfall})



import sqlite3



from flask import session

@flask_app.route("/predict", methods=["POST"])
def predict():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = model.predict(features)[0]

    # Get the email of the logged-in user from the session
    email = session.get('email')

    # Save the prediction to the database for the logged-in user
    save_prediction_to_database(email, prediction)

    # Call the get_crop_details function with the predicted crop name
    crop_details = get_crop_details(prediction)

    # Handle the response appropriately, such as returning it as JSON
    if crop_details == 'Crop not found.':
        return jsonify({'error': 'Crop not found.'})

    life_span, total_cost, fertilizers, season, vl = crop_details

    # Pass the prediction and crop details to the final.html template
    return render_template("final.html", prediction=prediction, life_span=life_span, total_cost=total_cost,
                           fertilizers=fertilizers, season=season, vl=vl)


def save_prediction_to_database(email, prediction):
    conn = sqlite3.connect('user4.db')
    cur = conn.cursor()
    cur.execute("UPDATE users SET prediction=? WHERE email=?", (prediction, email))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    flask_app.run(debug=True)