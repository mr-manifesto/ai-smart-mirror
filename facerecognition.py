import datetime
import sqlite3 as sq
import numpy as np
import cv2 as cv
import requests
import time

API_KEY = "34203a29fcf570558ee439f048678e5e"
CITY = "Visakhapatnam"

# ---------------- WEATHER FUNCTION ----------------
def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data["cod"] == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return temp, description
    except:
        pass

    return None, None


# ---------------- QUOTE FUNCTION ----------------
def get_quote():
    try:
        url = "https://zenquotes.io/api/random"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data[0]["q"]
    except:
        return "Stay positive and keep building!"


# ---------------- DATABASE FUNCTION ----------------
def get_user_data(user_id):
    con = sq.connect("smartMirror.db")
    cursor = con.cursor()

    cursor.execute("SELECT id, name, year, branch, section, attendence FROM studentInfo WHERE id=?", (user_id,))
    data = cursor.fetchone()

    con.close()
    return data


# ---------------- FACE SETUP ----------------
haar_cascade = cv.CascadeClassifier('haarcascade.xml')

people = [
    {"id": "22L31A0433", "role": "student"},   # label 0
    {"id": "22L31A0431", "role": "student"},   # label 1
    {"id": "001", "role": "lecturer"},         # label 2
    {"id": "002", "role": "lecturer"}          # label 3
]


face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_trained.yml')

cap = cv.VideoCapture(0)

# ---------------- API UPDATE CONTROL ----------------
last_update = 0
update_interval = 300   # 5 minutes

temp = None
desc = ""
quote = ""

# ---------------- MAIN LOOP ----------------
while True:
    isTrue, img = cap.read()
    if not isTrue:
        print("Camera Error")
        break

    img = cv.resize(img, (900, 600))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # ---------------- TIME & DATE ----------------
    now = datetime.datetime.now()
    curr_time = now.strftime("%H:%M:%S")
    curr_date = now.strftime("%d-%m-%Y")

    cv.putText(img, f"Time: {curr_time}", (650,40),
               cv.FONT_HERSHEY_COMPLEX, 0.7, (0,255,255), 2)

    cv.putText(img, f"Date: {curr_date}", (650,70),
               cv.FONT_HERSHEY_COMPLEX, 0.7, (0,255,255), 2)

    # ---------------- UPDATE WEATHER & QUOTE (INTERVAL BASED) ----------------
    current_time_sec = time.time()
    if current_time_sec - last_update > update_interval:
        temp, desc = get_weather()
        quote = get_quote()
        last_update = current_time_sec

    # ---------------- DISPLAY WEATHER ----------------
    if temp:
        cv.putText(img, f"Weather: {desc}", (650,120),
                   cv.FONT_HERSHEY_COMPLEX, 0.6, (255,255,0), 2)

        cv.putText(img, f"Temp: {temp} C", (650,150),
                   cv.FONT_HERSHEY_COMPLEX, 0.6, (255,255,0), 2)

    # ---------------- DISPLAY QUOTE ----------------
    if quote:
        cv.putText(img, "Quote:", (20,500),
                   cv.FONT_HERSHEY_COMPLEX, 0.6, (0,255,0), 2)

        cv.putText(img, quote[:70], (20,530),
                   cv.FONT_HERSHEY_COMPLEX, 0.5, (0,200,0), 1)

    # ---------------- FACE DETECTION ----------------
    faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 4)

    for (x,y,w,h) in faces_rect:
        faces_roi = gray[y:y+h, x:x+w]
        faces_roi = cv.resize(faces_roi, (200, 200))

        label, confidence = face_recognizer.predict(faces_roi)

        if confidence < 80:
            student_id = people[label]
            user_data = get_user_data(student_id)

            if user_data:
                id, name, year, branch, section, attendence = user_data
            else:
                name = "Unknown"
                year = branch = section = attendence = ""
        else:
            name = "Unknown"
            year = branch = section = attendence = ""

        cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        cv.putText(img, str(people[label]), (20,20),
                    cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), thickness=2)

        cv.putText(img, f"Name: {name}", (20,40),
                   cv.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2)

        cv.putText(img, f"Year: {year}", (20,70),
                   cv.FONT_HERSHEY_COMPLEX, 0.6, (0,255,0), 2)

        cv.putText(img, f"Branch: {branch}", (20,100),
                   cv.FONT_HERSHEY_COMPLEX, 0.6, (0,255,0), 2)

        cv.putText(img, f"Section: {section}", (20,130),
                   cv.FONT_HERSHEY_COMPLEX, 0.6, (0,255,0), 2)

        cv.putText(img, f"Attendance: {attendence}", (20,160),
                   cv.FONT_HERSHEY_COMPLEX, 0.6, (0,255,0), 2)

    cv.imshow('AI Smart Mirror', img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()