# 📂 Payroll Automation & Cloud Distribution Tool

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Google Drive](https://img.shields.io/badge/Google%20Drive%20API-v3-green?style=for-the-badge&logo=google-drive&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge)

## 📖 Overview

This desktop application is designed to automate the monthly workflow of payroll distribution. It transforms a manual, time-consuming process into a one-click operation.

**The Problem:** An accountant receives a single "Master PDF" containing payroll slips for all employees. Manually splitting this file and uploading each page to the correct employee's private folder on the cloud is tedious and error-prone.

**The Solution:** This tool parses the PDF, identifies employee references using Regex, splits the files, and uses the Google Drive API to upload them to the correct destination (creating folders automatically if they don't exist).

## ✨ Key Features

* **Smart PDF Parsing:** Uses `pypdf` with a custom normalization engine to detect text (Reference, Month, Year) regardless of formatting inconsistencies or accents.
* **Intelligent Uploads:** Implements a "Check-or-Create" logic. It searches Google Drive for the employee's folder based on their ID. If the folder is missing, it creates it instantly before uploading.
* **Modern GUI:** A clean, responsive interface built with `Tkinter` featuring real-time logging and threaded operations (preventing UI freezing).
* **Secure:** Sensitive API credentials are kept local and excluded from version control.

## 🚀 Project Structure

```text
GestionPaie/
│
├── input/                 # (Optional) Drop your master PDF here
├── output_bulletins/      # Automatically generated individual PDFs
├── logs/                  # Execution logs (.md files) for audit trails
│
├── config.py              # Configuration (Drive Folder ID, Paths)
├── splitter.py            # Logic: PDF text extraction & normalization
├── uploader.py            # Logic: Google Drive OAuth2 authentication & Upload
├── main.py                # GUI Entry point (Tkinter)
│
├── requirements.txt       # Python dependencies
└── README.md              # Documentation


## 🛠️ Local Setup & Configuration Guide

Follow these steps to get the application running on your local machine.

### 1\. Clone and Install

First, get the code and set up the Python environment.

```bash
# Clone the repository
git clone [https://github.com/YOUR-USERNAME/automation-paie-drive.git](https://github.com/YOUR-USERNAME/automation-paie-drive.git)
cd automation-paie-drive

# (Optional) Create a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2\. Google Cloud Platform Setup (Critical)

To allow the script to access your Drive, you need to generate an API Key.

1.  **Create a Project:**
      * Go to the [Google Cloud Console](https://console.cloud.google.com/).
      * Click **New Project** and name it (e.g., "Payroll-Tool").
2.  **Enable the API:**
      * Search for **"Google Drive API"** in the top bar.
      * Click on it and press **Enable**.
3.  **Configure OAuth Consent Screen:**
      * Go to **APIs & Services \> OAuth consent screen**.
      * User Type: Select **External** and click Create.
      * Fill in "App Name" and your email.
      * **Test Users (IMPORTANT):** Scroll to the "Test Users" section, click **+ ADD USERS**, and enter your own Google email address. *If you skip this, you will get a 403 Access Denied error.*
4.  **Create Credentials:**
      * Go to **APIs & Services \> Credentials**.
      * Click **+ CREATE CREDENTIALS** \> **OAuth client ID**.
      * Application type: **Desktop app**.
      * Click Create.
      * **Download JSON:** Click the download icon (⬇️) next to your new client ID.

### 3\. Finalize Configuration

1.  **Credentials File:**
      * Rename the downloaded file to `credentials.json`.
      * Move it to the root folder of this project (next to `main.py`).
2.  **Target Folder Setup:**
      * Create a folder in your Google Drive (e.g., "Payroll 2025").
      * Open that folder in your browser and copy the **Folder ID** from the URL.
          * *URL:* `https://drive.google.com/drive/folders/1A2B3C4D5E6F7G8H9I0J`
          * *ID:* `1A2B3C4D5E6F7G8H9I0J`
3.  **Update Config:**
      * Open `config.py`.
      * Paste your Folder ID:
        ```python
        DRIVE_PARENT_FOLDER_ID = "1A2B3C4D5E6F7G8H9I0J"
        ```

## 🖥️ Usage

1.  Run the application:
    ```bash
    python main.py
    ```
2.  **Step 1:** Click **"Sélectionner & Éclater"**. Select your master PDF. The logs will show the extraction progress.
3.  **Step 2:** Verify the files in the `output_bulletins` folder.
4.  **Step 3:** Click **"Uploader vers Drive"**.
      * *First run:* A browser window will open. Login with your Google account.
      * *Security Warning:* Click **Advanced** \> **Go to [Project Name] (unsafe)** \> **Continue** (This appears because the app is in testing mode).
      * Watch the logs as files are uploaded to the cloud\!

## ❓ Troubleshooting

Common errors and how to fix them:

| Error Message | Cause | Solution |
| :--- | :--- | :--- |
| `Expecting value: line 1 column 1 (char 0)` | The `token.json` or `credentials.json` file is empty/corrupted. | Delete the `token.json` file and restart the app to re-authenticate. |
| `Error 403: access_denied` | The Google App is in "Testing" mode and your email is not authorized. | Go to GCP Console \> **OAuth consent screen** \> **Test Users** and add your email address. |
| `HttpError 404 ... "File not found"` | The Script cannot find the destination folder on Google Drive. | Check `config.py`. Ensure `DRIVE_PARENT_FOLDER_ID` matches the exact ID from your Google Drive folder URL. |

## 🔧 Technical Details

### Robust Text Extraction (`splitter.py`)

PDF text extraction is often messy. To solve this, I implemented a normalization pipeline:

1.  **Strip Accents:** `Référence` becomes `reference`.
2.  **Lower Case:** `M1001` becomes `m1001`.
3.  **Regex Matching:** The script looks for patterns like `reference salarie\s*[:.]?\s*([a-z0-9]+)` to ensure 100% detection rate even if the PDF formatting shifts slightly.

### Drive API Logic (`uploader.py`)

The uploader doesn't just dump files. It performs a query:

```python
query = "name = 'EMPLOYEE_ID' and 'PARENT_ID' in parents..."
```

If the query returns empty, the script creates the folder first. This ensures that files always end up in the correct employee's directory.

## 🛡️ Security

  * `.gitignore` is configured to exclude `credentials.json`, `token.json`, and the `output_bulletins/` folder.
  * **Never** commit your `credentials.json` file to GitHub.

## 👤 Author

**Yassine**

```
```
