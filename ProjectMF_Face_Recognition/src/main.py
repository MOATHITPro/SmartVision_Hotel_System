import cv2
import logging
from face_recognition import Face_Recognizer

def main():
    logging.basicConfig(level=logging.INFO)
    face_recognizer = Face_Recognizer()
    face_recognizer.run()

if __name__ == '__main__':
    main()
