import ftplib
import os
import ssl

FTP_HOST = "srv1046530.hstgr.cloud"
FTP_USER = "u324089851" # Usually the username on hostinger or we check environment/logs
FTP_PASS = "UbSMVZUfEYRFHn5@M9y#"

# We will check if we can upload modified files
def upload_file(ftp, local_path, remote_path):
    with open(local_path, "rb") as f:
        ftp.storbinary(f"STOR {remote_path}", f)
    print(f"Uploaded: {remote_path}")
