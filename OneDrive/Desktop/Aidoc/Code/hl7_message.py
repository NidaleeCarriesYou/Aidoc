from hl7apy.core import Message, Segment
from datetime import datetime

msg = Message("ORU_R01")

# MSH Segment
msg.msh.msh_1 = "|"
msg.msh.msh_2 = "^~\&"
msg.msh.msh_7 = datetime.now().strftime("%Y%m%d%H%M%S")
msg.msh.msh_9 = "ORU^R01"
msg.msh.msh_10 = "123456"  # Message Control ID
msg.msh.msh_11 = "P"
msg.msh.msh_12 = "2.5"

# PID Segment (Patient Identification)
pid = Segment("PID")
pid.pid_3 = "PAT12345"        # Patient ID
pid.pid_5 = "Doe^John"        # Patient Name
msg.add(pid)

# OBR Segment (Observation Request)
obr = Segment("OBR")
obr.obr_2 = "ACC98765"        # Accession Number
obr.obr_16 = "Dr. Smith"      # Radiologist Name
msg.add(obr)

# OBX Segment (Observation Result / Report Text)
obx = Segment("OBX")
obx.obx_1 = "1"              
obx.obx_2 = "TX"              
obx.obx_3 = "Report"         
obx.obx_5 = "Findings: No abnormalities detected." 
msg.add(obx)

print(msg.to_er7())


from hl7apy.parser import parse_message

hl7_text = msg.to_er7() 
parsed_msg = parse_message(hl7_text)

# Patient ID
patient_id = parsed_msg.pid.pid_3.value
# Accession Number
accession_number = parsed_msg.OBR.obr_2.value
# Radiologist Name
radiologist = parsed_msg.OBR.obr_16.value
# Report Text
report_text = parsed_msg.OBX.obx_5.value

print("Patient ID:", patient_id)
print("Accession Number:", accession_number)
print("Radiologist:", radiologist)
print("Report Text:", report_text)

