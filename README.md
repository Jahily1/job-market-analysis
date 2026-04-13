# 📊 Job Market Analysis: Toronto Data Roles
> **Automated Data Extraction Pipeline for Market Intelligence**

## 📌 Project Overview
This project is a dedicated tool for monitoring the **Data Analyst** job market in **Toronto, Ontario**. It automates the gathering of live job postings to help analyze hiring trends, demand for specific technical skills, and salary benchmarks in the Greater Toronto Area (GTA).

---

## 🛠️ Technical Stack
| Category | Tools |
| :--- | :--- |
| **Language** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) |
| **Database** | ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) |
| **API** | SerpApi (Google Jobs) |
| **Libraries** | `python-dotenv`, `google-search-results`, `sqlite3` |

---

## 🚀 Part 1: Job Market Extraction
The core logic resides in the `/job market extraction` directory. This script performs the "heavy lifting" of the data engineering process.

### ✨ Key Features
* **Live Scraping:** Targets "Data Analyst" roles specifically in the Toronto region.
* **Smart Storage:** Uses **SQL logic** (`INSERT OR IGNORE`) to ensure the database remains clean of duplicates.
* **Automated Backups:** Every run generates a timestamped `.db` backup to ensure data security.
* **Deep Metadata:** Captures Title, Company, Location, Description, and the direct Application Link.

### ⚙️ Setup & Installation
1. **Clone the repository**
2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
3. **Configuration:**
- Rename `.env.example` to `.env` inside the `job market extraction` folder.
- Add your **SerpApi Key** inside the `.env` file.
4.  **Run the pipeline:**
   ```bash
   python "job market extraction/Job_Search_Api.py"

   
