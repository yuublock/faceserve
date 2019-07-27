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

import face_recognition
from flask import Flask, jsonify, request, redirect, send_file
from PIL import Image, ImageDraw
import numpy as np

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

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

    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_known": is_known
    }
    # return jsonify(result)
    return send_file("image_with_boxes.jpg", mimetype='image/jpeg')

def draw_boxes(known_image, unknown_image):
    # Load a sample picture and learn how to recognize it.
    # known_image = face_recognition.load_image_file("images/known.jpg")
    known_face_encoding = face_recognition.face_encodings(known_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        known_face_encoding
    ]
    known_face_names = [
        "Known"
    ]

    # Load an image with an unknown face
    # unknown_image = face_recognition.load_image_file("images/unknown.jpg")

    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    pil_image = Image.fromarray(unknown_image)
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # Draw a label with a name below the face
        #text_width, text_height = draw.textsize(name)
        #draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        #draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
        if name == 'Known':
            draw.rectangle(((left, top), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))

    # Remove the drawing library from memory as per the Pillow docs
    del draw

    pil_image.save("image_with_boxes.jpg")
    return pil_image


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
