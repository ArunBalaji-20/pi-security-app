from flask import Flask,render_template,render_template_string,Response
import cv2
import time
import os
import glob

app=Flask(__name__)

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
video_capture = cv2.VideoCapture(0)

def get_most_recent_file():
    # Get list of all files in directory
    directory='C:/Users/Arun balaji/Documents/Projects_and_DEV/Face_detection/images'
    list_of_files = glob.glob(os.path.join(directory, '*'))
    if not list_of_files:
        return None  # Return None if directory is empty

    # Get the most recent file by modification time
    most_recent_file = max(list_of_files, key=os.path.getmtime)
    return most_recent_file[-10:-4]

def image_save(vid):
     timestamp = time.strftime("%Y%m%d-%H%M%S")
     path='C:/Users/Arun balaji/Documents/Projects_and_DEV/Face_detection/images'
     cv2.imwrite(os.path.join(path ,f"screenshot_{timestamp}.png"), vid) 

def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40)) 
    last_file=(get_most_recent_file())# get the last file
    current_timestamp=int(time.strftime("%Y%m%d-%H%M%S")[-6:])
    path='C:/Users/Arun balaji/Documents/Projects_and_DEV/Face_detection/images'
    if last_file!=None:
        if len(faces) > 0 and abs(current_timestamp-int(last_file))>=20:
            image_save(vid)# Save a new screenshot every 60 seconds
            # Save the frame with a timestamp
    if last_file==None:
        image_save(vid)
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces

def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            detect_bounding_box(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/h')
def h():
    return render_template_string('hi')

@app.route('/')
def mainpage():
    return render_template('home.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=='__main__':
    app.run()