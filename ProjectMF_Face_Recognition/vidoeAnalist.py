import cv2
import dlib
import numpy as np
import os

# Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

# Load Dlib shape predictor
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

# Load Dlib resnet50 model
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

class FaceExtractor:
    def __init__(self):
        pass

    def extract_faces(self, video_path, output_dir):
        cap = cv2.VideoCapture(video_path)
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            

            frame_count += 1
            print(f"Processing frame {frame_count}")

            # Detect faces in the frame
            faces = detector(frame, 0)
            
            # Extract and save faces
            for i, face in enumerate(faces):
                # Get face landmarks
                shape = predictor(frame, face)
                
                # Draw landmarks on the frame (optional)
                # for j in range(shape.num_parts):
                #     x, y = shape.part(j).x, shape.part(j).y
                #     cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

                # Extract face region
                face_img = frame[face.top():face.bottom(), face.left():face.right()]

                # Save face image
                face_file_path = os.path.join(output_dir, f"frame_{frame_count}_face_{i}.jpg")
                cv2.imwrite(face_file_path, face_img)

        cap.release()

def main():
    video_path = "egyptCelebrait.mp4"
    output_dir = "output_faces"
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    face_extractor = FaceExtractor()
    face_extractor.extract_faces(video_path, output_dir)

if __name__ == "__main__":
    main()








# version 2

#  مسبقًا قبل حفظها مرة أخرى. هنا الكود المحدث:

# python
# Copy code
# import cv2
# import dlib
# import numpy as np
# import os

# # Use frontal face detector of Dlib
# detector = dlib.get_frontal_face_detector()

# # Load Dlib shape predictor
# predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

# # Load Dlib resnet50 model
# face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

# class FaceExtractor:
#     def __init__(self):
#         pass

#     def extract_faces(self, video_path, output_dir):
#         cap = cv2.VideoCapture(video_path)
#         frame_count = 0
#         saved_faces = []

#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             frame_count += 1
#             print(f"Processing frame {frame_count}")

#             # Detect faces in the frame
#             faces = detector(frame, 0)
            
#             # Extract and save faces
#             for i, face in enumerate(faces):
#                 # Check if face has already been saved
#                 if self.face_already_saved(face, saved_faces):
#                     continue

#                 # Save face to list
#                 saved_faces.append(face)

#                 # Extract face region
#                 face_img = frame[face.top():face.bottom(), face.left():face.right()]

#                 # Save face image
#                 face_file_path = os.path.join(output_dir, f"frame_{frame_count}_face_{i}.jpg")
#                 cv2.imwrite(face_file_path, face_img)

#         cap.release()

#     def face_already_saved(self, face, saved_faces):
#         for saved_face in saved_faces:
#             if self.face_similarity(face, saved_face) < 50:  # Adjust threshold as needed
#                 return True
#         return False

#     def face_similarity(self, face1, face2):
#         # Compute similarity between two faces based on their positions
#         # You can use different metrics for comparison if needed
#         distance = np.sqrt((face1.left() - face2.left())**2 + (face1.top() - face2.top())**2)
#         return distance

# def main():
#     video_path = "path_to_video.mp4"
#     output_dir = "output_faces"
    
#     # Create output directory if it doesn't exist
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     face_extractor = FaceExtractor()
#     face_extractor.extract_faces(video_path, output_dir)

# if __name__ == "__main__":
#     main()
# يرجى استبدال "path_to_video.mp4" بمسار ملف الفيديو الذي تريد استخراج الوجوه منه. يتم استخراج الوجوه من كل إطار في الفيديو والتحقق مما إذا كانت الوجوه قد تم حفظها مسبقًا قبل حفظها مرة أخرى، مع مراعاة عدم حفظ أكثر من صورتين لنفس الوجه.