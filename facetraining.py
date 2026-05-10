# pylint:disable=no-member

import os
import cv2 as cv
import numpy as np


people = [
    {"id": "22L31A0433", "role": "student"},   
    {"id": "22L31A0431", "role": "student"},
    {"id": "23L35A0404", "role": "student"},
    {"id": "22L31A0414", "role": "student"},   
]

DIR = r'E:\openCV\people'

haar_cascade = cv.CascadeClassifier('haarcascade.xml')

features = []
labels = []


def augment_face(face):
    augmented = []


    augmented.append(face)


    augmented.append(cv.flip(face, 1))


    augmented.append(cv.convertScaleAbs(face, alpha=1.3, beta=20))
    augmented.append(cv.convertScaleAbs(face, alpha=0.7, beta=-20))


    augmented.append(cv.GaussianBlur(face, (3, 3), 0))


    rows, cols = face.shape
    M1 = cv.getRotationMatrix2D((cols/2, rows/2), 10, 1)
    M2 = cv.getRotationMatrix2D((cols/2, rows/2), -10, 1)

    augmented.append(cv.warpAffine(face, M1, (cols, rows)))
    augmented.append(cv.warpAffine(face, M2, (cols, rows)))

    return augmented


def create_train():
    for person in people:
        path = os.path.join(DIR, person["id"])


        if not os.path.exists(path):
            print(f"⚠️ Folder not found: {path}")
            continue

        label = people.index(person)

        for img in os.listdir(path):
            img_path = os.path.join(path, img)

            img_array = cv.imread(img_path)

            if img_array is None:
                print(f"⚠️ Skipping unreadable image: {img_path}")
                continue 

            gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

            faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 3)


            if len(faces_rect) == 0:
                continue

            for (x, y, w, h) in faces_rect:
                face_roi = gray[y:y+h, x:x+w]
                face_roi = cv.resize(face_roi, (200, 200))


                augmented_faces = augment_face(face_roi)

                for aug_face in augmented_faces:

                    if aug_face is None or aug_face.size == 0:
                        continue

                    features.append(aug_face)
                    labels.append(label)


create_train()

print(f"Training samples: {len(features)}")


if len(features) == 0:
    print("❌ No training data found. Check dataset!")
    exit()

labels = np.array(labels)


face_recognizer = cv.face.LBPHFaceRecognizer_create()

face_recognizer.train(features, labels)


face_recognizer.save('face_trained.yml')


np.save('labels.npy', labels)

print("✅ Model trained successfully with augmentation 🚀")