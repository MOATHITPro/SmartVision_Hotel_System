

import re
import socket
from cgitb import text
from distutils.text_file import TextFile
from multiprocessing import Value
from turtle import color
from typing import Self
from unittest import result
from PIL import Image, ImageTk
import sys
import os
import yaml

with open('../service/faceRecognetionAPI/config.yaml') as f:
    config = yaml.safe_load(f)

server_ip = config['server']['ip']
server_port=config['server']['port']
# تغييرها وفقًا لعنوان الخادم الخاص بك
base_url = f"http://{server_ip}:{server_port}"

# إضافة المسار الذي يحتوي على المجلد الأب إلى sys.path
current_dir = os.path.dirname(__file__)  # مجلد الحالي للملف النشط
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))  # المجلد الأب للمجلد الحالي
sys.path.insert(0, parent_dir)  # إضافة المسار إلى sys.path

# الآن يمكنك استيراد الوحدة بشكل مطلق
from database import DatabaseManager

import psutil
import os
import subprocess
import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
import threading                       
import requests
import tkinter as tk
import os
import mysql.connector


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("MFFace Recognetion")
        self.geometry(f"{1100}x{580}")
        self.attributes('-alpha', 0.9)
        # configure grid layout (4x4) 
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

         
        # create sidebar frame with widgets
        img_face=customtkinter.CTkImage(light_image=Image.open('../data/data_faces_from_camera/fahd.jpg'),dark_image=Image.open('../data/data_faces_from_camera/fahd.jpg'),size=(50,50))
      
        icon= Image.open("customtkinter/assets/icons/security.ico").resize((50, 50))
        icon2= Image.open("customtkinter/assets/icons/premium-service.ico").resize((50, 50))
        icon1 = ImageTk.PhotoImage(icon)
        iconpremium= ImageTk.PhotoImage(icon2)
        
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Controal", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text="Detection",image=icon1, command=self.run_Detection)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Stop",image=icon1,command=self.stop_Detection)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Screen Fit", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        # new button 
        self.sidebar_button_new1 = customtkinter.CTkButton(self.sidebar_frame, text="Server", image=icon1, command=self.run_server)
        self.sidebar_button_new1.grid(row=4, column=0, padx=20, pady=10)

        self.sidebar_button_new2 = customtkinter.CTkButton(self.sidebar_frame, text="Stop", image=icon1, command=self.stop_server)
        self.sidebar_button_new2.grid(row=5, column=0, padx=20, pady=10)
        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="IP")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent",text="API Services FR", border_width=2, text_color=("gray10", "#DCE4EE"),command=self.run_faceRecognetionAPI)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
       

        self.tabview = customtkinter.CTkTabview(self, width=250)
        
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Lastface")

        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Lastface"), text="Lastface", )
        
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)
        self.tabview.add("AllFaces")
        # self.tabview.add("Tab 3")
        # self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        # self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        # self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
        # #                                                 values=["Value 1", "Value 2", "Value Long Long Long"])
        # self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        # self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
        #                                             values=["Value 1", "Value 2", "Value Long....."])
        # self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        # self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Enter IP",
        #                                                    command=self.open_input_dialog_event)
        # self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        # self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="",image=img_face)
        # self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)
        # self.label_tab_3 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="",image=img_face)
        # self.label_tab_3.grid(row=0, column=1, padx=20, pady=20)
        # self.label_tab_4 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="",image=img_face)
        # self.label_tab_4.grid(row=0, column=2, padx=20, pady=20)
        folder_path = "../data/data_faces_from_camera"  # تحديد المسار الخاص بالمجلد
        self.display_images_in_folder(folder_path, self.tabview)
        self.recentFace(self.tabview)
        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        # self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame,image=iconpremium, text="Functions Group:")
        self.label_radio_group = customtkinter.CTkButton(master=self.radiobutton_frame, image=iconpremium, text="Face Recognetion")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0,text="InteernalNetwork")
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        # self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame,width=30,height=20, )
        self.progressbar_1 = customtkinter.CTkProgressBar(
            self.slider_progressbar_frame,
            width=200,  # عرض المستطيل
            height=20,  # ارتفاع المستطيل
            border_color='blue',      
            # bg_color='red',    
            corner_radius=4,
            progress_color='green'
          
        )
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.label_cpu = customtkinter.CTkLabel(
            self.slider_progressbar_frame,
           text=0,
          
        )
        self.label_cpu.grid(row=1, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.progressbar_2 = customtkinter.CTkProgressBar(
            self.slider_progressbar_frame,
            width=200,  # عرض المستطيل
            height=20,  # ارتفاع المستطيل
            border_color='blue',      
            # bg_color='red',    
            corner_radius=4,
            progress_color='green'
          
                                                          )
        self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")



        self.label_net = customtkinter.CTkLabel(
            self.slider_progressbar_frame,
           text=0,
          
        )
        self.label_net.grid(row=2, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")


        self.progressbar_3 = customtkinter.CTkProgressBar(
            self.slider_progressbar_frame,
            width=200,  # عرض المستطيل
            height=20,  # ارتفاع المستطيل
            border_color='blue',      
            # bg_color='red',    
            corner_radius=4,
            progress_color='green'
          
                                                          )
        self.progressbar_3.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.label_mem = customtkinter.CTkLabel(
            self.slider_progressbar_frame,
           text=0,
          
        )
        self.label_mem.grid(row=3, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")

        #   # Create button to stop main.py
        # self.stop_button = customtkinter.CTkButton(self, text="Stop Main", command=self.stop_main)
        # self.stop_button.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Camara Management")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(100):
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"Camara {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)
       
       
       
       
        # self.display_camera_images(["../data/data_faces_from_camera/me36.jpg"])

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.label_radio_group = customtkinter.CTkButton(master=self.checkbox_slider_frame, image=iconpremium, text="Web Serveses:")
        self.label_radio_group.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Services API")
        self.checkbox_1.configure(text="Bandwidth 3X")
        self.checkbox_2.configure(text="Token Secure")
        self.checkbox_3.configure(text="File Storage")
        self.checkbox_1.select()
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        self.radio_button_1.configure(state="disabled")
        self.radio_button_2.configure(state="disabled")
        self.radio_button_3.configure(state="disabled")
        self.radio_button_3.configure(text="Attribute Analysis")
        self.radio_button_2.configure(text="High-Performance")
        # self.radio_button_3.configure(text="disabled")
        
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        # self.optionmenu_1.set("CTkOptionmenu")
        # self.combobox_1.set("CTkComboBox")
        # self.slider_1.configure(command=self.progressbar_2.set)
        # self.slider_2.configure(command=self.progressbar_3.set)
        # self.progressbar_1.configure(mode="indeterminnate")
        # self.progressbar_1.start()

        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        self.seg_button_1.configure(values=["Level", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")
        self.get_cpu_performance()
        self.get_net_performance()
        self.get_url_fromYaml()
    # def display_camera_images(self, image_paths):
    #     # Iterate through camera image paths and display images
    #     for i, image_path in enumerate(image_paths):
    #         # Load image using PIL
    #         img = Image.open(image_path)

    #         # Resize image if needed to fit within the frame
    #         img = img.resize((100, 100), Image.ANTIALIAS)

    #         # Convert PIL Image to PhotoImage for tkinter display
    #         img_tk = ImageTk.PhotoImage()

    #         # Create a label to display the image within the custom scrollable frame
    #         label = self.scrollable_frame.create_label(image=img_tk)
    #         label.grid(row=i, column=0, padx=10, pady=(0, 20))

    #         # Keep a reference to the image to prevent garbage collection
    #         label.img_tk = img_tk
    def display_images_in_folder(self,folder_path, tabview):
        files = os.listdir(folder_path)  # قائمة بجميع الملفات في المجلد
        images = []  # قائمة لتخزين الصور
        
        # تحميل الصور وإضافتها إلى القائمة
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):  # التحقق من امتدادات الملفات المدعومة
                image_path = os.path.join(folder_path, file)  # مسار الصورة الكامل
                image = Image.open(image_path)  # فتح الصورة باستخدام PIL
                images.append(image)
        
        # عرض الصور في واجهة الاستخدام
        for i, image in enumerate(images):

            img_face = customtkinter.CTkImage(light_image=image, dark_image=image, size=(50, 50))
            
            label = customtkinter.CTkLabel(tabview.tab("AllFaces"), text="", image=img_face)
            label.grid(row=0, column=i, padx=20, pady=20)
            
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a IP :", title="IP Network")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
    
    
    
    def run_Detection(self):
        # Run ../test.py using python executable from myenv
        script_pathDetection = "../main.py"
        python_executable = r"C:\Users\Administrator\Desktop\FaceRecognition311\myenv\Scripts\python.exe"
        self.Detection_process = subprocess.Popen([python_executable, script_pathDetection])

    def stop_Detection(self):

        # Stop the main.py process if it's running
        if hasattr(self, 'main_process') and self.main_process.poll() is None:
            self.Detection_process.terminate()
            print("######### Detection is stoped")
    
    
    
    def run_faceRecognetionAPI(self):
        # Run ../test.py using python executable from myenv
        script_pathfaceRecognetionAPI = "../service/faceRecognetionAPI/faceRecognetionAPI.py"
        python_executable = r"C:\Users\Administrator\Desktop\FaceRecognition311\myenv\Scripts\python.exe"
        self.faceRecognetionAPI_process = subprocess.Popen([python_executable, script_pathfaceRecognetionAPI])

    def stop_faceRecognetionAPI(self):

        # Stop the main.py process if it's running
        if hasattr(self, 'main_process') and self.main_process.poll() is None:
            self.faceRecognetionAPI_process.terminate()
            print("######### Detection is stoped")
    
    def run_server(self):
        # Run ../test.py using python executable from myenv
        script_path_server = "../features_extraction_to_csv_API.py"
        python_executable = r"C:\Users\Administrator\Desktop\FaceRecognition311\myenv\Scripts\python.exe"
        self.server = subprocess.Popen([python_executable, script_path_server])

    def stop_server(self):
        # Stop the main.py process if it's running
        if hasattr(self, 'main_process') and self.server.poll() is None:
            self.server.terminate()
            print("######### server is stoped")

    def run_faceDetection(self):
        # Create a new thread to run the script
        script_thread = threading.Thread(target=self.execute_faceDetection, daemon=True)
        script_thread.start()

    def execute_faceDetection(self):
        # Command to execute the other Python file
        os.system("python ../main.py")


    def run_features_extraction_to_csv_API(self):
        # Create a new thread to run the script
        script_thread = threading.Thread(target=self.execute_features_extraction, daemon=True)
        script_thread.start()

    def execute_features_extraction(self):
        # Command to execute the other Python file
        os.system("python ../features_extraction_to_csv_API.py")



    def get_url_fromYaml(self):
       
        self.entry.insert(0, f"{base_url}/registration")
      
    def update_textbox(self):
        result=DatabaseManager().retrieveLatestface_unknown()
        if result:
            text = str(result[0])  # تحويل القيمة إلى سلسلة

            self.textbox.insert("1.0", "\n Alarm!!  Unknown person on the fourth floor " + text+" at "+str(result[3]))
            
        self.textbox.after(1000, self.update_textbox)
    def recentFace(self,tabview):
        
        result=DatabaseManager().retrieveLatestPersonData()
  
        if result:
            text = str(result[2])  # تحويل القيمة إلى سلسلة
            image = Image.open(text)
            img_face = customtkinter.CTkImage(light_image=image, dark_image=image, size=(200,200))
            label = customtkinter.CTkLabel(tabview.tab("Lastface"), text="", image=img_face)
            label.grid(row=0, column=0,  padx=10, pady=10, sticky="n")
        self.tabview.tab("Lastface").after(1000, self.recentFace)
        
        self.tabview.tab("Lastface").update()
    def get_cpu_performance(self):
        cpu_percent = psutil.cpu_percent(interval=None)
        
        self.progressbar_1.set(cpu_percent * 0.1)
        self.progressbar_1.update()
        
        self.label_cpu.configure(text=f"{cpu_percent * 0.1:.1f}")
        self.label_cpu.update
        # print(f"######## CPU Performance: {cpu_percent * 2}%")
        self.progressbar_1.after(1000, self.get_cpu_performance)
    def get_net_performance(self):
        cpu_percent = psutil.cpu_percent(interval=None)
        
        net_io = psutil.net_io_counters()
        net_sent = net_io.bytes_sent
        net_recv = net_io.bytes_recv
        self.progressbar_2.set(cpu_percent * 0.1)
        self.progressbar_2.update()
        print(int(net_sent*0.000001))
        # print(f"######## CPU Performance: {cpu_percent * 2}%")
        self.label_net.configure(text=f"{cpu_percent * 0.1:.1f}")
        self.label_net.update
        self.progressbar_2.after(1000, self.get_net_performance)

        
if __name__ == "__main__":
    app = App()
    app.update_textbox()
    app.mainloop()
