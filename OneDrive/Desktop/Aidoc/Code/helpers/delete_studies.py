import os
import random
import string
from datetime import datetime
import uuid
import pydicom
import requests

ORTHANC_URL = "http://127.0.0.1:8042"
DICOM_FOLDER = r"..\DICOM"  # folder with your local DICOM files

def delete_studies(ORTHANC_URL):
    print("Deleting all studies in Orthanc...")
    try:
        studies = requests.get(f"{ORTHANC_URL}/studies").json()
    except Exception as e:
        print("Failed to get studies from Orthanc! Check if Orthanc is running!")
        return
    for study_id in studies:
        try:
            requests.delete(f"{ORTHANC_URL}/studies/{study_id}")
        except Exception as e:
            print(f"Failed to delete studies from Orthanc!, Check if Orthanc is running! \n Error: {e}")
            with open(r"logs\erors.log", "a") as log_file:
                log_file.write(f"{datetime.now()} - Failed to delete studies from Orthanc!, Check if Orthanc is running! \n Error: {e}")
            failed = 1
    print(f"Deleted {len(studies)} studies.\n")


#delete_studies
