import requests

def send_notification(device_token, title, body, server_key):
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'key={server_key}'
    }
    payload = {
        'to': device_token,
        'notification': {
            'title': title,
            'body': body,
            
            'mutable_content': True,
            'sound': 'Tri-tone'
        },
        'data': {
            'url': "https://commons.wikimedia.org/wiki/File:External_link_font_awesome.svg",
            'dl': "deeplink"
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print('Notification sent successfully.')
    else:
        print(f'Failed to send notification. Status code: {response.status_code}')

# مثال على الاستخدام
device_token = 'flnb2bYJQu2Arx2dwcUojY:APA91bGdLs1x55AyR7KaU-D3ldl6OFFqj9amBEutPbSRGQUqIzo9rhiAERGUuSoHQEd1jeQSirfx-iTwCaT-txV2WEqopl1kY-e_pyqZPsNDIa8WxdiPAUD-RVb7NEMmD8ewRM1pWrjD'
title = 'Hello'
body = 'Welco evryone in this app'
server_key = 'AAAAKLeQxpE:APA91bG4mJkwGRgjtJIEDsTuoZBgmBLF4SyBUmnVsVqlTgC3sBHk5Vui0aUlJHnlf8wYd-qHRsKnoO-g2LIQBaBrEMy3PwdA1z57HYutpUBXDV4oqxZlUxedgD0hIUBU6Rp_rnzIU19c'
send_notification(device_token, title, body, server_key)
