#importing all the usefull modules
import cv2 as cv
import face_recognition
import numpy as np
import os
from datetime import datetime
# import csv #to edit csv file
import time
import pyautogui
from tkinter import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials


#making some programs
def wind(textt):
    win = Tk()
    win.geometry("1920x1080")
    win.title("Message for you")
    abel= Label(win, text= f"{textt}", font=('Times New Roman bold',50), justify="center")
    abel.pack(pady=150)
    win.eval('tk::PlaceWindow . center')
    win.mainloop()

def markAttendance(num):
    scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file', 
        'https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name('coder73_apikey.json', scope)
    now = datetime.now()
    client = gspread.authorize(creds)
    sheet = client.open('Attendance').sheet1
    name = 'Dagar'
    sch_num = 'I-1382'
    ftime = now.strftime("%H:%M:%S")
    if num == 1:
        sheet.append_row([name, sch_num, ftime, "Present"])
    elif num == 0:
        sheet.append_row([name, sch_num, ftime, "Absent"])

t_f = []

#learning my face's enc & identifying loc -- means training it...
my_img = face_recognition.load_image_file('my_img.jpg')
my_face_enc = face_recognition.face_encodings(my_img)[0]
my_face_loc = face_recognition.face_locations(my_img)[0]

cap = cv.VideoCapture(0)#using the first webcam out of all

#running loops
for p in range(3):
    while True:
        succes, frame = cap.read()
        frame_res = cv.resize(frame, (1920, 1250))
        frame_res = cv.cvtColor(frame_res, cv.COLOR_BGR2RGB)

        face = face_recognition.face_locations(frame_res)

        #it means, if face is present in current frame save that image otherwise continue...
        if len(face) == 1:
            cv.imwrite(filename=f'img{p}.jpg', img=frame)
        elif len(face) == 0:
            continue

        # cv.imshow("Current frame", frame_res)

        # press_q()
        # if cv.waitKey(1) == ord('q'):
        break#breaking while loop 

    #taking properties of the testing image
    fina_face_img = face_recognition.load_image_file(f'img{p}.jpg')
    face_finally = face_recognition.face_locations(fina_face_img)
    fina_face_enc = face_recognition.face_encodings(fina_face_img)

    #testing/comparing both images...
    matches = face_recognition.compare_faces(my_face_enc, fina_face_enc)
    face_dis = face_recognition.face_distance(my_face_enc, fina_face_enc)

    
    print(matches)
    if matches[0] == True:
        t_f.append(1)
    elif matches[0] == False:
        t_f.append(0)
        
    print(face_dis)

print(t_f)

#my if else ladder...
tf_count = t_f.count(1)
if tf_count >= 2:
    markAttendance(1)
    wind("Your attendance has been marked present!")
elif tf_count <= 1:
    markAttendance(0)
    wind("You have been marked absent")

cap.release()
cv.destroyAllWindows()  