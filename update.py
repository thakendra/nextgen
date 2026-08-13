import subprocess
import os
import sys

BASE_DIR = r"D:\nextgen"
ADMIN_DIR = os.path.join(BASE_DIR, "admin")

# Tracks steps that failed, so a broken deploy cannot look like a clean one.
FAILURES = []


def report(step, proc, ok_message):
    """Print a step's real outcome. Anything a sub-script wrote to stderr, and
    any non-zero exit, is surfaced here — a step that fails silently is worse
    than one that fails loudly, because the site then sits at an old version
    while the console says everything worked."""
    if proc.stdout and proc.stdout.strip():
        print(proc.stdout.strip())
    elif proc.returncode == 0:
        print(ok_message)
    if proc.stderr and proc.stderr.strip():
        print(proc.stderr.strip())
    if proc.returncode != 0:
        FAILURES.append(step)
        print("[FAILED] {} exited with code {}.".format(step, proc.returncode))

print("==================================================")
print("[*] NEXTGEN 1-COMMAND AUTO-SYNC & PUBLISH SYSTEM")
print("==================================================")

# Step 1: Auto-publish any uncommitted drafts from Sanity Dashboard
print("\n[Step 1/5] Auto-publishing all drafts in Sanity Dashboard...")
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
    report("Step 1 (publish drafts)", p1, "All drafts processed.")
except Exception as e:
    FAILURES.append("Step 1 (publish drafts)")
    print("Draft note:", e)

# Step 2: Build all project showcase pages and category grids
print("\n[Step 2/5] Generating all Showcase HTML pages...")
try:
    p2 = subprocess.run(
        [sys.executable, "build_from_sanity.py"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    report("Step 2 (build pages)", p2, "Build completed.")
except Exception as e:
    FAILURES.append("Step 2 (build pages)")
    print("Error in build:", e)

# Step 3: Synchronize to Hostinger Server
print("\n[Step 3/5] Uploading all files to Hostinger Live Server...")
try:
    p3 = subprocess.run(
        [sys.executable, "sync_to_hostinger.py"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    report("Step 3 (upload to Hostinger)", p3, "Sync completed.")
except Exception as e:
    FAILURES.append("Step 3 (upload to Hostinger)")
    print("Error in sync:", e)

# Step 4: Tell search engines what changed (runs after the sync, so the pages
# and the ownership key file are already live when the crawler comes looking)
print("\n[Step 4/5] Notifying search engines via IndexNow...")
try:
    p4 = subprocess.run(
        [sys.executable, "ping_indexnow.py"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    report("Step 4 (IndexNow ping)", p4, "IndexNow step finished.")
except Exception as e:
    FAILURES.append("Step 4 (IndexNow ping)")
    print("IndexNow note:", e)

# Step 5: Commit & push to GitHub
print("\n[Step 5/5] Committing and pushing to GitHub repository...")
try:
    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, shell=True)
    subprocess.run(["git", "commit", "-m", "chore: auto-sync from update.py"], cwd=BASE_DIR, shell=True)
    push = subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, shell=True)
    if push.returncode != 0:
        FAILURES.append("Step 5 (git push)")
        print("[FAILED] git push exited with code {}.".format(push.returncode))
    else:
        print("GitHub synchronized successfully!")
except Exception as e:
    FAILURES.append("Step 5 (git push)")
    print("Git sync note:", e)

print("\n==================================================")
if FAILURES:
    # The upload is the step that decides whether the public site changed, so a
    # failure there must never be reported as a completed deploy.
    print("[INCOMPLETE] Finished with errors in: " + ", ".join(FAILURES))
    print("The live site at https://nextgeninterior.com may still show the old version.")
    sys.exit(1)
print("[OK] COMPLETE! Everything is live on https://nextgeninterior.com")
print("==================================================")
