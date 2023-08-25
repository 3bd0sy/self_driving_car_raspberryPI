import numpy
import cv2
from flask import Flask, render_template, Response, stream_with_context, request
#from Manuledrivre.motor import s
from AIdrivre.motorModule import motor
from AIdrivre.cameraModule import PIcamera
from AIdrivre.pipeLine import stream

from AIdrivre.edgeDetectionModule import edgeDetection
from AIdrivre.tfliteDetection import objectDetection
from AIdrivre.driveModule import driveOBJ
from VoiceProcessing import extract_command

import json

# video = cv2.VideoCapture(0)
cam=PIcamera()
app = Flask('__name__')
database = {  # add database sqlite
    'username': 'abdo',
    'password': '1234'
}

car=motor()
car.speed(30)
#car.forward(1)
def video_stream():
#     cam=PIcamera(display= not True)
    detect = edgeDetection(display=not True)
    #car=motor()
    drv=driveOBJ(car)
    objectDetect = objectDetection()
    frame_rate_calc=1
    freq = cv2.getTickFrequency()

    while True:
        t1 = cv2.getTickCount()    
        
        frame=stream(cam,detect,car,drv,objectDetect)        
        
        cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
        ret, buffer = cv2.imencode('.jpeg', frame)
        frame = buffer.tobytes()
        yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame + b'\r\n')

        t2 = cv2.getTickCount()
        # Calculate the time elapsed between t1 and t2 in seconds
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            car.stop()
            car.exit()
            break

def video_stream_m():
    while True:
        frame=cam.capture()
        ret, buffer = cv2.imencode('.jpeg', frame)
        frame = buffer.tobytes()
        yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route("/")
def main():
    return render_template('index.html')


@app.route('/form_login', methods=['POST', 'GET'])
def login():
    username = request.form['name']
    password = request.form['pass']
    if username.lower() == database['username'] and password.lower() == database["password"]:
        # return render_template('contant.html', name=username)
        return render_template('home.html')

    else:
        return render_template('index.html')


@app.route('/button', methods=['POST'])
def button():
    # Get JSON data from request
    data = request.get_json()
    # Print button name and value
    btn_name=data['button_name']
    value=data['button_value']
    if btn_name=="up":
        car.forward()
        print("btn UP is clicked")
    
    if btn_name=="down":
        print("btn DOWN is clicked")
        car.backward()

    if btn_name=="left":
        print("btn LEFT is clicked")
        car.left()

    if btn_name=="right":
        print("btn RIGHT is clicked")
        car.right()

    if btn_name in ["_up","_down","_left","_right"]:
        print("car stopped")
        car.stop()

    #print("data:",data['button_name'], data['button_value'])
    # Return JSON response
    return json.dumps(True)


@app.route("/view")
def view():
    return render_template('home.html')


@app.route("/ai_page")
def view_ai():
    
    return render_template('ai_page.html')


@app.route("/settings")
def view_sett():
    return render_template('settings.html')


@app.route("/about")
def view_about():
    return render_template('about.html')


@app.route("/manual_page")
def view_manual():
    return render_template('manual_page.html')


@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    return Response(video_stream_m(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/voice_page")
def voice():
    return render_template('voice_page.html')


@app.route('/upload', methods=['POST'])
def upload():
    # print(request)
    # TODO edit the follwing code to move the car 
    # TODO there was problem with audio format `webm` you should convert it to `wav`

    blob = request.files['blob']
    blob.save('./voice_save/voice1.wav') # or any other format
    comamand=extract_command(blob)

    # if comamand=="forward":
    #     car.forward()
    
    # if btn_name=="backward":
    #     car.backward()

    # if comamand=="left":
    #     car.left()

    # if comamand=="right":
    #     car.right()

    # if comamand in ["_up","_down","_left","_right"]:
    #     print("car stopped")
    #     car.stop()
    return 'OK'

# print("Running on http://your ip:5000/camera")
app.run(host='0.0.0.0', port='5000', debug=not False)# change host on raspberry pi
