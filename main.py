import cv2
import numpy as np
import face_recognition
from WriterReader import *
from Variable import *
from RegSpotted import CameraReg
from FEncode import findEncodings
from FEncode import *
import time
import os
import sys

with open('Counter.csv') as File:
    reader = csv.reader(File, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
    for Count in reader:
        if len(Count) <= 0:
            break
        else:
            print(reader)
            count = str(Count[0])
            print(Count)
            print(count)

for cls in myList:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])
print(classNames)
encodeListKnown = findEncodings(images)

cap = cv2.VideoCapture(0)  # Здесь выставляется ID камеры
print(myList)
while True:

    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(matches)
        print(faceDis)
        matchIndex = np.argmin(faceDis)


        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
        else:#Припиши сюда нонматч
            name = "Unnamed" + count
            ret, frame = cap.read()
            cv2.imwrite(('Known/' + name + '.jpg'), frame)
            images.append(img)
            classNames.append(os.path.splitext(name)[0])
            myList = os.listdir(path)
            print(classNames)
            encodeListKnown = findEncodings(images)
            with open('Counter.csv', 'w') as File:
                writer = csv.writer(File)

                count = str(int(count)+1)
                writer.writerow(count)
            print(myList)



        print(name)
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        CameraReg(name)


    cv2.imshow('Camera',img)
    cv2.waitKey(1)
