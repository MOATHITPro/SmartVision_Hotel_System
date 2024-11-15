# import dlib
# import numpy as np
# import cv2
# import pandas as pd
# import logging
# import mysql.connector
# import datetime
# import requests
# import os

# # Dlib
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')
# face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

# # إنشاء اتصال بقاعدة البيانات
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="face_recognition"
# )
# cursor = conn.cursor()

# # إنشاء جدول للتاريخ الحالي
# current_date = datetime.datetime.now().strftime("%Y_%m_%d")
# table_name = "face_detect2"
# create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name TEXT, time TEXT, date DATE)"
# cursor.execute(create_table_sql)
# conn.commit()

# class FaceRecognizer:
#     def __init__(self):
#         self.font = cv2.FONT_ITALIC
#         self.face_features_known_list = []
#         self.face_name_known_list = []
#         self.current_frame_face_name_list = []
#         self.current_frame_face_feature_list = []

#     def get_face_database(self):
#         path_features_known_csv = "data/features_all.csv"
#         if os.path.exists(path_features_known_csv):
#             csv_rd = pd.read_csv(path_features_known_csv, header=None)
#             for i in range(csv_rd.shape[0]):
#                 features_someone_arr = []
#                 self.face_name_known_list.append(csv_rd.iloc[i][0])
#                 for j in range(1, 129):
#                     features_someone_arr.append('0' if pd.isnull(csv_rd.iloc[i][j]) else csv_rd.iloc[i][j])
#                 self.face_features_known_list.append(features_someone_arr)
#             logging.info("Faces in Database: %d", len(self.face_features_known_list))
#             return True
#         else:
#             logging.warning("'features_all.csv' not found!")
#             return False

#     def notify_flutter_app(self, name):
#         flutter_endpoint_url = 'http://localhost:8080'  # تحديد النقطة النهائية المناسبة هنا
#         payload = {'text': f'تعرف على الوجه: {name}'}
#         response = requests.post(flutter_endpoint_url, json=payload)
#         print(response.text)

#     def verification(self, name):
#         current_date = datetime.datetime.now().strftime('%Y-%m-%d')
#         current_time = datetime.datetime.now().strftime('%H:%M:%S')

#         cursor.execute("SELECT * FROM face_detect2 WHERE name = %s AND date = %s AND time = %s",
#                        (name, current_date, current_time))
#         existing_entry = cursor.fetchone()

#         if existing_entry:
#             print(f"{name} is already marked as detected for {current_date} at {current_time}")
#         else:
#             cursor.execute("INSERT INTO face_detect2 (name, time, date) VALUES (%s, %s, %s)",
#                            (name, current_time, current_date))
#             conn.commit()
#             print(f"{name} marked as detected for {current_date} at {current_time}")

#     def process(self, image_path):
#         if self.get_face_database():
#             img_rd = cv2.imread(image_path)
#             faces = detector(img_rd, 0)

#             for i in range(len(faces)):
#                 shape = predictor(img_rd, faces[i])
#                 self.current_frame_face_feature_list.append(
#                     face_reco_model.compute_face_descriptor(img_rd, shape))
#                 self.current_frame_face_name_list.append("unknown")

#             for k in range(len(faces)):
#                 self.current_frame_face_X_e_distance_list = []
#                 for i in range(len(self.face_features_known_list)):
#                     if str(self.face_features_known_list[i][0]) != '0.0':
#                         e_distance_tmp = np.sqrt(
#                             np.sum(np.square(np.array(self.current_frame_face_feature_list[k]) -
#                                              np.array(self.face_features_known_list[i]))))
#                         self.current_frame_face_X_e_distance_list.append(e_distance_tmp)
#                     else:
#                         self.current_frame_face_X_e_distance_list.append(999999999)

#                 similar_person_num = self.current_frame_face_X_e_distance_list.index(
#                     min(self.current_frame_face_X_e_distance_list))

#                 if min(self.current_frame_face_X_e_distance_list) < 0.4:
#                     self.current_frame_face_name_list[k] = self.face_name_known_list[similar_person_num]
#                     print(f"Face recognition result: {self.face_name_known_list[similar_person_num]}")
#                     self.verification(self.face_name_known_list[similar_person_num])
#                 else:
#                     print("Face recognition result: Unknown person")
#                     self.notify_flutter_app("Unknown Person")

#     def run(self):
#         image_path = "ImagesClient/unkown.jpg"
#         self.process(image_path)

# if __name__ == '__main__':
#     FaceRecognizer_con = FaceRecognizer()
#     FaceRecognizer_con.run()


from flask import Flask, request
import dlib
import numpy as np
import cv2
import pandas as pd
import logging
import mysql.connector
import datetime
import requests
import os

app = Flask(__name__)

# Dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

# إنشاء اتصال بقاعدة البيانات
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="face_recognition"
)
cursor = conn.cursor()

# إنشاء جدول للتاريخ الحالي
current_date = datetime.datetime.now().strftime("%Y_%m_%d")
table_name = "face_detect2"
create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name TEXT, time TEXT, date DATE)"
cursor.execute(create_table_sql)
conn.commit()

class FaceRecognizer:
    def __init__(self):
        self.font = cv2.FONT_ITALIC
        self.face_features_known_list = []
        self.face_name_known_list = []
        self.current_frame_face_name_list = []
        self.current_frame_face_feature_list = []

    def get_face_database(self):
        path_features_known_csv = "data/features_all.csv"
        if os.path.exists(path_features_known_csv):
            csv_rd = pd.read_csv(path_features_known_csv, header=None)
            for i in range(csv_rd.shape[0]):
                features_someone_arr = []
                self.face_name_known_list.append(csv_rd.iloc[i][0])
                for j in range(1, 129):
                    features_someone_arr.append('0' if pd.isnull(csv_rd.iloc[i][j]) else csv_rd.iloc[i][j])
                self.face_features_known_list.append(features_someone_arr)
            logging.info("Faces in Database: %d", len(self.face_features_known_list))
            return True
        else:
            logging.warning("'features_all.csv' not found!")
            return False

    def notify_flutter_app(self, name):
        flutter_endpoint_url = 'http://127.0.0.1:5000/notify'
        payload = {'text': f'تعرف على الوجه: {name}'}
        response = requests.post(flutter_endpoint_url, json=payload)
        print(response.text)

    def verification(self, name):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        cursor.execute("SELECT * FROM face_detect2 WHERE name = %s AND date = %s AND time = %s",
                       (name, current_date, current_time))
        existing_entry = cursor.fetchone()

        if existing_entry:
            print(f"{name} is already marked as detected for {current_date} at {current_time}")
        else:
            cursor.execute("INSERT INTO face_detect2 (name, time, date) VALUES (%s, %s, %s)",
                           (name, current_time, current_date))
            conn.commit()
            print(f"{name} marked as detected for {current_date} at {current_time}")

    def process(self, image_path):
        if self.get_face_database():
            img_rd = cv2.imread(image_path)
            faces = detector(img_rd, 0)

            for i in range(len(faces)):
                shape = predictor(img_rd, faces[i])
                self.current_frame_face_feature_list.append(
                    face_reco_model.compute_face_descriptor(img_rd, shape))
                self.current_frame_face_name_list.append("unknown")

            for k in range(len(faces)):
                self.current_frame_face_X_e_distance_list = []
                for i in range(len(self.face_features_known_list)):
                    if str(self.face_features_known_list[i][0]) != '0.0':
                        e_distance_tmp = np.sqrt(
                            np.sum(np.square(np.array(self.current_frame_face_feature_list[k]) -
                                             np.array(self.face_features_known_list[i]))))
                        self.current_frame_face_X_e_distance_list.append(e_distance_tmp)
                    else:
                        self.current_frame_face_X_e_distance_list.append(999999999)

                similar_person_num = self.current_frame_face_X_e_distance_list.index(
                    min(self.current_frame_face_X_e_distance_list))

                if min(self.current_frame_face_X_e_distance_list) < 0.4:
                    self.current_frame_face_name_list[k] = self.face_name_known_list[similar_person_num]
                    print(f"Face recognition result: {self.face_name_known_list[similar_person_num]}")
                    self.verification(self.face_name_known_list[similar_person_num])
                else:
                    print("Face recognition result: Unknown person")
                    self.notify_flutter_app("Unknown Person")

    def run(self):
        image_path = "ImagesClient/me.jpg"
        self.process(image_path)
        print('############# sent notify')


@app.route('/notify', methods=['POST'])
def notify():
    payload = request.json
    name = payload.get('text')
    FaceRecognizer_con.notify_flutter_app(name)
    print('############# sent notify')
    return 'Notification Sent'

if __name__ == '__main__':
    print('############# sent notify')
    FaceRecognizer_con = FaceRecognizer()
    app.run()