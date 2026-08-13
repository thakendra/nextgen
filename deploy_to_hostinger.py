import ftplib
import os
import ssl

import server_config

FTP_HOST = server_config.FTP_HOST
FTP_USER = server_config.FTP_USER  # Hostinger account username
FTP_PASS = server_config.ftp_password()

# We will check if we can upload modified files
def upload_file(ftp, local_path, remote_path):
    with open(local_path, "rb") as f:
        ftp.storbinary(f"STOR {remote_path}", f)
    print(f"Uploaded: {remote_path}")
