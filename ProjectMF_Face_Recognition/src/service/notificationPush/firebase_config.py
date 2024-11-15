import firebase_admin
from firebase_admin import credentials

def initialize_app():
    # تهيئة التطبيق باستخدام ملف المفاتيح
    cred = credentials.Certificate('config/security-c546f-firebase-adminsdk-eeok3-4bc85ca650.json')
    firebase_admin.initialize_app(cred)