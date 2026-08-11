import os, re

base_dir = r"D:\nextgen"
cat_files = [
    "architecture.html", "interiors.html", "residential.html", "commercial.html",
    "hospitality.html", "healthcare.html", "education.html", "workplace.html",
    "club-resort.html", "dpr-landscaping.html"
]

for fname in cat_files:
    fpath = os.path.join(base_dir, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Normalize projects-wrap section
    pattern = r'<div class="projects-wrap">[\s\S]*?(?=(?:<!--\s*SEO|<section class="seo|<footer|<div class="footer))'
    clean_wrap = '<div class="projects-wrap">\n  <div class="projects-grid">\n  </div>\n</div>\n\n'
    content = re.sub(pattern, clean_wrap, content, count=1)
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Cleaned {fname}")
