import RPi.GPIO as GPIO
import time
from flask import Flask,request,render_template , Response
import os
import sys
import Adafruit_DHT as dht
from camera_pi import Camera
from picamera import PiCamera
from pushbullet import Pushbullet


API_KEY = '<ENTER API KEY HERE>'
pb=Pushbullet(API_KEY)
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

servoPIN=22
motionPIR=24
buzzer=23
ledRed = 17
ledYlw = 27
senTMP = 4
ledRedSts = 0
ledYlwSts = 0
GPIO.setup(24, GPIO.IN)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(servoPIN,GPIO.OUT)
GPIO.setup(ledRed,GPIO.OUT)
GPIO.output(ledRed,GPIO.LOW)
GPIO.setup(ledYlw,GPIO.OUT)
GPIO.output(ledYlw,GPIO.LOW)
p=GPIO.PWM(servoPIN,50)
@app.route("/")

def index():
	try:
		ledRedSts = GPIO.input(ledRed)
		ledYlwSts = GPIO.input(ledYlw)

		templateData = {
			'title' : 'GPIO output Status!',
			'ledRed' : ledRedSts ,
			'ledYlw' : ledYlwSts ,
			}

		return render_template('index.html',**templateData)

	except KeyboardInterrupt:
		GPIO.cleanup()

	exit
@app.route("/<deviceName>/<action>")

def action(deviceName,action):
	temperature = ''
	humidity = ''
	if deviceName == 'ledRed':
		actuator = ledRed
		if action == 'on':
			GPIO.output(actuator,GPIO.HIGH)
		if action == 'off':
			GPIO.output(actuator,GPIO.LOW)
	if deviceName == 'ledYlw':
		actuator = ledYlw
		if action == 'on':
			GPIO.output(actuator,GPIO.HIGH)
		if action == 'off':
			GPIO.output(actuator,GPIO.LOW)

	ledRedSts = GPIO.input(ledRed)
	ledYlwSts = GPIO.input(ledYlw)

	if deviceName == 'senTMP' and action == 'get':

		humi, temp = dht.read_retry(dht.DHT22, 4)
		humi = '{0:0.1f}' .format(humi)
		temp = '{0:0.1f}' .format(temp)
		temperature = temp
		humidity =  humi

	if deviceName == 'servoPIN':

		if action == 'on':
			p.start(0)
			for i in range (100,0,-10):
				p.ChangeDutyCycle(6.5)
				time.sleep(0.02)
				p.ChangeDutyCycle(0)
				time.sleep(0.2)
		if action == 'off':
			p.start(0)
			for i in range (0,100,10):
				p.ChangeDutyCycle(0.01)
				time.sleep(0.02)
				p.ChangeDutyCycle(0)
				time.sleep(0.2)

	if deviceName == 'motionPIR':
		time.sleep(2)
		while True:
			if action == 'on':
				if GPIO.input(24):
					GPIO.output(23, True)
					time.sleep(0.5)
					GPIO.output(23, False)
					capture()
					pb.push_note("Alert!","Motion Detected!")
					pushimage()
					time.sleep(5)
				time.sleep(0.1)
			if action == 'off':
				GPIO.output(23, False)
	templateData = {
		'ledRed' : ledRedSts,
		'ledYlw' : ledYlwSts,
		'temperature' : temperature,
		'humidity' : humidity,
		}

	return render_template('index.html',**templateData)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')

def video_feed():
		return Response(gen(Camera()),
		mimetype='multipart/x-mixed-replace; boundary=frame')

def capture():
	camera = PiCamera()
	camera.rotation = 180
	camera.start_preview()
	time.sleep(2)
	camera.capture('image.jpg')
	camera.stop_preview()

def pushimage():
	with open("image.jpg","rb") as pic:
		fileData=pb.upload_file(pic,"image.jpg")

	pb.push_file(**fileData)

if __name__ == "__main__":
	app.run(host="0.0.0.0" , debug=True , threaded = True)


