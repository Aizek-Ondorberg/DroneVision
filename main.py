import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path ='Known'# в эту папку загружаются лица известных людей, отсюда же НС будет их брать для сравнения
images = [] #Это массив со всеми изображениями
classNames = [] #Это массив со всеми именами
myList = os.listdir(path) #Прогрузка всего занесенного из папки path
print(myList) # Проверка подтверждения регистрации

for cls in myList:# Склейка
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])
print(classNames)

def findEncodings(images):# Это функция для распознавания
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

def CameraReg (name): #Посещаемость, если файл .csv открыть то там будет дата и время, и имя посетителя
    with open ('Spotted.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList =[]
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%D %H:%M:%S')#%H:%M:%S'
            #dtString = now.strftime('%Year:%Month:%Day:%Hour:%Minute:%Seconds')
            f.writelines(f'\n{name},{dtString}')
        #print(myDataList)

#markAttendance('mainlizo')

encodeListKnown = findEncodings(images)
print('Complete')

cap = cv2.VideoCapture(0)# Здесь выставляется ID камеры

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame =  face_recognition.face_encodings(imgS, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img,(x1, y1),(x2,y2),(0, 255, 0),2)
            cv2.rectangle(img, (x1,y2-35), (x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            CameraReg(name)

    cv2.imshow('Camera',img)
    cv2.waitKey(1)