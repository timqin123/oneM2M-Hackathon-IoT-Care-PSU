
from flask import Flask, render_template, Response, request, redirect, url_for


import threading
import argparse
import datetime

import time
import cv2
import sys
sys.path.append("..")
from acmeLib import init
from acmeLib.config import *



app = Flask(__name__)
camera = cv2.VideoCapture(f"rtsp://44.203.203.28:8554/mystream")
#camera = cv2.VideoCapture(0)                      
def retrieve():
     init.RETRIEVE (   
         to                      = cseBaseName,
         originator              = defaultOriginator,
         requestIdentifier       = '123',
         releaseVersionIndicator = '3',
     )

def push2AcmeServer(content): 
 	try:

		
 		init.DELETE (
 		    to                      = cseBaseName + '/roboCar/Container/la', 
 		    originator              = aeOriginator,         
 		    requestIdentifier       = '123',              
 		    releaseVersionIndicator = '3',                 
 		)
	
 		init.CREATE (
 		    to                      = cseBaseName + '/roboCar/Container', 
 		    originator              = aeOriginator, 
 		    requestIdentifier       = '123', 
 		    releaseVersionIndicator = '3',
 		    resourceType            = init.Type.ContentInstance,
 		    primitiveContent = 
 			{
 			    'm2m:ContentInstance': {
 				'contentInfo': 'text/plain:0',              
 				'content': content              
 			    }
 			}
 		)
 	except Exception:
 		print("Error while writing to ACME server")

@app.route("/", methods=["GET","POST"])
def index():
    return render_template('index.html')

def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)

#====
#CAR
#====        
@app.route("/carForward/", methods=['POST'])
def carForward():
    content = "carForward"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

@app.route("/carBackward/", methods=['POST'])
def carBackward():
    content = "carBackward"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

@app.route("/carLeft/", methods=['POST'])
def carLeft():
    content = "carLeft"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

@app.route("/carRight/", methods=['POST'])
def carRight():
    content = "carRight"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

@app.route("/carAccelerate/", methods=['POST'])
def carAccelerate():
    content = "carAccelerate"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

@app.route("/carDecelerate/", methods=['POST'])
def carDecelerate():
    content = "carDecelerate"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

@app.route("/carAutoDrive/", methods=['POST'])
def carAutoDrive():
    content = "carAutoDrive"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

@app.route("/carStop/", methods=['POST'])
def carStop():
    content = "carStop"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

#=============
# ROBOTIC ARM
#=============

@app.route("/servoALeft/", methods=['POST'])
def servoALeft():
    content = "servoALeft"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

@app.route("/servoARight/", methods=['POST'])
def servoARight():
    content = "servoARight"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

@app.route("/servoBUp/", methods=['POST'])
def servoBUp():
    content = "servoBUp"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

@app.route("/servoBDown/", methods=['POST'])
def servoBDown():
    content = "servoBDown"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

@app.route("/servoCUp/", methods=['POST'])
def servoCUp():
    content = "servoCUp"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

@app.route("/servoCDown/", methods=['POST'])
def servoCDown():
    content = "servoCDown"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

@app.route("/servoDForward/", methods=['POST'])
def servoDForward():
    content = "servoDForward"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);

@app.route("/servoDBackward/", methods=['POST'])
def servoDBackward():
    content = "servoDBackward"
    push2AcmeServer(content)
    return render_template('index.html', forward_message=content);
