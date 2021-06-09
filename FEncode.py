import cv2
import face_recognition


def findEncodings(images):
    encodelist = []
    for img in images:
       img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
       encode = face_recognition.face_encodings(img)[0]
       encodelist.append(encode)
    return encodelist