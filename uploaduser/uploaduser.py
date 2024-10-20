import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime
import random
import string

# Initialize Firebase
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to generate random alphanumeric string of length n
def generate_id(n):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=n))

# Read CSV file
df = pd.read_csv("users.csv")

# Fixed company ID to be added to all records
company_id = "eSJY7B4N1Ifyu4Gk3H8E"

# Iterate over each row and insert into Firebase
for index, row in df.iterrows():
    print("Processing...")
    # Generate unique document ID
    document_id = generate_id(20)  # Adjust the length of the ID as needed

    data = {
        "clientid": document_id,  # Insert the generated document_id as clientid
        "companyid": company_id,  # Add the fixed company ID to each record
        "name": f"{row['firstname']} {row['lastname']}",
        "email": row['email'] if not pd.isna(row['email']) else None,
        "phone_number": row['phone_number'].replace("'", "").replace("+", "") if not pd.isna(row['phone_number']) else None,
        "label": row['label'] if not pd.isna(row['label']) else None,
        "created_time": datetime.strptime(row['created_time'], "%m/%d/%y %H:%M"),
        "num_of_purchase": int(row['num_of_purchase']) if not pd.isna(row['num_of_purchase']) else None,
        "spent": float(row['spent'][1:]) if not pd.isna(row['spent']) else None,
        "last_activity": row['last_activity'],
        "last_activity_time": datetime.strptime(row['last_activity_time'], "%m/%d/%y %H:%M")
    }

    db.collection("client").document(document_id).set(data)

print("Data inserted into Firebase.")
