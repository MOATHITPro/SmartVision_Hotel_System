class Notification:
    cred = credentials.Certificate('../config/security-c546f-firebase-adminsdk-eeok3-4bc85ca650.json')
    firebase_admin.initialize_app(cred)


