import paramiko
import os
import posixpath
import glob

HOST = "srv1046530.hstgr.cloud"
USER = "root"
PASS = "UbSMVZUfEYRFHn5@M9y#"
REMOTE_DIR = "/var/www/nextgen"
LOCAL_DIR = r"D:\nextgen"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, username=USER, password=PASS, timeout=15)

sftp = client.open_sftp()
print("Connected to Hostinger!")

# Base files to always sync
FILES_TO_SYNC = [
    "sanity-integration.js",
    "site-common.css",
    "interiors.html",
    "residential.html",
    "architecture.html",
    "hospitality.html",
    "commercial.html",
    "healthcare.html",
    "education.html",
    "workplace.html",
    "club-resort.html",
    "dpr-landscaping.html",
    "gallery-page.js",
    "gallery-page.css",
    "sitemap.xml",
    "robots.txt"
]

# Find all HTML files in the root directory
for html_file in glob.glob(os.path.join(LOCAL_DIR, "*.html")):
    base = os.path.basename(html_file)
    if base not in FILES_TO_SYNC:
        FILES_TO_SYNC.append(base)

for filename in FILES_TO_SYNC:
    local_path = os.path.join(LOCAL_DIR, filename)
    if os.path.exists(local_path):
        remote_path = posixpath.join(REMOTE_DIR, filename)
        try:
            sftp.put(local_path, remote_path)
            print(f"Uploaded: {filename}")
        except Exception as e:
            print(f"Failed {filename}: {e}")

sftp.close()
client.close()
print("All files synchronized successfully to Hostinger!")
