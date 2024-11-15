import requests
import cv2
import yaml
with open('config.yaml') as f:
    config = yaml.safe_load(f)

server_ip = config['server']['ip']
server_port=config['server']['port']
# تغييرها وفقًا لعنوان الخادم الخاص بك
base_url = f"http://{server_ip}:{server_port}"

# نقطة النهاية لرفع الصورة واستخراج الميزات
upload_endpoint = "/registration"

# تغييرها وفقًا لمسار الصورة التي تريد تحميلها واستخراج الميزات منها
image_path = "stafInGoogle.jpg"

# قراءة الصورة
image = cv2.imread(image_path)

# إنشاء طلب POST مع إرفاق الملف
files = {'image': open(image_path, 'rb')}


response = requests.post(base_url + upload_endpoint, files=files)

# قراءة الاستجابة
if response.status_code == 200:
    print("تم تحميل الصورة واستخراج الميزات بنجاح!")
    print("استجابة الخادم: ", response.text)
else:
    print("فشل في تحميل الصورة واستخراج الميزات.")