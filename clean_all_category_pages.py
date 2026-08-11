import os
import re

CATEGORY_FILES = [
    "architecture.html",
    "interiors.html",
    "residential.html",
    "hospitality.html",
    "commercial.html",
    "healthcare.html",
    "education.html",
    "workplace.html",
    "club-resort.html",
    "dpr-landscaping.html"
]

BASE_DIR = r"D:\nextgen"

for fname in CATEGORY_FILES:
    fpath = os.path.join(BASE_DIR, fname)
    if not os.path.exists(fpath):
        continue
        
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Clean projects-grid to be empty: <div class="projects-grid"></div>
    # Using regex to match from <div class="projects-grid"> to the matching closing </div> before </div>\n</div> or inquiry/contact
    cleaned_content = re.sub(
        r'(<div class="projects-grid">)[\s\S]*?(</div>\s*</div>\s*(?:<div class="inquiry-band"|<div class="contact-strip"|<section|<footer))',
        r'\1\n  \2',
        content
    )
    
    # If regex didn't trigger, also check standard pattern
    if '<div class="projects-grid">' in cleaned_content:
        parts = cleaned_content.split('<div class="projects-grid">')
        if len(parts) == 2:
            # Find the closing </div> of projects-wrap
            wrap_parts = parts[1].split('</div>\n</div>', 1)
            if len(wrap_parts) == 2:
                cleaned_content = parts[0] + '<div class="projects-grid">\n  </div>\n</div>' + wrap_parts[1]

    # 2. Ensure sanity-integration.js is included before </body>
    if 'sanity-integration.js' not in cleaned_content:
        cleaned_content = cleaned_content.replace('</body>', '<script src="sanity-integration.js"></script>\n</body>')
        
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(cleaned_content)
        
    print(f"Cleaned {fname}")

print("All category pages cleaned successfully!")
