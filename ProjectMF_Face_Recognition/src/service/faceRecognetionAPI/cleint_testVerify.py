import yaml
import requests

with open('config.yaml') as f:
    config = yaml.safe_load(f)

server_ip = config['server']['ip']
server_port=config['server']['port']
# تعيين عنوان URL لطلب POST إلى الـ API
url = f"http://{server_ip}:{server_port}/verify"  # استبدل "your-api-address-here" بعنوان الـ API الخاص بك

# تحديد الملف المطلوب إرساله
image_filename = "stafInGoogle.jpg"  # استبدل بمسار الصورة التي تريد استخدامها

# فتح الملف كـ binary وإرساله كجزء من الطلب POST
with open(image_filename, "rb") as file:
    files = {"image": file}
    response = requests.post(url, files=files)

# التحقق من الاستجابة
if response.status_code == 200:
    print("Identity verified for:", response.text)
else:
    print("Verification failed:", response.text)
