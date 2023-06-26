from flask import Flask, render_template, Response,request
import cv2
from camera import VideoCamera_tamil,VideoCamera_hindi
from camera_eng import VideoCamera
import cv2
import atexit
app = Flask(__name__,template_folder="templates",static_url_path='/static')


videoCamera=VideoCamera()
videoCamera_tamil=VideoCamera_tamil()
videoCamera_hindi=VideoCamera_hindi()

def switch_off_camera():
    videoCamera.release_camera()
    videoCamera_tamil.release_camera()
    videoCamera_hindi.release_camera()

def generate_frames():
    while True:
        frame = videoCamera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def generate_frames_tamil():
    while True:
        frame= videoCamera_tamil.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def generate_frames_hindi():
    while True:
        frame= videoCamera_hindi.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')





@app.route('/video_feed')
def video_feed():
    switch_off_camera()

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_tamil')
def video_feed_tamil():
    switch_off_camera()
    return Response(generate_frames_tamil(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_hindi')
def video_feed_hindi():
    switch_off_camera()
    return Response(generate_frames_hindi(), mimetype='multipart/x-mixed-replace; boundary=frame')






@app.route('/')
def index():
    cap = cv2.VideoCapture(0)
    cap.release()
    return render_template('index.html')

@app.route('/About')
def about():
    switch_off_camera()
    return render_template('about.html')

@app.route("/Privacy Policy")
def privacypolicy():
    switch_off_camera()
    return render_template('privacy_policy.html')


@app.route("/Conversion")
def conversion():
    return render_template('conversion.html')

@app.route("/tamil_translation")
def tamil_conversion():
    return render_template('conversion_tamil.html')


@app.route("/hindi_translation")
def hindi_conversion():
    return render_template('conversion_hindi.html')

@app.route("/english_translation")
def english_conversion():
    return render_template('conversion.html')




@app.route("/how_works")
def howworks():
    switch_off_camera()
    return render_template('how_works.html')

@app.route("/why_sign_language")
def whysign():
    switch_off_camera()
    return render_template('y_sign.html')


if __name__ == "__main__":
    app.run(debug=True)


