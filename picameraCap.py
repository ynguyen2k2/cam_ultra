from flask import Flask, render_template, Response
from picamera2 import Picamera2, Preview
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
import io

app = Flask(__name__)

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

def gen():
    stream = io.BytesIO()
    encoder = JpegEncoder()
    output = FileOutput(stream)
    while True:
        # Capture a frame
        picam2.capture_file(output)
        
        # Stream the frame
        stream.seek(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')
        stream.seek(0)
        stream.truncate()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)