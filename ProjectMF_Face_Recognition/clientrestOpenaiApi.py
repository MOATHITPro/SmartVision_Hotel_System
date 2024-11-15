import requests
import json

def send_api_request(message):
    url = 'http://localhost/restOpenaiApi/api.php'
    headers = {'Content-Type': 'application/json'}
    data = {'content': message}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        print('حدث خطأ أثناء استدعاء النقطة النهائية.')
        return None

message = input('أدخل رسالتك: ')
response = send_api_request(message)

if response:
    print(response)