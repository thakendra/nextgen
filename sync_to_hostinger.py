import paramiko
import os
import posixpath
import glob

import server_config

REMOTE_DIR = "/var/www/nextgen"
LOCAL_DIR = r"D:\nextgen"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(**server_config.ssh_connect_kwargs())

sftp = client.open_sftp()
print("Connected to Hostinger!")

# Base files to always sync
FILES_TO_SYNC = [
    "sanity-integration.js",
    "site-common.css",
    "379f8581522c55333d2da688aa273a29.txt",  # IndexNow ownership key
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

# ...and in the blogs/ subfolder, which the root glob above never reaches.
for html_file in glob.glob(os.path.join(LOCAL_DIR, "blogs", "*.html")):
    rel = posixpath.join("blogs", os.path.basename(html_file))
    if rel not in FILES_TO_SYNC:
        FILES_TO_SYNC.append(rel)

# ...and in the locations/ subfolder.
for html_file in glob.glob(os.path.join(LOCAL_DIR, "locations", "*.html")):
    rel = posixpath.join("locations", os.path.basename(html_file))
    if rel not in FILES_TO_SYNC:
        FILES_TO_SYNC.append(rel)

# ...and images in the images/ subfolder.
for img_ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
    for img_file in glob.glob(os.path.join(LOCAL_DIR, "images", img_ext)):
        rel = posixpath.join("images", os.path.basename(img_file))
        if rel not in FILES_TO_SYNC:
            FILES_TO_SYNC.append(rel)


def ensure_remote_dir(remote_path):
    """mkdir -p for the remote parent directory."""
    parent = posixpath.dirname(remote_path)
    if parent in ("", "/", REMOTE_DIR):
        return
    try:
        sftp.stat(parent)
    except IOError:
        ensure_remote_dir(parent)
        sftp.mkdir(parent)


for filename in FILES_TO_SYNC:
    local_path = os.path.join(LOCAL_DIR, filename.replace("/", os.sep))
    if os.path.exists(local_path):
        remote_path = posixpath.join(REMOTE_DIR, filename)
        try:
            ensure_remote_dir(remote_path)
            sftp.put(local_path, remote_path)
            print(f"Uploaded: {filename}")
        except Exception as e:
            print(f"Failed {filename}: {e}")

sftp.close()
client.close()
print("All files synchronized successfully to Hostinger!")
