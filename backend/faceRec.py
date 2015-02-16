﻿#!/usr/bin/env python

import time
import picamera
import picamera.array
import os
import cv2
import numpy as np
import json
import csv
import labels

def savePhoto(pipename):
	with os.open(pipename, os.O_RDONLY|os.O_NONBLOCK) as pipe:
				for line in pipe:
					jsonQuery = json.loads(line)
					print jsonQuery
					

if __name__ == "__main__":
	print "faceRec: start"
	pipename="/tmp/pipe_faceRec"
	if not os.path.exists(pipename):
		os.umask(0)
		os.mkfifo(pipename,0666)
	pipename_fotoin="/tmp/pipe_faceRec"
	if not os.path.exists(pipename_fotoin):
		os.umask(0)
		os.mkfifo(pipename_fotoin,0666)
	pipename_fotoout="/tmp/pipe_faceRec"
	if not os.path.exists(pipename_fotoout):
		os.umask(0)
		os.mkfifo(pipename_fotoout,0666)
	pictureSize=(320,240)
	face_resizeSize=(70,70)
	face_resize = np.empty(face_resizeSize)
	face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/lbpcascades/lbpcascade_frontalface.xml')
	#face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')
	#sexmodel:
	sexmodel = cv2.createFisherFaceRecognizer()
	#[imgs,labels] = csv.readCsv("/home/pi/mirror/bilder/gender.csv")
	[imgs,person_labels,gender_labels, person_dict, gender_dict] = labels.getLabels()
	labels = np.asarray(gender_labels, dtype=np.int32)
	sexmodel.train(np.asarray(imgs), np.asarray(labels))
	#personmodel:
	personmodel = cv2.createFisherFaceRecognizer(threshold=300.0)
	#personmodel = cv2.createEigenFaceRecognizer(threshold=4500.0)
	#personmodel = cv2.createLBPHFaceRecognizer(threshold=100.0)
	#[imgs,labels] = csv.readCsv("/home/pi/mirror/bilder/person.csv")
	labels = np.asarray(person_labels, dtype=np.int32)
	personmodel.train(np.asarray(imgs), np.asarray(labels))
	with picamera.PiCamera() as camera:
		camera.resolution = (640, 480)
		time.sleep(2)
		print "end preperations. start taking pictures"
		with picamera.array.PiYUVArray(camera, size=pictureSize) as output:
			while True:
				savePhoto(pipename_fotoin)
				output.truncate(0)
				camera.capture(output, 'yuv', resize=pictureSize, use_video_port=True)
				gray,u,v = cv2.split(output.array)
				faces = face_cascade.detectMultiScale(image=gray, scaleFactor=1.1, minNeighbors=5, minSize=(40,40))	
				json_transfer = "["
				jsonObjCounter = 0
				for (x,y,w,h) in faces:
					face = gray[y:y+h, x:x+w]
					face_resize = cv2.resize(face, face_resizeSize, face_resize,0,0,cv2.INTER_NEAREST)
					#look for known persons
					[p_label, p_confidence] = personmodel.predict(face_resize)
					if not p_label == -1:
						if jsonObjCounter > 0:
							json_transfer += ","
						json_transfer += json.dumps({"typ":"person","prediction": person_dict["num2person"][p_label],"confidence": p_confidence})
						jsonObjCounter +=1
					else:
						#determine m/w if person is not known
						[g_label, g_confidence] = sexmodel.predict(face_resize)
						if not g_label == -1:
							if jsonObjCounter > 0:
								json_transfer += ","
							json_transfer += json.dumps({"typ":"sex","prediction": gender_dict["num2gender"][g_label],"confidence": g_confidence})
							jsonObjCounter +=1
				json_transfer += "]"
				if not json_transfer == "[]":
					with open(pipename, "w") as pipeout:
						pipeout.write(json_transfer)