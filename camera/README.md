# Camera application

- `main.py`: Run TCPServer and RTSPServer to sream and wait data from TCPClient
- `tcp_client.py`: Run TCPClient to send data control to TCPServer
- `convert.py`: Convert `.yuv` file to `.mp4` file
- `camera.sh`: Take photo and record

## Install library
```
  sudo apt install git
  sudo apt-get install imagemagick
  sudo apt install gstreamer1.0-rtsp && sudo apt install python3-gst-1.0 && sudo apt install gir1.2-gst-rtsp-server-1.0
  sudo apt install build-essential cmake libopencv-dev  
  sudo apt-get install python3-pip
  sudo apt install libgstrtspserver-1.0-dev
```
