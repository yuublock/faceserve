import face_recognition

known_image = face_recognition.load_image_file('images/known.jpg')
unknown_image = face_recognition.load_image_file('images/unknown.jpg')

try:
    known_face_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
except IndexError:
    print("Unable to locate faces")

known_faces = [
    known_face_encoding
]

results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

print("Is the unknown face a picture of Known? {}".format(results[0]))
print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
