#run test3 and page3 to work!!

# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import imutils
import time
import dlib
import cv2
import numpy as np
import requests
import base64
import json
from PIL import Image
import io

def equal():
	for i in range(140):		
		print('=', end='')
	print("\n")

def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))

# convert PIL Image to an RGB image( technically a numpy array ) that's compatible with opencv
def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
vs = VideoStream(0,framerate=2).start()
time.sleep(2.0)


# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream, resize it to
	# have a maximum width of 400 pixels, and convert it to
	# grayscale

	frame = vs.read()
	"""img = Image.fromarray(frame,mode='RGB')
	frame_1 = toRGB(img)
	img.show()



	image_string = base64.b64encode(frame_1)
	image_string = str(image_string)
	text_file = open("Output.txt", "w")
	text_file.write(image_string)
	text_file.close()"""


	frame = imutils.resize(frame, width=400)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#save image
	#cv2.imwrite("temp.jpg", gray)
	cv2.imwrite("temp.jpg", frame)

	#encode to base64
	with open("temp.jpg", "rb") as image_file:
		image_string = base64.b64encode(image_file.read())

	#Send temp frame to API
	#get the json of all
	url = "http://localhost:5000/process_base64"
	image = {'image_64': image_string}
	r = requests.post(url,data = image)

	#gettin array of faces
	faces_json = (r.text)

	#converting json to array of faces dicts
	faces = json.loads(faces_json)

	# detect faces in the grayscale frame
	#rects = detector(gray, 0)

	# loop over the face detections
	for face in faces:

		# get 68 points and put in np array
		shape_1 = face['face_68']
		shape = np.array(shape_1)

		#draw 68 on image
		for (x, y) in shape:
			cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

		face_rectangle = face['face_rect']
		
		
		#draw rectangle
		cv2.rectangle(frame, (face_rectangle[0], face_rectangle[1]), (face_rectangle[2], face_rectangle[3]), (255,0,0), 2)
		"""for (x1,y1,x2,y2) in face_rectangle:
			cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)"""


		#write name
		name = face['name']
		cv2.putText(frame,name, (face_rectangle[0],face_rectangle[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
	if(name == 'shehab'):
		cv2.waitKey(50)
		input()
		cv2.destroyAllWindows()
		vs.stop()
		break
		

for i in range(5):		
	print("\n")
equal()
while(True):
	choice = input("What do u want to know about me? (options: Education, Emploment_history, Academic_projects, Languages, Techinical_skills, Sports_achievments)\n")
	if(choice == "Exit"):
		break
	equal()
	for i in range(2):		
		print("\n")
	equal()
	if(choice == "Education"):
		print("-Bachelor of Science in Computer Engineering, American University in Cairo (AUC) \n-Expected Graduation Spring 2021 \n-GPA: 3.77 \n-IGCSE  Misr Language School, June 2016\n")
	# do a bit of cleanup

	if(choice == "Employment_history"):
		print("-Freelance Commercial Model  September 2015 – Present\n    *Modeled in 10+ TV commercial ads including: Pepsi Egypt, Vodafone Egypt, Nescafe Egypt.\n\n-Freelance Guitarist/Performer January 2012 – Present\n    *Performed 4 times with Cairo Guitar Orchestra at Cairo Opera House\n    *Performed at the Spanish Embassy in Egypt, Sheraton Cairo, Shooting Club\n")
		print("-Klenka, Cairo, Egypt/nMachine Learning intern  December 2017 - February 2018\n    *Implemented MNIST(Modified National Institute of Standards and Technology) Digit Recognizer\n    project using CNN(Convolutional Neural Network) with 0.99014 accuracy. (Python)\n    *Designed Face Detection and Recognition web API. (Python)\n    *Built a live video Face Detection and Recognition application. (Python)\n    *Developed Egyptian ID Arabic number reader and recognizer using CNN(Convolutional NeuralNetwork) and image processing. (Python)\n")

	if(choice == "Technical_skills"):
		print("-Programming Languages: C/C++, Python, HTML, JavaScript, JSON\n-Frameworks/tools: Flask web-development, Jinja 2, Linux(Terminal Commands)\n-Softwares: Visual Studio, VS Code, Microsoft Excel, Microsoft Word, Microsoft Access\n-Programming Skills: Image processing (OpenCV), Data Processing (Python), Object-Oriented,programming, Web-Development\n-Machine Learning Skills: CNN (Convolutional Neural Network), ANN(Artificial Neural Network), K-NN (K-Nearest Neighbors), SVM (Support Vector Machine), XGBoost, K-Means Clustering, Regression, Dimensionality Reduction.")

	if(choice == "Languages"):
		print("-Fluent in both spoken and written English\n-Native in both spoken and written Arabic")

	if(choice == "Academic_projects"):
		print("Developed a 2‐D game using C++ SFML\n-Built words frequency in a document application using BST in C++\n-Solved Sliding Tiles puzzle using PQ in C++")
	equal()
