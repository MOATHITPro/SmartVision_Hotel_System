import tkinter as tk
from ui_app import VideoApp
import cv2
import dlib

# Initialize face detector, predictor, and model
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('../data/data_dlib/shape_predictor_68_face_landmarks.dat')
face_reco_model = dlib.face_recognition_model_v1("../data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

def main():
    window = tk.Tk()
    app = VideoApp(window, "Face Recognition Video Feed")
    app.run()

    cap = cv2.VideoCapture(0)  # Open default camera
    process_faces(cap)

def process_faces(stream):
    while stream.isOpened():
        ret, frame = stream.read()
        if ret:
            faces = detector(frame, 0)
            for face in faces:
                shape = predictor(frame, face)
                # Perform face recognition and other processing here
            cv2.imshow("Face Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
