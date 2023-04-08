import os
from PIL import Image
import numpy as np
import cv2
import pickle

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
recog = cv2.face.LBPHFaceRecognizer_create()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "images")

curr_id = 0
label_id = {}
y_labels = []
x_train = []

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith('png') or file.endswith('jpg'):
            path = os.path.join(root, file)
            label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()
            if not label in label_id:
                label_id[label] = curr_id
                curr_id += 1

            id_ = label_id[label]

            pil_img = Image.open(path).convert("L").resize((550,500), Image.LANCZOS)
            
            img_arr = np.array(pil_img, 'uint8')
            faces = face_cascade.detectMultiScale(img_arr)

            for (x,y,w,h) in faces:
                roi = img_arr[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(id_)


with open('labels.pickle', 'wb') as f:
    pickle.dump(label_id, f)

recog.train(x_train, np.array(y_labels))
recog.save('trainer.yml')