from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
from acmeLib import init
from acmeLib.config import *

def push2AcmeServer(content): 
    try:
        """
        init.DELETE (
            to                      = cseBaseName + '/roboCar/Container/la', 
            originator              = aeOriginator,         
            requestIdentifier       = '123',              
            releaseVersionIndicator = '3',                 
	)
        """

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

net = detectNet("ssd-mobilenet-v2", threshold=0.5)
output = videoOutput("display://0") # this saves a video file with successful object detection if I change to 'file.mp4'
input = videoSource("rtsp://44.203.203.28:8554/mystream", argv=['--input-codec=h264'])

net.SetTrackingEnabled(True)
net.SetTrackingParams(minFrames=3, dropFrames=15, overlapThreshold=0.5)

while True:
    img = input.Capture()

    if img is None: # capture timeout
        continue

    detections = net.Detect(img)
    
    output.Render(img)
    output.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    
    personDetected = False
    for detection in detections:
        if detection.ClassID == 1 and detection.TrackStatus >= 0:
            print("Yey person detected!")
            personDetected = True
            break

    if personDetected:
        push2AcmeServer("carStop")
    else:
        push2AcmeServer("carAutoDrive")    
