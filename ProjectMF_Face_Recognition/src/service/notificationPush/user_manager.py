from firebase_admin import firestore

class UserManager:
    def __init__(self):
        self.db = firestore.client()

    def get_users(self):
        # قراءة بيانات المستخدمين
        users_ref = self.db.collection('users')
        users = users_ref.get()

        for user in users:
            print(f'User ID: {user.id}')
            print(f'Username: {user.get("username")}')
            # استعراض المزيد من الحقول الأخرى حسب الحاجة
            print('----------------------')