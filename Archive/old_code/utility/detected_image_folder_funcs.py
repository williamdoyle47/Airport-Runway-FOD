import os
import shutil


def create_folder(folderName): # creates folder
    exists = os.path.exists(folderName)
    if not exists:
        os.makedirs(folderName)

def delete_folder_contents(folderPath): #deletes folder contents (don't want a huge folder of images)
    for filename in os.listdir(folderPath):
        file_path = os.path.join(folderPath, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print("Contents of folder deleted: " + folderPath)

def clearLog(): #clears the log file
    with open("Log.txt", "a") as text_file:
        text_file.truncate(0)