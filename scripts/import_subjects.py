from pymongo import MongoClient
import json, os

# --- Connect to MongoDB ---
client = MongoClient("mongodb://localhost:27017/")  
db = client["rating"]  

# --- File paths ---
base_dir = os.path.dirname(__file__)
subjects_json = os.path.join(base_dir, "..", "subjects", "subjects.json")
descriptions_dir = os.path.join(base_dir, "..", "subjects", "descriptions")

# --- Load subjects from JSON ---
with open(subjects_json, encoding="utf-8") as f:
    subjects = json.load(f)

# --- Process each subject ---
for subject in subjects:
    subject_id = subject.get("id")
    desc_path = os.path.join(descriptions_dir, f"{subject_id}.txt")

    # If a description file exists, read it
    if os.path.exists(desc_path):
        with open(desc_path, encoding="utf-8") as desc_file:
            subject["desc"] = desc_file.read().strip()
    else:
        print(f"⚠️ No description file found for: {subject_id}")

    #  Upsert (insert or update) into MongoDB
    db.subjects.update_one(
        {"id": subject_id},
        {"$set": subject},
        upsert=True
    )

print("Subjects with descriptions imported successfully!")