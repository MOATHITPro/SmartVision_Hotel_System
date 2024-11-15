# #! C:\Users\Administrator\Desktop\FaceRecognition311\myenv\Scripts\python.exe

# # import requests
# import requests
# import json
# def send_notification(device_token, title, body, server_key):
#         url = 'https://fcm.googleapis.com/fcm/send'
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': 'key=' + server_key
#         }
#         payload = {
#             'to': device_token,
#             'notification': {
#                 'title': title,
#                 'body': body,
#                 'mutable_content': True,
#                 'sound': 'Tri-tone'
#             },
#             'data': {
#                 'url': 'https://commons.wikimedia.org/wiki/File:External_link_font_awesome.svg',
#                 'dl': 'deeplink'
#             }
#         }
#         response = requests.post(url, headers=headers, data=json.dumps(payload))
#         status_code = response.status_code
#         if status_code == 200:
#             return 'Notification sent successfully.'
#         else:
#             return 'Failed to send notification. Status code: ' + str(status_code)
#         # def run_notification():
# send_notification("dqfxv3i9S7izBs-LSSANzq:APA91bFcDm3z4qeH2toRyVjcoAQGZ70Ik7HqmkoAsb1nCzuw6MiEBRpwGoYeBd_c00B941cupBdzhUfMyMpeNZ7eyjxEVNNAjBwYOLF1WvqzZZeP1IfOtBfE-1_f_b1WkqGb8Okz_0lY","Danger","test endpoint ","AAAAKLeQxpE:APA91bG4mJkwGRgjtJIEDsTuoZBgmBLF4SyBUmnVsVqlTgC3sBHk5Vui0aUlJHnlf8wYd-qHRsKnoO-g2LIQBaBrEMy3PwdA1z57HYutpUBXDV4oqxZlUxedgD0hIUBU6Rp_rnzIU19c")
                            

import tkinter as tk
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Run Another Python File")
        self.geometry("300x150")
        
        # Create a button to run another Python file
        self.run_button = tk.Button(self, text="Run Script", command=self.run_script)
        self.run_button.pack(pady=30)
    
    def run_script(self):
        # Command to execute the other Python file
        os.system("python complex_example.py")

if __name__ == "__main__":
    app = App()
    app.mainloop()
