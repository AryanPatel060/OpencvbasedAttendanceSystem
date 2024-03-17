import cv2 
import  numpy as np
import face_recognition
import os
import time
pTime=0
cTime=0
def findencodings(images):
    encodeList  = []
    for img in images:
        img = cv2.cvtColor(img ,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
def add_data_to_file(file_path, data):
    # Read existing content from the file
    try:
        with open(file_path, 'r') as file:
            existing_content = file.read()
    except FileNotFoundError:
        existing_content = ''

    # Check if the data is already in the file
    if data not in existing_content:
        # If not, append the data to the file
        with open(file_path, 'a') as file:
            file.write(data + '\n')
        # print(f'Data "{data}" added to the file.')
    
        # print(f'Data "{data}" already exists in the file.')


path  = "IMG"
images = []
classNames  = []
mylist  = os.listdir(path)
for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

encodeListKnown = findencodings(images)
print('encoding Complete')

cap =cv2.VideoCapture(1)
while True :
    success, img = cap.read()
    # imgs = cv2.resize(img)
    imgs = cv2 .cvtColor(img , cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame  = face_recognition.face_encodings(imgs , facesCurFrame)

    for encodeface,faceLoc in zip(encodeCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown , encodeface )
        faceDist = face_recognition.face_distance(encodeListKnown , encodeface)
        print(faceDist)
        matchIndex =np.argmin(faceDist)

        if matches [matchIndex]:

            name =classNames[matchIndex].upper()
            print (name)
            
            file_path = 'attendance.txt'
            add_data_to_file(file_path, name)

            y1,x2,y2,x1 = faceLoc
            cv2.rectangle(img, (x1,y1),(x2,y2) , (0,255,0),2)
            # cv2.rectangle(imgs, (x1,y1-35),(x2,y2) , (0,255,0),cv2.FILLED)
            cv2.putText(img,name, (x1+6,y1-6) , cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)

    cv2.imshow('webcam' , img)
    cv2.waitKey(1)


