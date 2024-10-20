import firebase_admin
from firebase_admin import credentials, firestore
import csv

# Initialize Firebase Admin SDK
cred = credentials.Certificate("key.json")  # Replace with your service account key path
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to determine gender based on display_name in Spanish
def determine_gender(display_name):
    # Assuming Spanish names follow the common pattern of gender-specific endings
    if display_name.endswith("a") or display_name.endswith("A"):
        return "Female"
    elif display_name.endswith("o") or display_name.endswith("O"):
        return "Male"
    else:
        return "Unknown"

# Retrieve data from Firebase and save to CSV
users_ref = db.collection(u'users')
users_data = users_ref.stream()

with open('userdata.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["OS", "Verified_Social_Network", "Created_Time", "Modified_Time", "Display_Name", "Photo_URL", "SearchKey", "Uploaded_Products", "Gender"])
    for user in users_data:
        user_data = user.to_dict()
        os = user_data.get('OS', '')
        verified_social_network = user_data.get('verified_social_network', '')
        created_time = user_data.get('created_time', '')
        modified_time = user_data.get('modified_time', '')
        display_name = user_data.get('display_name', '')
        photo_url = user_data.get('photo_url', '')
        search_key = user_data.get('searchKey', '')
        uploaded_products = user_data.get('uploaded_products', '')

        # Determine gender based on display_name
        gender = determine_gender(display_name)

        # Write data to CSV
        writer.writerow([os, verified_social_network, created_time, modified_time, display_name, photo_url, search_key, uploaded_products, gender])

print("Data saved to userdata.csv")
