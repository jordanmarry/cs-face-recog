import io
import cv2
import pickle
import tkinter as tk
import urllib.request
from PIL import Image, ImageTk
from cs_player.player import player

players = {}
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
recog = cv2.face.LBPHFaceRecognizer_create()

recog.read('trainer.yml')

label = {"person" : 1}
with open('labels.pickle', 'rb') as f:
    labels = pickle.load(f)
    label = {v:k for k,v in labels.items()}

cap = cv2.VideoCapture('./videos/s1mple.mp4')

while 1:

    ret, vid = cap.read()
    gray = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        # roi_color = vid[y:y+h, x:x+w]

        # img_item = "20.png"
        # cv2.imwrite(img_item, roi_color)

        id, conf = recog.predict(roi_gray)

        if label[id] in players:
            players[label[id]] = players[label[id]] + 1
        else:
            players[label[id]] = 1

        cv2.rectangle(vid, (x,y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(vid, label[id] + " " + str(round(conf, 2)), (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255),2)


    cv2.imshow('video', vid)

    # Hold Q button down to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


players = dict(sorted(players.items(), key=lambda item: item[1], reverse=True))
max_num = players[next(iter(players))]
player_info = []
for key, value in players.items():
    if value >= (max_num*.75):
        player_info.append(player(key))

for i in player_info:

    img_url = i.get_photo()
    img_data = urllib.request.urlopen(img_url).read()
    img_pil = Image.open(io.BytesIO(img_data))

    root = tk.Tk()
    root.title(i.get_player_name() + "'s Information")


    frame = tk.Frame(root, padx=20, pady=5)
    frame.pack()

    canvas = tk.Canvas(frame, width=img_pil.width, height=img_pil.height)
    canvas.pack(side="left")
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    info_box = i.get_player_infobox()
    info1 = ""
    for key, value in info_box.items():
        info1 += key + ": " + value + "\n\n"
    text1 = tk.Label(frame, text=info1, anchor="w", justify="left")
    text1.pack(side="right")


    frame2 = tk.Frame(root)
    frame2.pack()

    info2 = i.get_player_info()
    text2 = tk.Label(frame2, text=info2, wraplength=600)
    text2.pack()


    frame3 = tk.Frame(root)
    frame3.pack(fill="both", expand=True)

    achieve = i.get_achieve()
    info3 = "Achievements:\n\n"
    for ach in achieve:
        info3 += str(ach[0]) + " - " + str(ach[1]) +" in " + str(ach[3]) + "\n\n"
    text3 = tk.Label(frame3, text=info3, wraplength=800, anchor="w", justify="left")
    text3.pack(side="left", padx=50)

    history = i.get_history()
    info4 = "History:\n\n"
    for key, value in history.items():
        info4 += value + " playing for " + key + "\n\n"

    text4 = tk.Label(frame3, text=info4, wraplength=800, anchor="e", justify="right")
    text4.pack(side="right", padx=50)

    root.mainloop()