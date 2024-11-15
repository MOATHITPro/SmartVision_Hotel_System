import os
import base64
from flask import Flask, jsonify
from database import DatabaseManager

app = Flask(__name__)
db = DatabaseManager()

# تحديد المسار الكامل لمجلد الصور
IMAGES_FOLDER = 'data/data_faces_from_camera/'

@app.route('/persons', methods=['GET'])
def get_all_persons():
    persons = db.retrieveAllPersons()

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
            image_path = os.path.join(IMAGES_FOLDER, image_filename)
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
    app.run(host="192.168.43.75")