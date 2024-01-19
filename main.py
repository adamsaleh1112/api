from flask import Flask, request, render_template, jsonify, Response  # importing flask to allow for creation of api webserver
# from adafruit_motorkit import MotorKit  # motorkit library to allow for motor function on robot
from time import sleep  # time library allows sleep function, which pauses code to allow for rests
import cv2
import numpy as np
from overlay import video_overlay

# tank = MotorKit(0x40)  # setting the variable tank to a 0x40 gpio board
app = Flask(__name__)  # assigning api name
camera = cv2.VideoCapture(0)


def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/")  # main route that will display the html
def index():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/overlay")
def overlay():
    return Response(video_overlay(), mimetype='multipart/x-mixed-replace; boundary=frame')


#
# @app.route("/stop", methods=['POST'])  # main route that will display the html
# def stop():  # stops any movement for any movement function
#     tank.motor1.throttle = 0
#     tank.motor2.throttle = 0
#     return jsonify({'status': 'error', 'message': 'Invalid command'})  # function must end in a return command
#
#
# @app.route("/forward", methods=['POST'])  # main route that will display the html
# def forward():  # stops any movement for any movement function
#     tank.motor1.throttle = 0.75 * -1
#     tank.motor2.throttle = 0.75 + 0.069
#     return jsonify({'status': 'error', 'message': 'Invalid command'})  # function must end in a return command
#
#
# @app.route("/backward", methods=['POST'])  # main route that will display the html
# def backward():  # stops any movement for any movement function
#     tank.motor1.throttle = 0.75
#     tank.motor2.throttle = (0.75 + 0.0665) * -1
#     return jsonify({'status': 'error', 'message': 'Invalid command'})  # function must end in a return command
#
#
# @app.route("/left", methods=['POST'])  # main route that will display the html
# def left():  # stops any movement for any movement function
#     tank.motor1.throttle = 0.75 * -1
#     tank.motor2.throttle = (0.75 + 0.069) * -1
#     return jsonify({'status': 'error', 'message': 'Invalid command'})  # function must end in a return command
#
#
# @app.route("/right", methods=['POST'])  # main route that will display the html
# def right():  # stops any movement for any movement function
#     tank.motor1.throttle = 0.75 * 1
#     tank.motor2.throttle = (0.75 + 0.069) * 1
#     return jsonify({'status': 'error', 'message': 'Invalid command'})  # function must end in a return command
#
#
# @app.route("/go", methods=['POST'])  # main route that will display the html
# def go():  # stops any movement for any movement function
#     def forward(throttle, time):
#         tank.motor1.throttle = throttle * -1
#         tank.motor2.throttle = throttle + 0.069
#         sleep(time)
#         tank.motor1.throttle = 0.0
#         tank.motor2.throttle = 0.0
#
#     def left90(throttle):
#         tank.motor1.throttle = throttle * -1
#         tank.motor2.throttle = (throttle + 0.069) * -1
#         sleep(1.195)
#         tank.motor1.throttle = 0.0
#         tank.motor2.throttle = 0.0
#
#     def reverse(throttle, time):
#         tank.motor1.throttle = throttle
#         tank.motor2.throttle = (throttle + 0.0665) * -1
#         sleep(time)
#         tank.motor1.throttle = 0.0
#         tank.motor2.throttle = 0.0
#
#     forward(0.75, 4.8)
#     sleep(0.2)
#     left90(0.75)
#     sleep(0.2)
#     forward(0.75, 3.4)
#     sleep(0.2)
#     reverse(0.75, 5.8)
#
#     return jsonify({'status': 'error', 'message': 'Invalid command'})  # function must end in a return command
#

if __name__ == "__main__":  # runs api
    app.run(host='0.0.0.0', port=5000)  # gives the webserver the port :5000
