from flask import Flask, Response
from picamera2 import Picamera2
import cv2


app = Flask(__name__)

# cau hinh picamera
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()
#  tạo một thẻ image để hiện thi video
@app.route('/')
def index():
     return 'image:<br><img src="/video">'
#  hàm tạo frame lấy từ picamera 
def generate_frames():
    while True:
        # đọc image từ picamera 
        frame = camera.capture_array()
        # chuyen image thành memorry buffer
        ret, buffer = cv2.imencode('.jpg', frame)
        
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)