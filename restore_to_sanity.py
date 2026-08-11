import json
import os
import subprocess

NDJSON_PATH = r"D:\nextgen\admin\all_projects.ndjson"
RESTORE_NDJSON = r"D:\nextgen\admin\restore_projects.ndjson"

EXCLUDE_SLUGS = [
    "chapur-hotel", "restro-office", "executive-suites", 
    "breakout-lounge", "chapur-boardroom"
]

restored_docs = []
with open(NDJSON_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        if not line.strip():
            continue
        doc = json.loads(line)
        slug = doc.get('slug', {}).get('current', '')
        title = doc.get('title', '')
        
        if slug in EXCLUDE_SLUGS or any(ex in title.lower() for ex in EXCLUDE_SLUGS):
            continue
            
        restored_docs.append(doc)

with open(RESTORE_NDJSON, 'w', encoding='utf-8') as f:
    for doc in restored_docs:
        f.write(json.dumps(doc) + '\n')

print(f"Prepared {len(restored_docs)} projects to restore to Sanity.")

# Run sanity dataset import
p = subprocess.run(
    ["npx", "sanity", "dataset", "import", "restore_projects.ndjson", "production", "--replace"],
    cwd=r"D:\nextgen\admin",
    capture_output=True,
    text=True,
    shell=True
)

print(p.stdout)
if p.stderr:
    print("Stderr:", p.stderr)
