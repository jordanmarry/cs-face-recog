import cv2
import numpy as np
import pickle

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
recog = cv2.face.LBPHFaceRecognizer_create()

recog.read('trainer.yml')

label = {"person" : 1}
with open('labels.pickle', 'rb') as f:
    labels = pickle.load(f)
    label = {v:k for k,v in labels.items()}

cap = cv2.VideoCapture('./videos/s1mple_zywoo.mp4')

while 1:

    ret, vid = cap.read()
    gray = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = vid[y:y+h, x:x+w]

        img_item = "10.png"
        cv2.imwrite(img_item, roi_color)

        id, conf = recog.predict(roi_gray)

        cv2.rectangle(vid, (x,y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(vid, label[id] + " " + str(round(conf, 2)), (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255),2)


    cv2.imshow('video', vid)

    # Hold Q button down to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()