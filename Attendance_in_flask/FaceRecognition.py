import cv2
import face_recognition
import numpy as np 

img = face_recognition.load_image_file('IMG/elon-musks.jpg')
img  = cv2.cvtColor(img  , cv2.COLOR_BGR2RGB)
imgtest = face_recognition.load_image_file('IMG/elon-musks_test.jpg')
imgtest  = cv2.cvtColor(imgtest  , cv2.COLOR_BGR2RGB)


faceloc = face_recognition.face_locations(img)[0]
encode = face_recognition.face_encodings(img)[0]
cv2.rectangle(img , (faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]),(255,0,255) , 2 )

faceloctest = face_recognition.face_locations(imgtest)[0]
encodetest = face_recognition.face_encodings(imgtest)[0]
cv2.rectangle(imgtest , (faceloctest[3],faceloctest[0]),(faceloctest[1],faceloctest[2]),(255,0,255) , 2 )

face_recognition.compare_faces([encode],encodetest)

cv2.imshow('img', img)
cv2.imshow('imgtest', imgtest)

cv2.waitKey(0)

