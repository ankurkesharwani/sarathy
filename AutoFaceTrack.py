################################################################################
#
#       Auto Face Track Algorithim
#      ============================
#
#       @Author: Ankur Kesharwani
#
#       The following program tracks a users face and prints the actions
#       made by the user's head such as, Up, Down, Left & Right.
#
################################################################################

import cv2
import cv2.cv as cv
import numpy as np
import time

import socket
import sys

#
# The following function detects a user's face in the scene captured
# by the default capture device. It then returns the image of the
# face along with a Window enclosing the face.
#
# The following algo is based on OpenCV's HAAR Cascade Classifier.
#
def DetectFaces():
		
	# The window enclosing the face.
	track_window=None
	# The image containing the captured face.
	frame=None
	# Let the camera initialize by capturing some frames.
	print 'Initializing'
	for i in range (1,10):
		ret, frame=video_stream.read()
		print '.'
	# Now we are ready to capture the face.
	while(True):
		# Read video frame.
		ret, frame=video_stream.read()
		# Convert it to gray scale.
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# Detect face using HAAR Cascade Algorithm.
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		# For every face detected select the last one.
		for (x,y,w,h) in faces:
			track_window=(x,y,w,h)
		if(len(faces)>0):
			cv2.destroyAllWindows()
			break
				
	# Return the track window and frame nicely packed in a tupple.
	return (track_window,frame)        

#
# The following function connects to the UInputServer at localhost.
# The UInputServer is the component that performs Input Injection thus
# acting as a user created input device.
#
def connectServer(host="127.0.0.1"):
	s = socket.socket()         # Create a socket object
	host = socket.gethostname() # Get local machine name
	port = 4444
	s.connect((host, port))
	return s

#
# The following function sends key strokes based on the state of the 
# RTN. The state is determined by the new and old states.
#
def sendCommand(s, newState):
	#Send key strokes based on state of the RTN.
	if(newState=="Up"):
		s.send("KPR_103")
	elif(newState=="Left"):
		s.send("KPR_106")
	elif(newState=="Right"):
		s.send("KPR_105")
	elif(newState=="Down"):
		s.send("KPR_108")

def disconnect(s):
	s.close()

if __name__=="__main__":

	# Connect to UInput Server.
	server=connectServer()

	# Load HAAR Cascades for processing.
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')

	# Variables to keep track of head movements.
	curr_X,curr_Y=(0,0)
	min_X, max_X, min_Y, max_Y = (0,0,0,0)
	gesture = None
	state = None
		
	# Set out video source to the default camera attached to computer.
	video_stream=cv2.VideoCapture(0)

	# Check if video stream is opened. If not, open it.
	if(video_stream.isOpened()==False):
		video_stream.open()

	# Detect faces.
	track_window,frame=DetectFaces()

	# Extract co-ordinates of face from track window tupple.
	f_x,f_y,f_w,f_h=track_window

	min_X=f_w/2 - f_w/6
	max_X=f_w/2 + f_w/6
	min_Y=f_h/2 - f_w/8
	max_Y=f_h/2 + f_w/8

	#
	#               Code for Gesture Recognition.
	#             =================================
	#
	# The following recognizes basic gestures made by head of the user.
	# The gestures recognized are Up, Down, Left and Right.
	#
	# The following algo uses the center of the nose as reference point
	# on the face.
	#
	# To increase computational efficiency, the algo clips the rectangular
	# bound around the recognized face and all processing is done in this
	# rectangular bound.
	#
	while(True):

		# Read a single frame from camera.
		ret, frame=video_stream.read()

		# Extract a region of interest.
		roi=frame[f_y:f_y+f_h,f_x:f_x+f_w]

		# Convert it to grey scale.
		gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
		# Extract the nose from face.
		nose = nose_cascade.detectMultiScale(gray, 1.3, 5)
		# For every nose detected select the last one and calculate
		# the center. Also draw bounds around the nose and a center
		# inside it. 
		for (n_x,n_y,n_w,n_h) in nose:
			#cv2.rectangle(roi,(n_x,n_y),(n_x+n_w,n_y+n_h),(255,0,0),1)
			cv2.circle(roi, (n_x+n_w/2+2,n_y+n_h/2+2),4,(0,0,255),-1)
			curr_X=n_x+n_w/2
			curr_Y=n_y+n_h/2

		cv2.rectangle(roi,(min_X,min_Y),(max_X, max_Y),(255,255,0),2)
		if(curr_X>min_X and curr_X>max_X):
			gesture = 'Right'
		elif(curr_X<min_X and curr_X<max_X):
			gesture = 'Left'
		if(curr_Y>min_Y and curr_Y>max_Y):
			gesture = 'Down'
		elif(curr_Y<min_Y and curr_Y<max_Y):
			gesture = 'Up'

		if(curr_X>min_X and curr_X<max_X and curr_Y>min_Y and curr_Y<max_Y):
			gesture = 'Neutral'
		if(state != gesture):
			state = gesture
			print state
			sendCommand(server, state)
					
		#Show the video feed in a nice window.
		cv2.imshow('Saarthy',roi)
		cv2.moveWindow("Saarthy", 850, 50);
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyAllWindows
			break
