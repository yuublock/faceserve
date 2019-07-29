# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file of person to censor
# The result is returned as json. For example:
#
# $ curl -XPOST -F "file=@known2.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_known": true
# }
import io
from draw_boxes import draw_boxes
from util import processImage
import shutil
import requests
import face_recognition
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request, redirect, send_file, session
from PIL import Image, ImageDraw
import numpy as np
import json
from config import *
# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# CORS(app)
app.config['CORS_HEADERS'] = "Content-Type"
# @app.after_request
# def add_headers(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            print('not there')
            return redirect(request.url)

        file = request.files['file']
        print('files')
        print(file)

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)
        
    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Faceblock</title>
    <h1>Upload a picture of the face to remove</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''
@app.route('/upload', methods=['POST'])
def uploadToYuuvis():
    baseUrl = 'https://api.yuuvis.io/dms/objects'
    header_name = 'Content-Type'
    # headerDict['Content-Type'] = 'multipart/form-data, application/x-www-form-urlencoded'
    headerDict = {}
    paramDict = {}
    header_name = 'Ocp-Apim-Subscription-Key'
    headerDict['Ocp-Apim-Subscription-Key'] = YKEY
    session = requests.Session()
    contentFilePath = './image_with_boxes.jpg'
    metaDataFilePath = './metadata.json'
    multipart_form_data = {
        'data' :('metadata.json', open(metaDataFilePath, 'rb'), 'application/json'),
        'mario' : ('image_with_boxes.jpg', open(contentFilePath, 'rb'), 'application/jpeg')
    }
    response = session.post(baseUrl, files=multipart_form_data, headers=headerDict)
    print(response.json())
    return response.json()

@app.route('/download', methods=['GET'])
def downloadToServer():
    headerDict = {}
    paramDict = {}
    baseUrl = 'https' + '://' + 'api.yuuvis.io'
    headerDict['Ocp-Apim-Subscription-Key'] = YKEY
    session = requests.Session()
   
    response = session.get(str(baseUrl+'/dms/objects/59408323-3063-4217-9ca7-661519b08b4a/contents/file'), stream=True,headers=headerDict)
    with open('./mario.jpeg', 'wb') as f:
        img = response.raw.decode_content = True
        shutil.copyfileobj(response.raw, f)
    return response.content

@app.route('/usemetoupload', methods=['POST'])
# @cross_origin(origin = '*')
def upload():
    response = jsonify({'some':'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    # del request.form.headers['Content-Type']

    
    # print(dir(request.files))
    # print(file)
    # file = request.files['picture']
    print('picture')
    # print(file.read())
    # print(request.data)
    # print(dir(request),'!!!')
    # for keys in request.files:
    #     print(keys + ':' + request.files.keys)
    
    # session = requests.Session()
    # response = session.post('/upload')
    # print(dir(response))
    # print(request.form['file'])
    # print(request.form.getlist('file'))
    v = request.files.get('file')
    processImage(v)
    print(v)
    # return response,201
    return response, 201

@app.route('/goose', methods=['GET'])
def getGoose():
    with open("./mario.jpeg", 'rb') as bites:
        return send_file(
                     io.BytesIO(bites.read()),
                     attachment_filename='mario.jpeg',
                     mimetype='image/jpg'
               )

def detect_faces_in_image(file_stream):
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)

    # Pre-calculated face encoding of the uploaded image generated with face_recognition.face_encodings(img)
    known_face_encoding = face_recognition.face_encodings(img)

    # Get face encodings for any faces in the image to censor
    unknown_image = face_recognition.load_image_file('images/unknown.jpg')
    unknown_face_encodings = face_recognition.face_encodings(unknown_image)

    face_found = False
    is_known = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face
        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
        if match_results[0].any():
            is_known = True

    if is_known:
        boxed = draw_boxes(img, unknown_image)
        boxed.save("image_with_boxes.jpg")

    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_known": is_known
    }
    # return jsonify(result)
    return send_file("image_with_boxes.jpg", mimetype='image/jpeg')

if __name__ == "__main__":
    app.secret_key = 'mario'
    app.run(host='0.0.0.0', port=5001, debug=True)
