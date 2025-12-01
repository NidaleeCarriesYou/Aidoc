import requests

def upload_file_to_orthanc(ORTHANC_URL, file_path, filename):
    # e. Upload to Orthanc via REST API
    with open(file_path, "rb") as f:
        response = requests.post(f"{ORTHANC_URL}/instances", files={"file": f})
    if response.status_code == 200:
        print(f"Uploaded {filename} successfully.")
    else:
        print(f"Failed to upload {filename}: {response.text}")