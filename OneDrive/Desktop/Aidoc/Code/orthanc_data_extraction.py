import requests
import os
from datetime import datetime

# כתובת Orthanc שלך
ORTHANC_URL = "http://127.0.0.1:8042"
clean_orthanc_url = ORTHANC_URL.replace("http://", "").replace("https://", "")

# פקודת ה־API לשליפת כל המחקרים
studies = requests.get(f"{ORTHANC_URL}/studies").json()

# קובץ HTML לפלט
html_file = "orthanc_studies.html"

html_content = """
<html>
<head>
    <title>Orthanc Studies</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid black; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
<h2>Orthanc Studies</h2>
<table>
<tr>
<th>Accession Number</th>
<th>Study Description</th>
<th>Study Date</th>
<th>Open in RadiAnt</th>
</tr>
"""

for study_id in studies:
    study = requests.get(f"{ORTHANC_URL}/studies/{study_id}").json()
    accession = study.get("MainDicomTags", {}).get("AccessionNumber", "")
    description = study.get("MainDicomTags", {}).get("StudyDescription", "")
    study_date = study.get("MainDicomTags", {}).get("StudyDate", "")

    if study_date:
        try:
            study_date = datetime.strptime(study_date, "%Y%m%d").strftime("%Y-%m-%d")
        except:
            pass

    radiant_link = f"dicom://{clean_orthanc_url}/studies/{study_id}"

    html_content += f"""
    <tr>
        <td>{accession}</td>
        <td>{description}</td>
        <td>{study_date}</td>
        <td><a href="{radiant_link}">Open</a></td>
    </tr>
    """

html_content += """
</table>
</body>
</html>
"""

# Save to file
with open(html_file, "w") as f:
    f.write(html_content)

print(f"HTML file created: {os.path.abspath(html_file)}")
