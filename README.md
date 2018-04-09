# Joseph Reger Detector on a Raspberry Pi

Example of using a learning model to recognise faces, using Apeigey face 
recognition python library and [dlib](http://dlib.net/)'s face 
recognition library using deep learning.

## Installation

### Requirements

 * Raspberry Pi with Camera (only tested on Pi Zero W)
 * Python 3
 * Flask 
 * Dlib
 * Recognition Python library 
 
### Setup Raspberry Pi

 * Download and Setup Raspberry Pi and connect to wireless network by following the instructions [here](https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65).  This will setup Dlib and Face Recognition libraries
 * Fix the missing library
 ```bash
sudo apt-get install libatlas-base-dev
```
 * Install flask 
 ```bash
 pip3 install Flask
 ```
 * Download the example
 ```bash
git clone --single-branch https://github.com/drffej/josephdetector
```

 ## Usage
 
 Run the example via the command
 
 ```bash
 cd josephdetector
 python3 josephdetector.py
 ```
 
After a few minutes this will run a web server 
 
 ```bash
Starting detector and loading libraries
Loading known face image(s)
Jeff and Joseph images loaded.
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 ```
 
 Open a browser session to the URL (or whatever name the pi is called)
  
 ```bash
 http://raspberrypi:5000/video_feed
 ```
