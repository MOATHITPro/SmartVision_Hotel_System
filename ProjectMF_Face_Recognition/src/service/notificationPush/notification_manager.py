import multiprocessing
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import firestore

class Notification:
    
    def send_push_notification(self,title,server_key, body, data=None):
        # تهيئة Firebase Admin SDK
        cred = credentials.Certificate(server_key)
        app = firebase_admin.initialize_app(cred)

        # إرسال الإشعار باستخدام Firebase Cloud Messaging
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            tokens=[]
        )
        if data:
            message.data = data

        # استعلام مجموعة "tokens" في Firestore لاسترداد جميع التوكنات
        db = firestore.client(app=app)
        tokens_collection = db.collection('tokens')
        tokens = [doc.to_dict()['token'] for doc in tokens_collection.stream()]
        message.tokens = tokens

        response = messaging.send_multicast(message)

        print("Successfully sent notification:", response)

        # تخزين الإشعار في Firestore
        notifications_collection = db.collection('notifications')
        for token in tokens:
            notification_data = {
                'title': title,
                'body': body,
                'token': token
            }
            if data:
                notification_data['data'] = data

            notifications_collection.add(notification_data)

        print("Successfully stored notification in Firestore.")