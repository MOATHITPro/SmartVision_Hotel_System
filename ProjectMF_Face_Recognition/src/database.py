import time
import mysql.connector
import datetime

class DatabaseManager:
    def __init__(self):
        print("init db connection")
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="face_recognition"
        )

    def verification(self, name):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM face_detect2 WHERE name = %s AND date = %s AND time = %s", (name, current_date, current_time))
        existing_entry = cursor.fetchone()

        if existing_entry:
            print(f"{name} is already marked as detected for {current_date} at {current_time}")
        else:
            cursor.execute("INSERT INTO face_detect2 (name, time, date) VALUES (%s, %s, %s)", (name, current_time, current_date))
            self.conn.commit()
            print(f"{name} marked as detected for {current_date} at {current_time}")
            
    def insert_unknown_face_record(self):
        try:
            if self.conn.is_connected():
                print("Connected to MySQL successfully")
                cursor = self.conn.cursor()

                # Get current date and time
                current_date = datetime.datetime.now().strftime('%Y-%m-%d')
                current_time = datetime.datetime.now().strftime('%H:%M:%S')

                # Insert record into 'face_unknown' table
                cursor.execute("INSERT INTO face_unknown (place, time, date, ipCamera, numCamera) VALUES (%s, %s, %s, %s, %s)",
                               ("first floor", current_time, current_date, "10.10.2.1", "1"))
                self.conn.commit()

                print("Unknown face record inserted successfully")
                # You can add API signal sending code here

        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")

        finally:
            if self.conn and self.conn.is_connected():
                cursor.close()
                print("MySQL connection is closed")

    
    
    def savePersonData(self,name,link_face_image,room_number,checkin,checkout,additional_data,modified_by):
        try:
             if self.conn.is_connected():
                print("Connected to MySQL successfully")
                cursor = self.conn.cursor()

            # Insert record into 'Person' table
                cursor.execute("INSERT INTO person (name, link_face_image, checkin, checkout, room_number, additional_data, modified_by) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (name, link_face_image, checkin, checkout, room_number, additional_data, modified_by))
                self.conn.commit()


                print("Unknown face record inserted successfully")
                # You can add API signal sending code here

        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")

        finally:
            if self.conn and self.conn.is_connected():
                cursor.close()
                print("MySQL connection is closed")

  
    
    def retrievePersonData(self):
        try:
            if self.conn.is_connected():
                cursor = self.conn.cursor()

                # Retrieve all records from 'person' table
                cursor.execute("SELECT * FROM person")
                records = cursor.fetchall()

                return records

        except mysql.connector.Error as e:
            print(f"Error retrieving data from MySQL: {e}")
            return None

        finally:
            if self.conn and self.conn.is_connected():
                cursor.close()
                print("MySQL connection is closed")

    def retrieveLatestPersonData(self):
        try:
            if self.conn.is_connected():
                cursor = self.conn.cursor()

                # Retrieve the last record from 'person' table
                cursor.execute("SELECT * FROM person ORDER BY id DESC LIMIT 1")
                record = cursor.fetchone()

                return record

        except mysql.connector.Error as e:
            print(f"Error retrieving data from MySQL: {e}")
            return None

        finally:
            if self.conn and self.conn.is_connected():
                cursor.close()
                print("MySQL connection is closed")
    

    def retrieveLatestface_detect2(self):
        try:
            if self.conn.is_connected():
                cursor = self.conn.cursor()

                # Retrieve the last record from 'person' table
                cursor.execute("SELECT id FROM face_detect2 ORDER BY id DESC LIMIT 1")
                record = cursor.fetchone()

                return record

        except mysql.connector.Error as e:
            print(f"Error retrieving data from MySQL: {e}")
            return None

        finally:
            if self.conn and self.conn.is_connected():
                cursor.close()
                print("MySQL connection is closed")
    


    def retrieveLatestface_unknown(self):
        try:
            if self.conn.is_connected():
                cursor = self.conn.cursor()

                # Retrieve the last record from 'person' table
                cursor.execute("SELECT * FROM face_unknown ORDER BY id DESC LIMIT 1")
                record = cursor.fetchone()

                return record

        except mysql.connector.Error as e:
            print(f"Error retrieving data from MySQL: {e}")
            return None

        finally:
            if self.conn and self.conn.is_connected():
                cursor.close()
                print("MySQL connection is closed")
    
    def retrieveAllPersons(self):
        try:
            if self.conn.is_connected():
                cursor = self.conn.cursor()

                # Retrieve all records from 'person' table
                cursor.execute("SELECT * FROM person")
                records = cursor.fetchall()

                return records

        except mysql.connector.Error as e:
            print(f"Error retrieving data from MySQL: {e}")
            return None

        finally:
            if self.conn and self.conn.is_connected():
                cursor.close()
                print("MySQL connection is closed")
    def close_connection(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("MySQL connection is closed")
