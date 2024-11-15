import multiprocessing
from notification_manager import Notification

# Replace with the path to your service account key JSON file
server_key = 'config/security-c546f-firebase-adminsdk-eeok3-4bc85ca650.json'

# Replace with your device tokens
device_tokens = [
    'dqfxv3i9S7izBs-LSSANzq:APA91bFcDm3z4qeH2toRyVjcoAQGZ70Ik7HqmkoAsb1nCzuw6MiEBRpwGoYeBd_c00B941cupBdzhUfMyMpeNZ7eyjxEVNNAjBwYOLF1WvqzZZeP1IfOtBfE-1_f_b1WkqGb8Okz_0lY',
    'DEVICE_TOKEN_2',
    # Add more device tokens as needed
]

# Notification details
title = 'Test Notification'
body = 'This is a test notification.'
data = {
    'key1': 'value1',
    'key2': 'value2'
}

def long_running_function():
    # هنا يمكنك وضع العمليات التي تستغرق وقتًا طويلاً
    Notification().send_push_notification(title, server_key, body, data)
    pass

if __name__ == '__main__':
    multiprocessing.freeze_support()  # تجميد الدعم للعمليات
    # إنشاء عملية فرعية لتنفيذ الدالة
    process = multiprocessing.Process(target=long_running_function)

    # تشغيل العملية الفرعية بشكل مستقل
    process.start()

    print("countino processing")