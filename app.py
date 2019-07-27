from flask import Flask, render_template, request
import os, datetime
from werkzeug.utils import secure_filename
import uuid
import face_recognition

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/upload', methods = ['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)

@app.route('/result', methods=['GET'])
def result():
    return "File uploaded"

if __name__ == '__main__':
    app.run(debug = True)
