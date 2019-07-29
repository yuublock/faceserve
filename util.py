import requests
import face_recognition
import io
from draw_boxes import draw_boxes 

# def uploadToYuuvis(files):
#     baseUrl = 'https://api.yuuvis.io/dms/objects'
#     header_name = 'Content-Type'
#     # headerDict['Content-Type'] = 'multipart/form-data, application/x-www-form-urlencoded'
#     headerDict = {}
#     paramDict = {}
#     header_name = 'Ocp-Apim-Subscription-Key'
#     headerDict['Ocp-Apim-Subscription-Key'] = YKEY
#     session = requests.Session()
#     contentFilePath = './image_with_boxes.jpg'
#     metaDataFilePath = './metadata.json'
#     multipart_form_data = {
#         'data' :('metadata.json', open(metaDataFilePath, 'rb'), 'application/json'),
#         'mario' : ('image_with_boxes.jpg', open(contentFilePath, 'rb'), 'application/jpeg')
#     }
#     response = session.post(baseUrl, files=multipart_form_data, headers=headerDict)
#     print(response.json())
#     return response.json()

# def foo():
#   print('mario')

def processImage(file_stream):
    # Load the uploaded image file
    print('maridjfkdj')
    # file_stream = openk(files, 'rb')
    # file_stream = io.BytesIO(files)
    # print(dir(file_stream))
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
        boxed.save("image_dwith_boxkes.jpg")

    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_known": is_known
    }
    # return jsonify(result), 201
    # return send_file("image_with_boxes.jpg", mimetype='image/jpeg')