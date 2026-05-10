import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from dotenv import load_dotenv
import cv2 as cv
import numpy as np
import sqlite3
import requests
import datetime

load_dotenv()

# Load Haar Cascade
haar_cascade = cv.CascadeClassifier("haarcascade.xml")


people = [
    {"id": "22L31A0433", "role": "student"},   
    {"id": "22L31A0431", "role": "student"},
    {"id": "23L35A0404", "role": "student"},
    {"id": "22L31A0414", "role": "student"},   
          
]

# Load trained model
face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read("face_trained.yml")

# Cache variables
last_update = 0
update_interval = 300
cached_weather = ""
cached_temp = ""
cached_quote = ""

# ---------------- DATABASE FUNCTIONS ---------------- #

def get_user_data(user_id):
    con = sqlite3.connect("smartMirror.db")
    cursor = con.cursor()

    cursor.execute(
        "SELECT id,name,year,branch,section,attendence FROM studentInfo WHERE id=?",
        (user_id,)
    )

    data = cursor.fetchone()
    con.close()
    return data


def get_lecturer_data(lecturer_id):
    con = sqlite3.connect("smartMirror.db")
    cursor = con.cursor()

    cursor.execute(
        "SELECT id,name,department,subject,experience FROM lecturerInfo WHERE id=?",
        (lecturer_id,)
    )

    data = cursor.fetchone()
    con.close()
    return data

# ---------------- API FUNCTIONS ---------------- #

def get_weather():
    try:
        API_KEY = os.getenv("OPENWEATHER_API_KEY")
        CITY = "Visakhapatnam"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        return data["weather"][0]["description"], data["main"]["temp"]
    except:
        return "Clear sky", 25


def get_quote():
    try:
        data = requests.get("https://zenquotes.io/api/random").json()
        return data[0]["q"]
    except:
        return "Stay positive and keep building!"

# ---------------- FLASK APP ---------------- #

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route("/")
def home():
    return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return render_template("index.html")
    return render_template("login.html")


@app.route("/recognize", methods=["POST"])
def recognize():

    global last_update, cached_weather, cached_temp, cached_quote

    if "image" not in request.files:
        return jsonify({"error": "No image received"}), 400

    file = request.files["image"]

    img = cv.imdecode(np.frombuffer(file.read(), np.uint8), cv.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Invalid image"}), 400

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # ---- Weather & Quote Cache ---- #
    current_time = datetime.datetime.now().timestamp()

    if current_time - last_update > update_interval:
        cached_weather, cached_temp = get_weather()
        cached_quote = get_quote()
        last_update = current_time

    weather = cached_weather
    temp = cached_temp
    quote = cached_quote

    now = datetime.datetime.now()
    time_now = now.strftime("%H:%M:%S")
    date = now.strftime("%d-%m-%Y")

    # ---- Face Detection ---- #
    faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 4)

    print(f"Faces detected: {len(faces_rect)}")

    for (x, y, w, h) in faces_rect:

        face_roi = gray[y:y+h, x:x+w]
        face_roi = cv.resize(face_roi, (200, 200))
        face_roi = cv.equalizeHist(face_roi)
        face_roi = cv.GaussianBlur(face_roi, (3, 3), 0)

        label, confidence = face_recognizer.predict(face_roi)

        print(f"LABEL: {label}, CONFIDENCE: {confidence}")

        # ---- Confidence Check ---- #
        if confidence < 80:

            # Safety check
            if label >= len(people):
                break

            person = people[label]

            # -------- STUDENT -------- #
            if person["role"] == "student":
                user_data = get_user_data(person["id"])

                if user_data:
                    id, name, year, branch, section, attendance = user_data

                    return jsonify({
                        "role": "student",
                        "id": id,
                        "name": name,
                        "year": year,
                        "branch": branch,
                        "section": section,
                        "attendance": attendance,
                        "weather": weather,
                        "time": time_now,
                        "temp": temp,
                        "quote": quote,
                        "date": date
                    })

            # -------- LECTURER -------- #
            elif person["role"] == "lecturer":
                lecturer_data = get_lecturer_data(person["id"])

                if lecturer_data:
                    id, name, dept, subject, exp = lecturer_data

                    return jsonify({
                        "role": "lecturer",
                        "id": id,
                        "name": name,
                        "department": dept,
                        "subject": subject,
                        "experience": exp,
                        "weather": weather,
                        "time": time_now,
                        "temp": temp,
                        "quote": quote,
                        "date": date
                    })

    # ---- Unknown Case ---- #
    return jsonify({
        "role": "unknown",
        "id": "",
        "name": "Unknown",
        "year": "",
        "branch": "",
        "section": "",
        "attendance": "",
        "weather": weather,
        "time": time_now,
        "temp": temp,
        "quote": quote,
        "date": date
    })


if __name__ == "__main__":
    app.run(debug=True)
