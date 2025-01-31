from datetime import datetime
from arduinoControllers.led_controller import LEDController
# from monitorDetectAndRunArduino import ArduinoController
from notify import Notify
from database import DatabaseManager
import requests
import json
import dlib
import numpy as np
import cv2
import os
import pandas as pd
import time
import logging
import sqlite3
import datetime
import mysql.connector
from mysql.connector import Error
import asyncio
from service.notificationPush.notification_manager import Notification

import pyttsx3
from gtts import gTTS
import playsound
# Dlib  / Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

# Dlib landmark / Get face landmarks
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

# Dlib Resnet Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")




class Face_Recognizer:
    def __init__(self):
        self.font = cv2.FONT_ITALIC
      
        # FPS
        self.frame_time = 0
        self.frame_start_time = 0
        self.fps = 0
        self.fps_show = 0
        self.start_time = time.time()

        # cnt for frame
        self.frame_cnt = 0

        #  Save the features of faces in the database
        self.face_features_known_list = []
        # / Save the name of faces in the database
        self.face_name_known_list = []

        #  List to save centroid positions of ROI in frame N-1 and N
        self.last_frame_face_centroid_list = []
        self.current_frame_face_centroid_list = []

        # List to save names of objects in frame N-1 and N
        self.last_frame_face_name_list = []
        self.current_frame_face_name_list = []

        #  cnt for faces in frame N-1 and N
        self.last_frame_face_cnt = 0
        self.current_frame_face_cnt = 0

        # Save the e-distance for faceX when recognizing
        self.current_frame_face_X_e_distance_list = []

        # Save the positions and names of current faces captured
        self.current_frame_face_position_list = []
        #  Save the features of people in current frame
        self.current_frame_face_feature_list = []

        # e distance between centroid of ROI in last and current frame
        self.last_current_frame_centroid_e_distance = 0

        #  Reclassify after 'reclassify_interval' frames
        self.reclassify_interval_cnt = 0
        self.reclassify_interval = 15

    #  "features_all.csv"  / Get known faces from "features_all.csv"
    def get_face_database(self):
        if os.path.exists("data/features_all.csv"):
            path_features_known_csv = "data/features_all.csv"
            csv_rd = pd.read_csv(path_features_known_csv, header=None)
            for i in range(csv_rd.shape[0]):
                features_someone_arr = []
                self.face_name_known_list.append(csv_rd.iloc[i][0])
                for j in range(1, 129):
                    if csv_rd.iloc[i][j] == '':
                        
                        features_someone_arr.append('0')
                    else:
                        features_someone_arr.append(csv_rd.iloc[i][j])
                self.face_features_known_list.append(features_someone_arr)
            logging.info("Faces in Database： %d", len(self.face_features_known_list))
            return 1
        else:
            logging.warning("'features_all.csv' not found!")
            logging.warning("Please run 'get_faces_from_camera.py' "
                            "and 'features_extraction_to_csv.py' before 'face_reco_from_camera.py'")
            return 0

    def update_fps(self):
        now = time.time()
        # Refresh fps per second
        if str(self.start_time).split(".")[0] != str(now).split(".")[0]:
            self.fps_show = self.fps
        self.start_time = now
        self.frame_time = now - self.frame_start_time
        self.fps = 1.0 / self.frame_time
        self.frame_start_time = now
    
    
    @staticmethod
    # / Compute the e-distance between two 128D features
    def return_euclidean_distance(feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)

        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        return dist

    # / Use centroid tracker to link face_x in current frame with person_x in last frame
    def centroid_tracker(self):
        for i in range(len(self.current_frame_face_centroid_list)):
            e_distance_current_frame_person_x_list = []
            #  For object 1 in current_frame, compute e-distance with object 1/2/3/4/... in last frame
            for j in range(len(self.last_frame_face_centroid_list)):
                self.last_current_frame_centroid_e_distance = self.return_euclidean_distance(
                    self.current_frame_face_centroid_list[i], self.last_frame_face_centroid_list[j])

                e_distance_current_frame_person_x_list.append(
                    self.last_current_frame_centroid_e_distance)

            last_frame_num = e_distance_current_frame_person_x_list.index(
                min(e_distance_current_frame_person_x_list))
            self.current_frame_face_name_list[i] = self.last_frame_face_name_list[last_frame_num]

    #  cv2 window / putText on cv2 window
    def draw_note(self, img_rd):
        #  / Add some info on windows
        cv2.putText(img_rd, "Detection", (20, 40), self.font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "Frame  " + str(self.frame_cnt), (20, 100), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "FPS    " + str(self.fps.__round__(2)), (20, 130), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Faces  " + str(self.current_frame_face_cnt), (20, 160), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Q", (20, 450), self.font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

        for i in range(len(self.current_frame_face_name_list)):
            img_rd = cv2.putText(img_rd, "F " + str(i + 1), tuple(
                [int(self.current_frame_face_centroid_list[i][0]), int(self.current_frame_face_centroid_list[i][1])]),
                                 self.font,
                                 0.8, (255, 190, 0),
                                 1,
                                 cv2.LINE_AA)
          
   





   
    def facial_landmark_detector(image, rect):
    # تحميل محدد الوجه الذي تم تدريبه مسبقًا
        predictor_path = 'data/data_dlib/shape_predictor_68_face_landmarks.dat'
        predictor = dlib.shape_predictor(predictor_path)

    # تحويل إطار الوجه إلى نقاط تخطيط الوجه
        shape = predictor(image, rect)
        landmarks = [(shape.part(i).x, shape.part(i).y) for i in range(shape.num_parts)]
        return landmarks
  
    #  Face detection and recognition wit OT from input video stream
    def process(self, stream):
        count_sure=0
        
        
        # 1. Get faces known from "features.all.csv"
        if self.get_face_database():
            while stream.isOpened():
                self.frame_cnt += 1
       
                logging.debug("Frame " + str(self.frame_cnt) + " starts")
                flag, img_rd = stream.read()
                kk = cv2.waitKey(1)
                
            # 2. Detect faces for frame X
                faces = detector(img_rd, 0)

            # 3. Update cnt for faces in frames
                self.last_frame_face_cnt = self.current_frame_face_cnt
                self.current_frame_face_cnt = len(faces)

            # 4. Update the face name list in last frame
                self.last_frame_face_name_list = self.current_frame_face_name_list[:]

            # 5. Update frame centroid list
                self.last_frame_face_centroid_list = self.current_frame_face_centroid_list
                self.current_frame_face_centroid_list = []

            # 6.1 If cnt not changes
                if (self.current_frame_face_cnt == self.last_frame_face_cnt) and (
                    self.reclassify_interval_cnt != self.reclassify_interval):
                    logging.debug("scene 1: No face cnt changes in this frame!!!")

                    self.current_frame_face_position_list = []

                    if "unknown" in self.current_frame_face_name_list:
                        
                        self.reclassify_interval_cnt += 1
                        count_sure+=1
                        print(count_sure)
                        if  count_sure>=15:
                            DatabaseManager().insert_unknown_face_record()
                            notify = Notify()
                            notify.run_notification("Alert ", "Unknown face detected on the first floor from camera 1")
                                
                            # Notification().send_push_notification("Danger",'service/notificationPush/config/security-c546f-firebase-adminsdk-eeok3-4bc85ca650.json', "Unknown Face on the first floor!!", None)
                            # if __name__ == '__Notification__':
                            #     process = multiprocessing.Process(target=run_notification)
                            #     process.start()
                    if self.current_frame_face_cnt != 0:
                        for k, d in enumerate(self.new_method(faces)):
                            self.current_frame_face_position_list.append(tuple(
                                [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))
                            self.current_frame_face_centroid_list.append(
                            [int(faces[k].left() + faces[k].right()) / 2,
                             int(faces[k].top() + faces[k].bottom()) / 2])
                            
                            # img_rd = cv2.rectangle(img_rd,
                            #                    tuple([d.left(), d.top()]),
                            #                    tuple([d.right(), d.bottom()]),
                            #                    (0, 255, 0), 2)
                        
                        # Loop through the facial landmarks and draw them as points
                            shape = predictor(img_rd, d)
                            for i in range(shape.num_parts):
                                x = shape.part(i).x
                                y = shape.part(i).y
                                cv2.circle(img_rd, (x, y), 2, (255,51,255), 1)
                            
                        # Write names under ROI
                    
                    for i in range(self.current_frame_face_cnt):
                                # img_rd = cv2.putText(img_rd, self.current_frame_face_name_list[i],
                                #                  self.current_frame_face_position_list[i], self.font, 0.8, (0, 255, 255), 1,
                                #                  cv2.LINE_AA)

                            # Draw green rectangle with transparent background
                                rect_x = self.current_frame_face_position_list[i][0] 
                                rect_x += -40
                                rect_y = self.current_frame_face_position_list[i][1]
                                rect_y -= -5
                                rect_w = 100  # Width of the rectangle
                                rect_h = 20  # Height of the rectangle

                            # Draw the green rectangle with transparent background
                                overlay = img_rd.copy()
                                cv2.rectangle(overlay, (rect_x + rect_w, rect_y), (rect_x + rect_w + 150, rect_y + rect_h),
                                          (0, 255, 0), -1)

                                alpha = 0.3
                                img_rd = cv2.addWeighted(overlay, alpha, img_rd, 1 - alpha, 0)  # دمج الصورتين بشفافية محددة
                                # Write text on the green rectangle
                                cv2.putText(img_rd,self.current_frame_face_name_list[i], (rect_x + rect_w + 10, rect_y +15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (51, 25, 0), 1,
                            cv2.LINE_AA)

                    if self.current_frame_face_cnt != 1:
                        self.centroid_tracker()

                    for i in range(self.current_frame_face_cnt):
                        # 6.2 Write names under ROI
                        print("name", self.current_frame_face_name_list[i])
                       
                    #     img_rd = cv2.putText(img_rd, self.current_frame_face_name_list[i],
                    #                          self.current_frame_face_position_list[i], self.font, 0.8, (0, 255, 255), 1,
                    #                          cv2.LINE_AA)
                    # self.draw_note(img_rd)

                # 6.2  If cnt of faces changes, 0->1 or 1->0 or ...
                else:
                    logging.debug("scene 2: / Faces cnt changes in this frame")
                    self.current_frame_face_position_list = []
                    self.current_frame_face_X_e_distance_list = []
                    self.current_frame_face_feature_list = []
                    self.reclassify_interval_cnt = 0

                    # 6.2.1  Face cnt decreases: 1->0, 2->1, ...
                    if self.current_frame_face_cnt == 0:
                        logging.debug("  / No faces in this frame!!!")
                        # clear list of names and features
                        self.current_frame_face_name_list = []
                    # 6.2.2 / Face cnt increase: 0->1, 0->2, ..., 1->2, ...
                    else:
                        logging.debug("  scene 2.2  Get faces in this frame and do face recognition")
                        self.current_frame_face_name_list = []
                        for i in range(len(faces)):
                            shape = predictor(img_rd, faces[i])
                            self.current_frame_face_feature_list.append(
                                face_reco_model.compute_face_descriptor(img_rd, shape))
                            self.current_frame_face_name_list.append("unknown")
                            unique_filename = "unknonw.jpg"
                            unknown_faces_folder="data/unknown_faces_from_camera"
                            face_path = os.path.join(unknown_faces_folder, unique_filename)
                            #حفظ الصورة في المجلد
                            cv2.imwrite(face_path, img_rd)

                        # 6.2.2.1 Traversal all the faces in the database
                        for k in range(len(faces)):
                            
                            logging.debug("  For face %d in current frame:", k + 1)
                            self.current_frame_face_centroid_list.append(
                                [int(faces[k].left() + faces[k].right()) / 2,
                                 int(faces[k].top() + faces[k].bottom()) / 2])

                            self.current_frame_face_X_e_distance_list = []

                            # 6.2.2.2  Positions of faces captured
                            self.current_frame_face_position_list.append(tuple(
                                [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))

                            # 6.2.2.3 
                            # For every faces detected, compare the faces in the database
                            for i in range(len(self.face_features_known_list)):
                                # 
                                if str(self.face_features_known_list[i][0]) != '0.0':
                                    count_sure=0
                                    e_distance_tmp = self.return_euclidean_distance(
                                        self.current_frame_face_feature_list[k],
                                        self.face_features_known_list[i])
                                    logging.debug("      with person %d, the e-distance: %f", i + 1, e_distance_tmp)
                                    self.current_frame_face_X_e_distance_list.append(e_distance_tmp)
                                else:
                                    #  person_X
                                    self.current_frame_face_X_e_distance_list.append(999999999)

                            # 6.2.2.4 / Find the one with minimum e distance
                            similar_person_num = self.current_frame_face_X_e_distance_list.index(
                                min(self.current_frame_face_X_e_distance_list))

                            if min(self.current_frame_face_X_e_distance_list) < 0.4:
                                self.current_frame_face_name_list[k] = self.face_name_known_list[similar_person_num]
                                logging.debug("  Face recognition result: %s",
                                              self.face_name_known_list[similar_person_num])
                                
                                # Insert verification record
                                nam =self.face_name_known_list[similar_person_num]
                                print(type(self.face_name_known_list[similar_person_num]))
                                print("Pesrson known :",nam)
                                DatabaseManager().verification(nam)
                                # arduinocontroller = ArduinoController()
                                # arduinocontroller.start_observing()
# استدعاء ا
                            else:
                                logging.debug("  Face recognition result: Unknown person")

                        # 7.  / Add note on cv2 window
                        self.draw_note(img_rd)

                # 8.  'q'  / Press 'q' to exit
                if kk == ord('q'):
                    break

                self.update_fps()
                cv2.namedWindow("SPACEFACE", 1)
                cv2.imshow("SPACEFACE", img_rd)

        
                logging.debug("Frame ends\n\n")

    def new_method(self, faces):
        return faces
            

    def run(self):
        # cap = cv2.VideoCapture("video.mp4")  # Get video stream from video file
        cap = cv2.VideoCapture(0)              # Get video stream from camera
        self.process(cap)

        cap.release()
        cv2.destroyAllWindows()
    
   