#!/usr/bin/env python
# Joeseph Detector
# (c) 2018 Jeff Parker   
#
# Based on code and ideas from Adam Geity and Davis King
#
# See LICENCE

print("Starting detector and loading libraries")

from importlib import import_module
import os
import time
from flask import Flask, render_template, Response
from PIL import Image, ImageDraw
from io import BytesIO
import face_recognition
import numpy as np

from picamera import PiCamera


# initalise pi camera
camera = PiCamera()
camera.resolution = (320, 240)
time.sleep(1)
output = np.empty((240, 320, 3), dtype=np.uint8)

# load sample pictures and learn how to recognise it
print("Loading known face image(s)");
jeff_image = face_recognition.load_image_file("images/Jeff.jpg")
jeff_face_encoding = face_recognition.face_encodings(jeff_image)[0]
joseph_image = face_recognition.load_image_file("images/joseph.jpg")
joseph_face_encoding = face_recognition.face_encodings(joseph_image)[0]
print("Jeff and Joseph images loaded.")

# save faces in arrays
known_face_encodings = [
	jeff_face_encoding,
	joseph_face_encoding
]
known_face_names = [
	"Jeff",
	"Joseph"
]


app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
	"""Video streaming generator function."""

	# initialise some variables
	frame_count = 0;
	bytes_io = BytesIO()
	skip_frame = 1; 
	face_names = []
	face_locations = []

	while True:
		print("Capturing image.")
		camera.capture(output, format="rgb")
		im = Image.fromarray(output,'RGB')

		# process every other frame to speed up
		if frame_count > skip_frame:
			
			# reset
			frame_count = 0;

			# find face locations on captured image
			face_locations = face_recognition.face_locations(output)
			print("Found {} faces in image.".format(len(face_locations)))
		
			# find faces on captured image
			face_encodings = face_recognition.face_encodings(output,face_locations)

			# match up with saved faces
			face_names = []
			for face_encoding in face_encodings:
				# see of face is a match
				matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
				name = "Unknown"

				# match found add to know list of face names
				if True in matches:
					first_match_index = matches.index(True)
					name = known_face_names[first_match_index]
					print("I see someone names {}!".format(name))

				face_names.append(name)


		# blat out results on image with bounding box and name
		draw = ImageDraw.Draw(im)
		for (top, right, bottom, left), name in zip(face_locations,face_names):
			text_width, text_height = draw.textsize(name)
			draw.rectangle(((left, bottom ), (right, top)), outline=(0, 0, 255))
			draw.rectangle(((left, bottom + text_height + 10), (right, bottom)), fill=(0,0,255), outline=(0, 0, 255))
			draw.text((left + 6, bottom + text_height - 5), name, fill=(255, 255, 255, 255))

		# flip frame
		frame_count = frame_count + 1

		# convert to PNG string object
		bytes_io.seek(0)
		im.save(bytes_io, 'PNG')
		im.close()

		# send image to browser
		yield (b'--frame\r\n'
		       b'Content-Type: image/png\r\n\r\n' + bytes_io.getvalue() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
