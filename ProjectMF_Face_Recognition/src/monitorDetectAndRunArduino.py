



import os
import time
import serial

from database import DatabaseManager

class ArduinoController:
    # db_manager = DatabaseManager()
    def __init__(self):
        self.arduino = serial.Serial(port="COM10", baudrate=9600, timeout=0.1)
        # self.db_manager = DatabaseManager()
 
    def runLed(self):
        self.arduino.write(bytes('R', 'utf-8'))
        time.sleep(2)  # انتظر لمدة 2 ثوانٍ
        self.arduino.write(bytes('R', 'utf-8'))

    def start_observing(self):
        last_row_count = self.get_row_count()

        while True:
            row_count = self.get_row_count()
            print("it's loop observer")
            if row_count > last_row_count:
                print("@@@ codetion", row_count > last_row_count)
                self.handle_new_entry()

            last_row_count = row_count
            time.sleep(1)  # الانتظار لمدة ثانية واحدة قبل التحقق مرة أخرى

    def get_row_count(self):
        record = DatabaseManager().retrieveLatestface_detect2()
        if record:
            id = record[0]  # استخراج القيمة الفعلية لحقل id
            print("@@@ stat get row count", id)
            return id
        else:
            return 0  # إذا لم يتم استرداد أي سجل، يمكنك تعيين قيمة افتراضية هنا

    def handle_new_entry(self):
        print("@@@ start handle led ")
        # يتم استدعاء هذه الدالة عند إضافة إدخال جديد في جدول face_detect2
        # اقم هنا العمل الذي تريد تنفيذه عند حدوث التغيير
        self.runLed()
        print("New entry detected in face_detect2 table")

# تكوين كائن ArduinoController مع المنفذ المحدد
arduinocontroller = ArduinoController()
arduinocontroller.start_observing()
 