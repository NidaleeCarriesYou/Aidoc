import os
import time
import random
import string
from datetime import datetime
import uuid
import pydicom
import requests
from helpers.delete_studies import delete_studies
from helpers.create_folder import create_folder
from helpers.upload_file_to_orthanc import upload_file_to_orthanc


ORTHANC_URL = "http://127.0.0.1:8042"
ORIGINAL_DICOM_FOLDER = r"..\DICOM" 
MUTATED_DICOM_FOLDER = r"..\DICOM_MUTATED"
LOGS_DIR = r"logs"
MUTATED_DICOM_FOLDER_absolute_path = os.path.abspath(MUTATED_DICOM_FOLDER)
PATIENT_NAME = "Eyal Meridan"

time.sleep(2)

### prerequisites ###
delete_studies(ORTHANC_URL)
create_folder(LOGS_DIR)
create_folder(MUTATED_DICOM_FOLDER_absolute_path)

time.sleep(2)

print("DICOM Directory is : " + os.path.abspath(ORIGINAL_DICOM_FOLDER) )
print("Mutated DICOM Directory is : " + MUTATED_DICOM_FOLDER_absolute_path )
print("Patient is : " + PATIENT_NAME )
print("Starting Script!")


time.sleep(5)

# === 2. Modify local DICOM files ===
for filename in os.listdir(ORIGINAL_DICOM_FOLDER):

    filepath = os.path.abspath(os.path.join(ORIGINAL_DICOM_FOLDER, filename))
    print("Filename is: " + filepath)
    try:
        ds = pydicom.dcmread(filepath)
        print(f"File {filepath} read successfully.")
    except Exception as e:
        print(f"Failed to read {filepath}: {e}")
        with open("logs\errors.log", "a") as log_file:
            log_file.write(f"{datetime.now()} - Failed to read {filepath}: {e}\n")
        continue

    # a. Update StudyDate and StudyTime
    now = datetime.now()
    ds.StudyDate = now.strftime("%Y%m%d")
    ds.StudyTime = now.strftime("%H%M%S")

    # b. Random Accession Number (8 digits)
    ds.AccessionNumber = ''.join(random.choices(string.digits, k=8))

    # c. Generate new StudyInstanceUID
    ds.StudyInstanceUID = pydicom.uid.generate_uid()

    # d. Custom Study Description
    ds.StudyDescription = f"Aidoc Candidate Test - {PATIENT_NAME}"

    # Save modified DICOM to a temporary file
    temp_path = os.path.join(MUTATED_DICOM_FOLDER, "modified_" + filename)
    ds.save_as(temp_path)

    try:
        upload_file_to_orthanc(ORTHANC_URL,temp_path,filename)
    except Exception as e:
        print(f"Failed to upload file to Orthanc!, File: {filepath}: {e}")
        with open(r"logs\errors.log", "a") as log_file:
            log_file.write(f"{datetime.now()} - Failed to upload file to Orthanc!, File: {filepath}: {e}\n")
        continue
    


