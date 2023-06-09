ffmpeg -f v4l2 -framerate 30 -video_size 320x240 -i /dev/video0 -pix_fmt yuv420p -preset ultrafast -b:v 10000k  -f rtsp -rtsp_transport tcp rtsp://44.203.203.28:8554/mystream



