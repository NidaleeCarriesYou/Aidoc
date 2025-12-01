import os

MUTATED_DICOM_FOLDER = r"..\DICOM_MUTATED"

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path) 
        print(f"Folder created: {os.path.abspath(folder_path)}")
    else:
        print(f"Folder already exists: {os.path.abspath(folder_path)}")


#create_folder(MUTATED_DICOM_FOLDER)
