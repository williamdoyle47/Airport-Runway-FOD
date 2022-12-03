import sqlite3
import os
import shutil
# from detection_modules import Detection

# Incorporate soon
# image_folder_path = "fsfsf"


class LogDetection:
    def __init__(self):
        # self.detection = detection
        self.db_path = "detections.db"

    def create_db(self):
        try:
            conn = sqlite3.connect('detections.db')
            cursor = conn.cursor()

            cursor.execute("""CREATE TABLE detections(
                fodType text default "placeholderType",
                coordinates text DEFAULT "[0,0]",
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                confidenceScore float DEFAULT 0.6
            ) """)

            # data = cursor.execute(""" SELECT * FROM detections;""")
            # data = data.fetchall()
            # i = 0
            # for item in data:
            #     i = i+1
            #     print("\n")
            #     print(str(i) + ". ", item)

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(e)

    # Insert to DB

    def insertToDb(self, db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO detections VALUES (?, ?, ?, ?)", (self.detection.fod_type, str(self.detection.location),
                                                                          self.detection.datetime, float(self.detection.confidence_score)))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(e)

    # clear log
    def clearLog(self):  # clears the log file -- update to modify log in FOD Analytics endpoint so GUI can see log
        with open("Log.txt", "a") as text_file:
            text_file.truncate(0)

    # write log
    # writes the log file -- update to modify log in FOD Analytics endpoint so GUI can see log
    def writeToLog(self, folderPath):
        with open(folderPath, "a") as text_file:
            text_file.write(self.detection.__str__() + '-----\n')

    # store images in folder -- temp

    def create_img_folder(self, folderName):  # creates folder
        exists = os.path.exists(folderName)
        if not exists:
            os.makedirs(folderName)

    # deletes folder contents (don't want a huge folder of images)
    def delete_folder_contents(self, folderName):
        for filename in os.listdir(folderName):
            file_path = os.path.join(folderName, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        print("Contents of folder deleted: " + folderName)

    def add_detection_images(self, folderName):
        image = "detectionImages/" + str(self.id) + ".jpeg"

    def log_fod(self):
        self.insertToDb(self.db_path)
        self.clearLog()
        self.writeToLog("Log.txt")
        # add detection image to folder function #cache

        # store images in seperate folder
        # path to images stored in database

    def read_all_db(self):
        try:
            conn = sqlite3.connect('detections.db')
            cursor = conn.cursor()

            data = cursor.execute(""" SELECT * FROM detections;""")
            data = data.fetchall()
            print(data)
            conn.commit()
            conn.close()
            return data

        except sqlite3.Error as e:
            print(e)

    def read_map_points(self):
        try:
            conn = sqlite3.connect('detections.db')
            cursor = conn.cursor()
            # get uncleaned up and last 24hrs
            data = cursor.execute(""" SELECT * FROM `detections`""")
            # data = cursor.execute(""" SELECT * FROM `detections` WHERE timestamp >= datetime('now','-24 hours')""")

            data = data.fetchall()
            conn.commit()
            conn.close()
            return data

        except sqlite3.Error as e:
            print(e)


if __name__ == '__main__':
    ld = LogDetection()
    print(ld.read_map_points())
