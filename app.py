from flask import Flask, Response
import cv2
import time
import numpy as np
# import GPIO
# import ultrasensor

#GPIO Mode (BOARD / BCM)
# GPIO.setmode(GPIO.BCM)
 
# #set GPIO Pins
# GPIO_TRIGGER = 18
# GPIO_ECHO = 24
 
# #set GPIO direction (IN / OUT)
# GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
# GPIO.setup(GPIO_ECHO, GPIO.IN)

app = Flask(__name__)

# size of image
scale_percent = 60 # percent of original size
width = 640
height = 480

# Dummy video source, replace with your actual video source
video_source = cv2.VideoCapture(0)
height 
pts1 = np.array([[width*2/5 - 100, height*1.5/2], [width*3/5 + 100, height*1.5/2], [width*4/5 + 50, width - 170], [width/5 - 50, width - 170 ]], np.int32)
pts1 = pts1.reshape((-1, 1, 2))

pts2 = np.array([[width*2/5 , height/2], [width*3/5 , height/2], [width*3/5 + 100, height*1.5/2],[width*2/5 - 100, height*1.5/2]], np.int32)
pts2 = pts2.reshape((-1, 1, 2))

print(pts2)



def generate_frames():
    while True:
        success, frame = video_source.read()
        dim = (width, height)
        if not success:
            break
        else:
            cv2.polylines(frame, [pts1], isClosed=True, color=(0, 255, 255), thickness=2)
            cv2.polylines(frame, [pts2], isClosed=True, color=(0, 255, 0), thickness=2)
            # cv2.fillPoly(frame, [pts],  color=(0, 255, 0))
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.04)
            
        

@app.route('/')
def index():
     return 'image:<br><img src="/video">'

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)