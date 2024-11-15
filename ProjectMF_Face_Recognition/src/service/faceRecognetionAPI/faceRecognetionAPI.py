
import yaml

from flask import Flask, request
import os
import dlib
import csv
import numpy as np
import logging
import cv2

app = Flask(__name__)

# with open('config.yaml') as f:
#     config = yaml.safe_load(f)

server_ip = "192.168.43.75"
# config['server']['ip']
#  Path of cropped faces
path_images_from_camera = "data/data_faces_from_camera/"

#  Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

#  Get face landmarks
predictor = dlib.shape_predictor('../../data/data_dlib/shape_predictor_68_face_landmarks.dat')

#  Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1("../../data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

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
@app.route("/registration", methods=["POST"])
def upload_image():
    file = request.files["image"]
    # ghamdan add new info
    # checkin = request.form["checkin"]
    # checkout = request.form["checkout"]
    # roomid = request.form["roomid"]
    # print("######################",checkin,checkout)
            
    # print("######################",roomid)
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
    print(img)
    print(filename)
    print("===========================================")
    
   # Pass the necessary arguments to savePersonData
                          
    print(f'###################{response}')
    print(f'###################{[filename.split(".jpg")[0]]}')
    
    return str(response)
    # return 


# # تحقق من الهوية
# @app.route("/verify", methods=["POST"])


# def verify_identity():
#     file = request.files["image"]
#     img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

#     # Extract person name from filename (without extension)
#     filename = file.filename
#     person_name = filename.split('.')[0]

#     # Extract features from the image
#     features_128d = return_128d_features(img)

#     if features_128d is not None:
#         # Read stored features from CSV
#         with open("data/features_all.csv", "r") as csvfile:
#             reader = csv.reader(csvfile)
#             for row in reader:
#                 name = row[0]

#                 if name == person_name:
#                     stored_features = np.array(row[1:], dtype=float)

#                     # Calculate Euclidean distance between extracted and stored features
#                     distance = np.sqrt(np.sum(np.square(features_128d - stored_features)))

#                     # Set a threshold for identity match
#                     threshold = 0.6

#                     if distance <= threshold:
#                         return name  # Match found

#         return "No match found"
#     else:
#         return "No face detected in the provided image"


# Route to verify identity
@app.route("/verify", methods=["POST"])
def verify_identity():
    file = request.files["image"]
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Extract person name from filename (without extension)
    filename = file.filename
    person_name = filename.split('.')[0]

    # Extract features from the image
    features_128d = return_128d_features(img)

    if features_128d is not None:
        # Load all stored features from CSV into a dictionary
        stored_features_dict = {}
        print("############features_128d :",features_128d)
        with open("data/features_all.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name = row[0]
                stored_features = np.array(row[1:], dtype=float)
                stored_features_dict[name] = stored_features

        # Check if the person_name exists in the stored features dictionary
        if person_name in stored_features_dict:
            stored_features = stored_features_dict[person_name]

            # Calculate Euclidean distance between extracted and stored features
            distance = np.linalg.norm(features_128d - stored_features)
            print("@@@@@@@@@@@@@ features_128d :",features_128d)
            print("@@@@@@@@@@@@@ stored_features :",stored_features)
            # Set a threshold for identity match (adjust as needed)
            threshold = 0.6

            if distance <= threshold:
                return person_name  # Match found
            else:
                return "No match found"  # Features do not match

    return "No face detected in the provided image"  # No valid features extracted

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host=server_ip)