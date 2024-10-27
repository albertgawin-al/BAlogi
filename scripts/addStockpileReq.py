import firebase_admin
from firebase_admin import credentials, firestore

# Initialize the Firebase Admin SDK
cred = credentials.Certificate('serviceKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to send items_dict to Firebase
def send_to_firebase(itemsReq, group_name):
    try:
        collection_ref = db.collection("group").document(group_name)
        collection_ref.update({'itemsReq': itemsReq})
        print("Data sent to Firebase successfully.")
    except Exception as e:
        print("An error occurred while sending data to Firebase.")
        print(e)

# Your existing code
def parse_items_ids(file_content):
    lines = file_content.strip().split('\n')
    numbers = []
    for line in lines:
        parts = line.split('\t')
        for part in parts:
            if part.strip().isdigit():
                numbers.append(int(part.strip()))
    return numbers

def parse_wzor(file_content):
    lines = file_content.strip().split('\n')
    quantities = []
    for line in lines[1:]:
        parts = line.split('\t')
        quantities.append([part.strip() for part in parts])
    return quantities

def create_items_dict(items_ids_content, wzor_content):
    items_ids = parse_items_ids(items_ids_content)
    quantities = parse_wzor(wzor_content)
    items_dict = {str(item_id): 0 for item_id in items_ids}
    flat_quantities = [int(q) for row in quantities for q in row if q.isdigit()]
    for item_id, quantity in zip(items_ids, flat_quantities):
        items_dict[str(item_id)] = quantity
    # Remove items with a value of zero
    items_dict = {k: v for k, v in items_dict.items() if v != 0}
    return items_dict

with open('scripts/stockpileIds.txt', 'r') as f:
    items_ids_content = f.read()

with open('scripts/stockpileReq.txt', 'r') as f:
    wzor_content = f.read()

items_dict = create_items_dict(items_ids_content, wzor_content)
send_to_firebase(items_dict, "Broodytown")
