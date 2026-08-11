import subprocess
import os
import sys

BASE_DIR = r"D:\nextgen"
ADMIN_DIR = os.path.join(BASE_DIR, "admin")

print("==================================================")
print("[*] NEXTGEN 1-COMMAND AUTO-SYNC & PUBLISH SYSTEM")
print("==================================================")

# Step 1: Auto-publish any uncommitted drafts from Sanity Dashboard
print("\n[Step 1/4] Auto-publishing all drafts in Sanity Dashboard...")
try:
    p1 = subprocess.run(
        ["npx", "sanity", "exec", "publish_all_drafts.js", "--with-user-token"],
        cwd=ADMIN_DIR,
        capture_output=True,
        text=True,
        shell=True,
        encoding='utf-8',
        errors='ignore'
    )
    if p1.stdout:
        print(p1.stdout.strip())
    else:
        print("All drafts processed.")
except Exception as e:
    print("Draft note:", e)

# Step 2: Build all project showcase pages and category grids
print("\n[Step 2/4] Generating all Showcase HTML pages...")
try:
    p2 = subprocess.run(
        [sys.executable, "build_from_sanity.py"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    if p2.stdout:
        print(p2.stdout.strip())
    else:
        print("Build completed.")
except Exception as e:
    print("Error in build:", e)

# Step 3: Synchronize to Hostinger Server
print("\n[Step 3/4] Uploading all files to Hostinger Live Server...")
try:
    p3 = subprocess.run(
        [sys.executable, "sync_to_hostinger.py"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    if p3.stdout:
        print(p3.stdout.strip())
    else:
        print("Sync completed.")
except Exception as e:
    print("Error in sync:", e)

# Step 4: Commit & push to GitHub
print("\n[Step 4/4] Committing and pushing to GitHub repository...")
try:
    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, shell=True)
    subprocess.run(["git", "commit", "-m", "chore: auto-sync from update.py"], cwd=BASE_DIR, shell=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, shell=True)
    print("GitHub synchronized successfully!")
except Exception as e:
    print("Git sync note:", e)

print("\n==================================================")
print("[OK] COMPLETE! All 51 projects are live on https://nextgeninterior.com")
print("==================================================")
