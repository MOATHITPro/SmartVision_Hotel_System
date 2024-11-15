

# import pyfirmata2

# port = "COM9"
# board = pyfirmata2.Arduino(port)

# print("المنافذ الرقمية:")
# for pin in board.digital:
#     print(pin.pin_number)

# print("المنافذ التناظرية:")
# for pin in board.analog:
#     print(pin.pin_number)

# board.exit()


# import pyfirmata2
# import time
# port="COM9"
# board=pyfirmata2.Arduino(port)
# # ledPin=board.get_pin("D:13:O")
# ledPin = board.get_pin("d:2:o")
# while True:
#     ledPin.write(1)
#     time.sleep(1)
#     ledPin.write(0)
#     ledPin.write(0)
# board.exit()

# import pyfirmata2
# import time

# port = "COM9"
# board = pyfirmata2.Arduino(port)
# ledPin = board.get_pin("d:2:o")

# # Light up the LED for 1 seconds
# ledPin.write(1)
# time.sleep(1)
# ledPin.write(0)

# board.exit()


# import serial

# # تعيين المنفذ السلسلي وسرعة الباود
# port = 'COM10'  # قم بتغيير COM3 إلى المنفذ السلسلي الصحيح الذي يتم استخدامه
# baudrate = 9600

# # افتح اتصال سلسلي
# ser = serial.Serial(port, baudrate)

# while True:
#     # إرسال بيانات إلى Arduino
#     command = input("أدخل البيانات المراد إرسالها (1 أو 0): ")
#     ser.write(command.encode())

#     # قراءة البيانات المرسلة من Arduino
#     data = ser.readline().decode().strip()

#     # عرض البيانات المستلمة
#     print("البيانات المستلمة: ", data)



# import serial
# import time

# # تعيين المنفذ السلسلي وسرعة الباود
# port = 'COM10'  # قم بتغيير COM10 إلى المنفذ السلسلي الصحيح الذي يتم استخدامه
# baudrate = 9600

# # افتح اتصال سلسلي
# ser = serial.Serial(port, baudrate)

# # إرسال إشارة لتشغيل LED
# ser.write('1'.encode())
# print("تم إرسال إشارة لتشغيل LED.")

# # انتظر لمدة 3 ثوانٍ
# time.sleep(3)

# # إرسال إشارة لإطفاء LED
# ser.write('0'.encode())
# print("تم إرسال إشارة لإطفاء LED.")

# # قراءة البيانات المرسلة من Arduino
# data = ser.readline().decode().strip()

# # عرض البيانات المستلمة
# print("البيانات المستلمة: ", data)

# import serial
# import time
# import sys

# # تعيين المنفذ السلسلي وسرعة الباود
# port = 'COM10'  # قم بتغيير COM10 إلى المنفذ السلسلي الصحيح الذي يتم استخدامه
# baudrate = 9600

# # افتح اتصال سلسلي
# ser = serial.Serial(port, baudrate)

# # إرسال إشارة لتشغيل LED
# ser.write('1'.encode())
# print("تم إرسال إشارة لتشغيل LED.")

# # انتظر لمدة 3 ثوانٍ
# time.sleep(3)

# # إرسال إشارة لإطفاء LED
# ser.write('0'.encode())
# print("تم إرسال إشارة لإطفاء LED.")

# # قراءة البيانات المرسلة من Arduino
# data = ser.readline().decode().strip()

# # عرض البيانات المستلمة
# print("البيانات المستلمة: ", data)

# # إغلاق اتصال سلسلي
# ser.close()

# # انتهاء البرنامج
# sys.exit()

# import serial
# import time

# # تعيين المنفذ السلسلي وسرعة الباود
# port = 'COM10'  # قم بتغيير COM10 إلى المنفذ السلسلي الصحيح الذي يتم استخدامه
# baudrate = 9600

# # افتح اتصال سلسلي
# ser = serial.Serial(port, baudrate)

# # إرسال إشارة '1' لتشغيل LED
# ser.write('1'.encode())
# print("تم إرسال إشارة لتشغيل LED.")

# # انتظر لمدة 3 ثوانٍ
# time.sleep(3)

# # إرسال إشارة '0' لإطفاء LED
# ser.write('0'.encode())
# print("تم إرسال إشارة لإطفاء LED.")

# # قراءة البيانات المرسلة من Arduino
# data = ser.readline().decode().strip()

# # عرض البيانات المستلمة
# print("البيانات المستلمة: ", data)

# # إغلاق اتصال سلسلي
# ser.close()

 
import serial
import time
 
 
def arduinoCMD():
  
   # تعيين المنفذ السلسلي وسرعة الباود
    port = 'COM10'  # قم بتغيير COM10 إلى المنفذ السلسلي الصحيح الذي يتم استخدامه
    baudrate = 9600

    # افتح اتصال سلسلي
    ser = serial.Serial(port, baudrate)

    # إرسال إشارة '1' لتشغيل LED لمدة 5 ثوانٍ
    ser.write('1'.encode())
    print("تم إرسال إشارة لتشغيل LED.")

    # انتظر لمدة 5 ثوانٍ
    time.sleep(5)

    # إرسال إشارة '0' لإطفاء LED
    ser.write('0'.encode())
    print("تم إرسال إشارة لإطفاء LED.")

    # قراءة البيانات المرسلة من Arduino
    data = ser.readline().decode().strip()

    # عرض البيانات المستلمة
    print("البيانات المستلمة: ", data)

    # إغلاق اتصال سلسلي
    ser.close()

def execute_code_on_change():
    # قم بتنفيذ الكود الذي تريده عند إضافة حقل جديد في الجدول
    print("تم اكتشاف تغيير في الجدول. قم بتنفيذ الكود هنا.")

