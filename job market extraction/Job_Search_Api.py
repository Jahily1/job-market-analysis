import os  # Standard library to interact with the operating system (files, folders)
import sqlite3  # Built-in library to create and manage the SQL database
import shutil  # Library used for high-level file operations like copying and moving
from datetime import datetime  # Used to get the current date and time
from dotenv import load_dotenv  # Extension to load variables from a .env file
from serpapi import GoogleSearch  # The specific tool to connect to Google Jobs via SerpApi

# --- DYNAMIC PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'jobs_data.db')

load_dotenv()  # Reads the .env file
api_key = os.getenv('SERPAPI_KEY') 

# Create a timestamp string
retrieval_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 1. DATABASE CONFIGURATION
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Execute SQL to create the 'jobs' table (8 COLUMNS TOTAL)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,       -- 1
        title TEXT,                -- 2
        company TEXT,              -- 3
        location TEXT,             -- 4
        posted_at TEXT,            -- 5
        description TEXT,          -- 6
        link TEXT,                 -- 7 
        retrieved_at TEXT          -- 8
    )
''')

# --- List of locations to search specifically ---
target_locations = ["Toronto, Ontario, Canada"]

# 2. EXTRACTION AND STORAGE
for target_city in target_locations:
    print(f"--- Starting search for: {target_city} ---")
    
    params = {
        "engine": "google_jobs",
        "q": "Data Analyst",
        "location": target_city,
        "chips": "date_posted:3days",
        "api_key": api_key
    }

    for page in range(5):
        print(f"[{retrieval_date}] Fetching {target_city} - Page {page + 1}...")
        results = GoogleSearch(params).get_dict()
        jobs = results.get("jobs_results", [])
        
        if not jobs: 
            break
        
        for job in jobs:
            # Extract the Application Link
            apply_options = job.get('apply_options', [])
            job_link = apply_options[0].get('link') if apply_options else "No link available"

            # Organize the job data into a tuple (MUST BE 8 ITEMS)
            job_data = (
                job.get('job_id'),           # 1
                job.get('title'),            # 2
                job.get('company_name'),     # 3
                job.get('location'),         # 4
                job.get('detected_extensions', {}).get('posted_at'), # 5
                job.get('description'),      # 6
                job_link,                    # 7
                retrieval_date               # 8
            )
            
            # INSERT with exactly 8 question marks
            cursor.execute('''
                INSERT OR IGNORE INTO jobs (id, title, company, location, posted_at, description, link, retrieved_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', job_data)

        next_token = results.get("serpapi_pagination", {}).get("next_page_token")
        if not next_token: 
            break
        params["next_page_token"] = next_token

conn.commit()
conn.close()

# 3. BACKUP CREATION
file_date = datetime.now().strftime("%Y-%m-%d")
backup_filename = f"jobs_data_{file_date}.db"
backup_path = os.path.join(BASE_DIR, backup_filename)

try:
    shutil.copy2(db_path, backup_path)
    print(f"Database backup created: {backup_filename}")
except Exception as e:
    print(f"Error creating backup: {e}")

print(f"Data retrieved on {retrieval_date} saved successfully!")
