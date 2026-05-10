import cv2 as cv

haar_cascade = cv.CascadeClassifier('haarcascade.xml')

cap = cv.VideoCapture(0)

while True:
    isTrue, img = cap.read()
    if not isTrue:
        print("Unable to detect face")
        break

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)


    for (x,y,w,h) in faces_rect:
        cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0), thickness=2)


    cv.imshow('Detected Faces', img)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

print(f'Number of faces found = {len(faces_rect)}')
cv.waitKey(0)
cap.release()

