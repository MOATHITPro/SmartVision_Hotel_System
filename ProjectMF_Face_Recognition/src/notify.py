import requests
import json
import threading
import socket

class Notify:
    def __init__(self):
        self.url = 'https://fcm.googleapis.com/fcm/send'
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.device_token  = 'flnb2bYJQu2Arx2dwcUojY:APA91bGdLs1x55AyR7KaU-D3ldl6OFFqj9amBEutPbSRGQUqIzo9rhiAERGUuSoHQEd1jeQSirfx-iTwCaT-txV2WEqopl1kY-e_pyqZPsNDIa8WxdiPAUD-RVb7NEMmD8ewRM1pWrjD'
        self.server_key = 'AAAAKLeQxpE:APA91bG4mJkwGRgjtJIEDsTuoZBgmBLF4SyBUmnVsVqlTgC3sBHk5Vui0aUlJHnlf8wYd-qHRsKnoO-g2LIQBaBrEMy3PwdA1z57HYutpUBXDV4oqxZlUxedgD0hIUBU6Rp_rnzIU19c'

    def check_internet_connection(self):
        try:
            # يتم فحص اتصال الإنترنت باستخدام socket
            socket.create_connection(('www.google.com', 80), timeout=1)
            return True
        except socket.error:
            return False

    def send_notification(self, title, body):
        headers = {
            'Authorization': 'key=' + self.server_key
        }
        payload = {
            'to': self.device_token,
            'notification': {
                'title': title,
                'body': body,
                'mutable_content': True,
                'sound': 'Tri-tone'
            },
            'data': {
                'url': 'https://commons.wikimedia.org/wiki/File:External_link_font_awesome.svg',
                'dl': 'deeplink'
            }
        }
        response = requests.post(self.url, headers={**self.headers, **headers}, data=json.dumps(payload))
        status_code = response.status_code
        if status_code == 200:
            
            print('Notification sent successfully.')
            return 'Notification sent successfully.'
        else:
            
            print('Failed sent successfully.')
            return 'Failed to send notification. Status code: ' + str(status_code)

    def run_notification(self, title, body):

        if not self.check_internet_connection():
            print("## No internet connection.")
            return 'Failed to send notification. No internet connection.'

        thread = threading.Thread(target=self.send_notification, args=(title, body))
        thread.start()
        print("## Sending in progress....")
        return 'Notification sending in progress.'
