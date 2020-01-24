import os
from flask import Flask, request, redirect, url_for, flash,render_template, send_from_directory
from werkzeug.utils import secure_filename
#from face2 import process_picture, load_models
from test_rectangle3 import process_picture, load_models
from json import dump
import cv2
import numpy
import base64
import sys
import io
from PIL import Image
import json_tricks
import requests


#Loading model
detector, sp, facerec = load_models('shape_predictor_68_face_landmarks.dat','dlib_face_recognition_resnet_model_v1.dat','temp')


UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))

# convert PIL Image to an RGB image( technically a numpy array ) that's compatible with opencv
def toRGB(image):
    return cv2.cvtColor(numpy.array(image), cv2.COLOR_BGR2RGB)

#passing image            
@app.route("/index",methods=['GET','POST'])
def upload_file():
   
    if request.method == 'POST':
        #return "posted"

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files["file"]

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) 
            img = cv2.imdecode(numpy.fromstring(request.files['file'].read(), numpy.uint8), cv2.IMREAD_COLOR)
            picture_5 = process_picture(detector,sp,facerec,img)
            filename = "picture_json.json"
            with open(filename, 'w') as f:
                dump(picture_5, f)
            return picture_5




#passing base_64
@app.route("/process_base64",methods=['GET','POST'])
def upload_64():
    if request.method == 'GET': 

        # check if the post request has the file part

        #return "ds"
        image_64 = request.args['image_64']
        r = base64.decodestring(image_64)
        q = numpy.frombuffer(r, dtype=numpy.float64)  
        #return image_64
        # if user does not select file, browser also
        # submit a empty part without filename

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) 
            img = cv2.imdecode(numpy.fromstring(request.files['file'].read(), numpy.uint8), cv2.IMREAD_COLOR)
            picture_5 = process_picture(detector,sp,facerec,q)
            filename = "picture_json.json"
            with open(filename, 'w') as f:
                dump(picture_5, f)
            return picture_5
    else:
        # check if the post request has the file part

        #Get posted image_64 string
        image_64 = request.form['image_64']

        #Decode to Array for opencv
        img = toRGB(stringToImage(image_64))

        #get 128,68,rect
        picture_5 = process_picture(detector,sp,facerec,img)

        #dump in json form
        json_picture_5 = json_tricks.dumps(picture_5)
        

        #Send json string has arrays to API 
        #append name and distance
        url = "http://localhost:5001/upload_64"
        image = {'image_64': json_picture_5}
        r = requests.post(url,data = image)

        #get json with name appended
        json_pic_all = (r.text)
        return json_pic_all



if __name__ == '__main__':
    app.run(debug=True)
