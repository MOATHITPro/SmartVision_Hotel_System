import cv2
import dlib
import numpy as np
import pandas as pd
import datetime
import mysql.connector
import logging

class FaceRecognizer:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')
        self.face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

        # Establish MySQL connection
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="face_recognition"
            )
            if self.conn.is_connected():
                print("MySQL connection successful")
        except mysql.connector.Error as e:
            print("Cannot connect to MySQL:", e)

        self.cursor = self.conn.cursor()

    def create_database_table(self):
        current_date = datetime.datetime.now().strftime("%Y_%m_%d")
        table_name = "face_detect2"
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name TEXT, time TEXT, date DATE)"
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def update_database(self, name):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        # Check if the name is already marked as detected for the current date and time
        self.cursor.execute("SELECT * FROM face_detect2 WHERE name = %s AND date = %s AND time = %s", (name, current_date, current_time))
        existing_entry = self.cursor.fetchone()

        if existing_entry:
            print(f"{name} is already marked as detected for {current_date} at {current_time}")
        else:
            # Insert the name into the database
            self.cursor.execute("INSERT INTO face_detect2 (name, time, date) VALUES (%s, %s, %s)", (name, current_time, current_date))
            self.conn.commit()
            print(f"{name} marked as detected for {current_date} at {current_time}")

    def return_euclidean_distance(self, feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        return dist

    def process(self):
        cap = cv2.VideoCapture(0)  # Using the default camera (change the argument for different video source)
        frame_cnt = 0

        while cap.isOpened():
            ret, img_rd = cap.read()
            if not ret:
                break

            frame_cnt += 1
            faces = self.detector(img_rd, 0)

            for face in faces:
                shape = self.predictor(img_rd, face)
                face_feature = self.face_reco_model.compute_face_descriptor(img_rd, shape)
                # Perform face recognition logic here...

            # Display FPS and other info on the frame
            cv2.putText(img_rd, "Frame: " + str(frame_cnt), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.imshow("Face Recognition", img_rd)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def run(self):
        self.create_database_table()
        self.process()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    face_recognizer = FaceRecognizer()
    face_recognizer.run()
