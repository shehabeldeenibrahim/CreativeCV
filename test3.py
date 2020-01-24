import json
import os
import numpy
from flask import Flask, request, redirect, url_for, flash,render_template, send_from_directory
from werkzeug.utils import secure_filename
import requests
from os.path import basename
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import io
import base64
import json_tricks


def json_to_dict(file_path):
    with open(file_path) as json_data:
        d = json.load(json_data)
    json_dict = json.loads(d)
    return json_dict

def euclidean_distance(a,b):
    dist = numpy.linalg.norm(a-b)
    return dist

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def path_of_picture(full_path,file_name):
    return full_path.replace("/"+file_name,'')

def face_recognised(directory):
    return basename(directory)

def draw_rectangle(path, rectangle,text):
    fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
    source_img = Image.open(path).convert("RGBA")
    draw = ImageDraw.Draw(source_img)
    draw.rectangle(rectangle)
    draw.text((10,60), text, font=fnt, fill=(255,255,255,255))
    source_img.save('kamel.jpg')


app = Flask(__name__)

#2D array has jsonfilename:128array
pic_dataset = []

#dictionary has jsonfilename:rectangle array
name_rect = {}

#working directory
rootdir = '/media/shehab/D/Facerec_Project'


#LOADING DATASET
#loop over all the folders in root directory
#convert json string to python dictionary
#save 128 array to pic_dataset
#save rectangle in name_rectangle dict
for subdir, dirs, files in os.walk(rootdir):
    for filename in files:
        if filename.endswith(".json"): 
            json_to_dict(subdir+'/'+filename)
            json_dict = json_to_dict(subdir+'/'+filename)
            picture_128 = json_dict[0]['face_128']
            pic_dataset.append([filename,picture_128])

            name_rect[filename] = json_dict[0]['face_rect']
            continue
        else:
            continue



@app.route("/upload",methods=['GET','POST'])
def upload_file():
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file submitted"

        #Get uploaded file
        file = request.files["file"]
        
        #convert to base64
        buff=file.read()
        image_string = base64.b64encode(buff)



        #Send uploaded file to API and get
        #dictionary of 128 and 64 array
        url = "http://localhost:5000/process_base64"

        image = {'image_64': image_string}
        r = requests.post(url,data = image)

        #convert json to python dictionary
        pic_json = str(r.text)
        submitted_picture = json.loads(pic_json)
        
        #Array of picturename:EUdistance between
        #each image and submitted image
        distances = []

        #loop around all the dataset and add
        #picturename:distance
        i = 0
        x = len(pic_dataset)
        for i in range(x):
            temp = pic_dataset[i][1]
            temp = numpy.array(temp)
            sp = submitted_picture[0]['face_128']
            sp = numpy.array(sp)
            dist = euclidean_distance(temp,sp)
            distances.append([pic_dataset[i][0],dist])
            i = i+1

        #sort the array ascendingly
        distances.sort(key=lambda x: x[1])

        #get pic name from json name
        if distances[0][0].endswith('.json'):
            similar = distances[0][0][:-4]
            similar = similar+'jpg'
        #get path and directory of the most similar image
        full_path = find(similar, rootdir)
        directory = path_of_picture(full_path,similar)

        
    #return directory
    #return similar
    #return face_recognised(directory)
    #return url_for(full_path)
    #return send_from_directory(directory,similar)
    return face_recognised(directory)	
    #return send_from_directory('/media/shehab/D/Facerec_Project','kamel.jpg')


@app.route("/upload_64",methods=['GET','POST'])
def upload_file_64():
    
    if request.method == 'POST':
        
        image_64 = request.form['image_64']
        
        #convert json to python dictionary
        submitted_picture = json.loads(image_64)

        for face in submitted_picture:
            #Array of picturename:EUdistance between
            #each image and submitted image
            distances = []
            #loop around all the dataset and add
            #picturename:distance
            i = 0
            x = len(pic_dataset)
            for i in range(x):
                temp = pic_dataset[i][1]
                temp = numpy.array(temp)
                sp = face['face_128']
                sp = numpy.array(sp)
                dist = euclidean_distance(temp,sp)
                distances.append([pic_dataset[i][0],dist])
                i = i+1

            #sort the array ascendingly
            distances.sort(key=lambda x: x[1])

            #get pic name from json name
            if distances[0][0].endswith('.json'):
                similar = distances[0][0][:-4]
                similar = similar+'jpg'
            #get path and directory of the most similar image
            full_path = find(similar, rootdir)
            directory = path_of_picture(full_path,similar)
            #append name
            name = face_recognised(directory)
            face['name'] = name
           

    json_submitted_picture = json_tricks.dumps(submitted_picture)
    return json_submitted_picture
    #return send_from_directory('/media/shehab/D/Facerec_Project','kamel.jpg')



if __name__ == '__main__':
    app.run(debug=True, port = 5001)

