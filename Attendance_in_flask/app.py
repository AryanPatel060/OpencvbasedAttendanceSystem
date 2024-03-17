from flask import Flask, Response, render_template
import cv2
import  numpy as np
import face_recognition
import os
import time

app = Flask(__name__)

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


path  = "Attendance_in_flask\IMG"
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

camera = cv2.VideoCapture(0)
def gen_frames():  
   while True :
    success, img = camera.read()
    # imgs = cv2.resize(img)
    imgs = cv2 .cvtColor(img , cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame  = face_recognition.face_encodings(imgs , facesCurFrame)

    for encodeface,faceLoc in zip(encodeCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown , encodeface )
        faceDist = face_recognition.face_distance(encodeListKnown , encodeface)
        # print(faceDist)
        matchIndex =np.argmin(faceDist)

        if matches [matchIndex]:

            name =classNames[matchIndex].upper()
            print (name)
            
            file_path = 'Attendance_in_flask/attendance.txt'
            add_data_to_file(file_path, name)

            # y1,x2,y2,x1 = faceLoc
            # cv2.rectangle(img, (x1,y1),(x2,y2) , (0,255,0),2)
            # # cv2.rectangle(imgs, (x1,y1-35),(x2,y2) , (0,255,0),cv2.FILLED)
            # cv2.putText(img,name, (x1+6,y1-6) , cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
    
            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
        

@app.route('/')
def index():
    return render_template('adminpanel.html')

@app.route('/getframe')
def getframe():
    print("hello world")
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')













if __name__ == '__main__':
    app.run(debug=True)
