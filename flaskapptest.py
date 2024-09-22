from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import numpy as np
import math

### You can donate at https://www.buymeacoffee.com/mmshilleh 

width = 800
height = 600
# red
pts1 = np.array([[width/5 - 50,height ], [width*2/5 - 100, height*1.5/2 + 40 ], [width*3/5 + 100, height*1.5/2 +40], [width*4/5 + 50, height]], np.int32)
pts1 = pts1.reshape((-1, 1, 2))
# line 1 red
line_red_start1_y = height - ((height -  (height*1.5/2 + 40))/2)
line_red_start1_x =(width*2/5 - 100) - (width/5 - 50) /2 
line_red_start1 = (int(line_red_start1_x),int(line_red_start1_y))
line_red_end1 = ( int(line_red_start1_x) + 100,int(line_red_start1_y))

# line 2 red 
line_red_start2_x =((width*4/5 + 50) - (width*3/5 + 100)) /2  + (width*3/5 + 100)
line_red_start2 = (int(line_red_start2_x),int(line_red_start1_y))
line_red_end2 = ( int(line_red_start2_x) - 100,int(line_red_start1_y))


# green
pts2 = np.array([[width*2/5 - 30, height*1.5/2-30],[width*2/5+10 , height/2 + 80], [width*3/5-10  , height/2 + 80], [width*3/5 + 30, height*1.5/2-30]], np.int32)
# pts2 = np.array([[width*2/5+10 , height/2 + 80], [width*3/5-10  , height/2 + 80], [width*3/5 + 30, height*1.5/2-30],[width*2/5 - 30, height*1.5/2-30]], np.int32)
pts2 = pts2.reshape((-1, 1, 2))

# line 1 green
line_green_start1_y =  ((height*1.5/2-30 -  (height/2 + 80))/2) + (height/2 + 80)
line_green_start1_x =((width*2/5+10) - (width*2/5 - 30) )/2 + (width*2/5 - 30)
line_green_start1 = (int(line_green_start1_x),int(line_green_start1_y))
line_green_end1 = ( int(line_green_start1_x) + 30 ,int(line_green_start1_y))

# line 2 green 
line_green_start2_x =((width*3/5 + 30) - (width*3/5-10 )) /2  + (width*3/5-10 )
line_green_start2 = (int(line_green_start2_x),int(line_green_start1_y))
line_green_end2 = ( int(line_green_start2_x) - 30,int(line_green_start1_y))

# yellow
pts3 = np.array([[width*2/5 - 100, height*1.5/2 + 40 ], [width*2/5 - 30, height*1.5/2-30], [width*3/5 + 30, height*1.5/2-30], [width*3/5 + 100, height*1.5/2 +40]], np.int32)
pts3 = pts3.reshape((-1, 1, 2))

# line 1 yellow
line_yellow_start1_y =  ((height*1.5/2 + 40 -  (height*1.5/2-30))/2) + (height*1.5/2-30)
line_yellow_start1_x =((width*2/5 - 30) - (width*2/5 - 100) )/2 + (width*2/5 - 100)
line_yellow_start1 = (int(line_yellow_start1_x),int(line_yellow_start1_y))
line_yellow_end1 = ( int(line_yellow_start1_x) + 60 ,int(line_yellow_start1_y))

# line 2 yellow 
line_yellow_start2_x =((width*3/5 + 100) - (width*3/5 + 30)) /2  + (width*3/5 + 30)
line_yellow_start2 = (int(line_yellow_start2_x),int(line_yellow_start1_y))
line_yellow_end2 = ( int(line_yellow_start2_x) - 60,int(line_yellow_start1_y))

app = Flask(__name__)

camera = Picamera2()
camera.video_configuration.controls.FrameRate = 25.0
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (width, height)}))
camera.start()

@app.route('/')
def index():
     return '<meta name="viewport" content="width=device-width, initial-scale=1">image:<br><img src="/video">'

def generate_frames():
    while True:
        frame = camera.capture_array()
        cv2.polylines(frame, [pts1], isClosed=True, color=(0, 0, 255), thickness=2)
        cv2.line(frame, line_red_start1, line_red_end1, color=(0, 0, 255), thickness=2)
        cv2.line(frame, line_red_start2, line_red_end2, color=(0, 0, 255), thickness=2)

        cv2.polylines(frame, [pts2], isClosed=False, color=(0, 255, 0), thickness=2)
        cv2.line(frame, line_green_start1, line_green_end1, color=(0, 255,0 ), thickness=2)
        cv2.line(frame, line_green_start2, line_green_end2, color=(0, 255, 0), thickness=2)

        cv2.polylines(frame, [pts3], isClosed=False, color=(0, 255, 255), thickness=2)
        cv2.line(frame, line_yellow_start1, line_yellow_end1, color=(0, 255, 255), thickness=2)
        cv2.line(frame, line_yellow_start2, line_yellow_end2, color=(0, 255, 255), thickness=2)

        # cv2.fillPoly(frame, [pts2],  color=(255, 0, 0))
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)