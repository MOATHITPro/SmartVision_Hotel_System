from database import DatabaseManager

from flask import Flask, request
import os
import dlib
import csv
import numpy as np
import logging
import cv2
import os
import base64
from flask import Flask, jsonify
from database import DatabaseManager

app = Flask(__name__)

#  Path of cropped faces
path_images_from_camera = "data/data_faces_from_camera/"

#  Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

#  Get face landmarks
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

#  Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

#  Return 128D features for single image
def return_128d_features(img_rd):
    faces = detector(img_rd, 1)

    logging.info("%-40s %-20s", " Image with faces detected:", "Received Image")

    # For photos of faces saved, we need to make sure that we can detect faces from the cropped images
    if len(faces) != 0:
        shape = predictor(img_rd, faces[0])
        face_descriptor = face_reco_model.compute_face_descriptor(img_rd, shape)
    else:
        face_descriptor = 0
        logging.warning("no face")
    return face_descriptor

# Save image and extract features
@app.route("/upload", methods=["POST"])
def upload_image():
    file = request.files["image"]
    # ghamdan add new info
    checkin = request.form["checkin"]
    checkout = request.form["checkout"]
    roomid = request.form["roomid"]
    print("######## ",checkin,checkout)
            
    print("######## ",roomid)
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Save the image
    filename = file.filename
    save_path = os.path.join(path_images_from_camera, filename)
    cv2.imwrite(save_path, img)
    
    # Extract features from the image
    features_128d = return_128d_features(img)
    
    # Save features to CSV
    with open("data/features_all.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([filename.split(".jpg")[0]] + list(features_128d))
    
    response = [filename.split(".jpg")[0]] + list(features_128d)


    print("===========================================")
    print("save_path:",save_path)
    print("===========================================")
    
   # Pass the necessary arguments to savePersonData
    DatabaseManager().savePersonData(
        name=filename.split(".jpg")[0],
        link_face_image=save_path,  # Pass the saved image path
        room_number=roomid,
        checkin=checkin,
        checkout=checkout,
        additional_data=None,  # Add additional data if needed
        modified_by="System"  # Specify the modifier
    )
                            
    print(f'###################{response}')
    print(f'###################{[filename.split(".jpg")[0]]}')
    
    return str(response)
    # return 

@app.route('/persons', methods=['GET'])
def get_all_persons():
    persons = DatabaseManager().retrieveAllPersons()

    if persons is None:
        response = {
            'status': 'error',
            'message': 'Failed to retrieve persons from the database'
        }
    else:
        # تحويل البيانات إلى تنسيق يحتوي على البيانات الكاملة مع ترميز الصورة
        formatted_persons = []
        for person in persons:
            # استخراج اسم الصورة من الرابط الموجود في قاعدة البيانات
            image_filename = os.path.basename(person[2])
            # تشكيل المسار الكامل للصورة
            image_path = os.path.join(path_images_from_camera, image_filename)
            # قراءة محتوى الملف باستخدام وضع البايتات الثنائية
            with open(image_path, 'rb') as f:
                image_data = f.read()
            # ترميز الصورة باستخدام Base64
            encoded_image = base64.b64encode(image_data).decode('utf-8')

            # بناء البيانات المنسقة
            formatted_person = list(person)
            formatted_person[2] = encoded_image
            formatted_persons.append(formatted_person)

        response = {
            'status': 'success',
            'data': formatted_persons
        }

    return jsonify(response)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host="192.168.43.75")