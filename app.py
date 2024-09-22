from flask import Flask, Response
from picamera2 import Picamera2
import cv2


app = Flask(__name__)

# size of image
scale_percent = 60 # percent of original size
width = 640
height = 480

# Dummy video source, replace with your actual video source

pts1 = np.array([[width*2/5 - 100, height*1.5/2], [width*3/5 + 100, height*1.5/2], [width*4/5 + 50, width - 170], [width/5 - 50, width - 170 ]], np.int32)
pts1 = pts1.reshape((-1, 1, 2))

pts2 = np.array([[width*2/5 , height/2], [width*3/5 , height/2], [width*3/5 + 100, height*1.5/2],[width*2/5 - 100, height*1.5/2]], np.int32)
pts2 = pts2.reshape((-1, 1, 2))

# print(pts2)
time.sleep(2)
frame = picam2.capture_array()
print(frame)
# picam2.capture_file("app.jpg")
picam2.close()


# def generate_frames():
#     while True:
#         success, frame = video_source.read()
#         dim = (width, height)
#         if not success:
#             break
#         else:
#             cv2.polylines(frame, [pts1], isClosed=True, color=(0, 255, 255), thickness=2)
#             cv2.polylines(frame, [pts2], isClosed=True, color=(0, 255, 0), thickness=2)
#             # cv2.fillPoly(frame, [pts],  color=(0, 255, 0))
            
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#             time.sleep(0.04)
            
        

# @app.route('/')
# def index():
#      return 'image:<br><img src="/video">'

# @app.route('/video')
# def video():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)