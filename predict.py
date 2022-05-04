import os
import cv2
import tensorflow as tf
import numpy

model = tf.keras.models.load_model('male_female_classifier.h5')
#https://www.kaggle.com/agnishwarbagchi/male-female-classifier/notebook

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81

IMG_SIZE = 100
path = 'media/'

def predict(img_name):
    img = cv2.imread(os.path.join(path, img_name))
    img_array = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_array, 1.1, 4)

    genders = []
    scores = []

    for (x,y,w,h) in faces:
        crop = img_array[y:y+h, x:x+w]
        crop = cv2.resize(crop, (IMG_SIZE, IMG_SIZE))
        crop= crop.reshape(-1,IMG_SIZE, IMG_SIZE,1)
        score = model.predict(crop)[0][0]
        gender = "Male" if score<=0.5 else "Female"

        scores.append(score)
        genders.append(gender)

        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 4)
        cv2.putText(img, gender, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 6)

    filename = path+'predict.jpg'
    cv2.imwrite(filename, img)