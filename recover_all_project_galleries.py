import subprocess
import re
import json
import os
import urllib.parse

BASE_DIR = r"D:\nextgen"
OUTPUT_NDJSON = os.path.join(BASE_DIR, "admin", "all_projects.ndjson")

# Excluded non-project pages
EXCLUDED = {
    'index.html', 'architecture.html', 'interiors.html', 'residential.html', 
    'commercial.html', 'hospitality.html', 'healthcare.html', 'education.html', 
    'workplace.html', 'club-resort.html', 'dpr-landscaping.html', 'blog.html', 
    'careers.html', 'hotel-interior-design-nepal.html', 'hotel-resort-architecture-nepal.html',
    'hotel-resort-designer-nepal.html'
}

# Get list of all html files in repo
p = subprocess.run(["git", "ls-tree", "--name-only", "HEAD~2"], capture_output=True, text=True, cwd=BASE_DIR)
all_files = [f.strip() for f in p.stdout.splitlines() if f.endswith('.html') and f not in EXCLUDED]

print(f"Found {len(all_files)} project HTML files from git history.")

all_docs = []

for filename in all_files:
    slug = filename.replace('.html', '').strip()
    
    # Read the original pristine content from git before overwrite
    res = subprocess.run(["git", "show", f"HEAD~2:{filename}"], capture_output=True, text=True, cwd=BASE_DIR, errors='ignore')
    content = res.stdout
    if not content:
        continue
        
    # Extract Title
    title_match = re.search(r'<title>(.*?)(?:—|&mdash;|-)', content)
    title = title_match.group(1).strip() if title_match else slug.replace('-', ' ').title()
    
    # Extract Description
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
    desc = desc_match.group(1).strip() if desc_match else f"{title} by NextGen Interiors."
    
    # Extract Eyebrow
    eyebrow_match = re.search(r'<div class="hero-eyebrow">(.*?)</div>', content)
    eyebrow = eyebrow_match.group(1).replace('&middot;', '·').strip() if eyebrow_match else "Interior Design"
    
    # Extract Location
    loc_match = re.search(r'<span class="meta-label">Location</span><span class="meta-val">(.*?)</span>', content)
    location = loc_match.group(1).strip() if loc_match else "Kathmandu, Nepal"
    
    # Extract Category
    cat_match = re.search(r'<span class="meta-label">Category</span><span class="meta-val">(.*?)</span>', content)
    category_val = cat_match.group(1).strip() if cat_match else eyebrow
    
    # Determine Main Category & Sub Category
    full_cat_str = (category_val + " " + eyebrow + " " + slug).lower()
    main_cat = "interiors"
    sub_cat = "residential"
    
    if "architecture" in full_cat_str or "exterior" in full_cat_str:
        main_cat = "architecture"
        sub_cat = "residential"
        if "banquet" in full_cat_str:
            sub_cat = "hospitality"
    elif "hotel" in full_cat_str or "cafe" in full_cat_str or "banquet" in full_cat_str or "hospitality" in full_cat_str:
        main_cat = "interiors"
        sub_cat = "hospitality"
    elif "salon" in full_cat_str or "office" in full_cat_str or "venture" in full_cat_str or "commercial" in full_cat_str or "retail" in full_cat_str:
        main_cat = "interiors"
        sub_cat = "commercial"
    elif "skincare" in full_cat_str or "wellness" in full_cat_str or "clinic" in full_cat_str:
        main_cat = "interiors"
        sub_cat = "healthcare"
    elif "residential" in full_cat_str or "home" in full_cat_str or "residence" in full_cat_str or "villa" in full_cat_str:
        main_cat = "interiors"
        sub_cat = "residential"
        
    # Extract Intro Heading & Text
    intro_h_match = re.search(r'<h2 class="(?:intro-h|s-intro-h).*?>(.*?)</h2>', content, re.DOTALL)
    intro_heading = intro_h_match.group(1).replace('<br>', ' ').strip() if intro_h_match else f"A REFINED {title.upper()}"
    
    intro_p_match = re.search(r'<p class="intro-p">(.*?)</p>', content, re.DOTALL)
    if not intro_p_match:
        intro_p_match = re.search(r'<div class="s-intro-body.*?>(.*?)</div>', content, re.DOTALL)
    intro_text = re.sub(r'<.*?>', ' ', intro_p_match.group(1)).strip() if intro_p_match else desc
    
    # 1. EXTRACT ALL IMAGES FROM FILE (Galleries/...)
    img_srcs = []
    
    # Check initGallery format
    init_match = re.search(r"initGallery\('(.*?)',\s*(\[.*?\])", content, re.DOTALL)
    if init_match:
        folder = init_match.group(1)
        files_json = init_match.group(2).replace("'", '"')
        try:
            files = json.loads(files_json)
            for f in files:
                f_rel = os.path.join(folder, f) if folder else f
                if f_rel not in img_srcs:
                    img_srcs.append(f_rel)
        except:
            pass
            
    # Check lbImages format: src:'Galleries/...'
    for m in re.finditer(r"src:\s*['\"](Galleries/[^'\"]+)['\"]", content):
        src = m.group(1)
        if src not in img_srcs:
            img_srcs.append(src)
            
    # Check <img src="Galleries/..."
    for m in re.finditer(r'<img[^>]+src=["\'](Galleries/[^"\']+)["\']', content):
        src = m.group(1)
        if src not in img_srcs:
            img_srcs.append(src)
            
    # Also check hero image
    hero_match = re.search(r'<div class="hero-img"><img.*?src="(.*?)"', content)
    hero_src = hero_match.group(1).strip() if hero_match else (img_srcs[0] if img_srcs else '')
    
    thumbnail_doc = None
    if hero_src:
        hero_rel = urllib.parse.unquote(hero_src)
        hero_abs = os.path.join(BASE_DIR, hero_rel).replace('\\', '/')
        if os.path.exists(os.path.join(BASE_DIR, hero_rel)):
            thumbnail_doc = {
                "_type": "image",
                "asset": {
                    "_type": "reference",
                    "_sanityAsset": f"image@file:///{hero_abs}"
                }
            }
            
    gallery_docs = []
    # If no inner images found other than hero, use whatever images were in img_srcs
    for idx, f_rel in enumerate(img_srcs[:10]):
        f_unquoted = urllib.parse.unquote(f_rel)
        f_abs = os.path.join(BASE_DIR, f_unquoted).replace('\\', '/')
        if os.path.exists(os.path.join(BASE_DIR, f_unquoted)):
            gallery_docs.append({
                "_key": f"img_{idx+1}",
                "_type": "image",
                "caption": f"{title} Space {idx+1}",
                "asset": {
                    "_type": "reference",
                    "_sanityAsset": f"image@file:///{f_abs}"
                }
            })
            
    clean_id = re.sub(r'[^a-zA-Z0-9_-]', '-', f"project-{slug}")
    doc = {
        "_id": clean_id,
        "_type": "project",
        "title": title,
        "slug": { "_type": "slug", "current": slug },
        "mainCategory": main_cat,
        "subCategory": sub_cat,
        "eyebrow": eyebrow,
        "location": location,
        "intro_heading": intro_heading,
        "intro_text": intro_text,
        "description": desc,
    }
    
    if thumbnail_doc:
        doc["thumbnail"] = thumbnail_doc
    if gallery_docs:
        doc["galleryImages"] = gallery_docs
        
    all_docs.append(doc)
    print(f"[{slug}] Found {len(gallery_docs)} gallery photos.")

print(f"Total projects extracted with all photos: {len(all_docs)}")

with open(OUTPUT_NDJSON, 'w', encoding='utf-8') as f:
    for doc in all_docs:
        f.write(json.dumps(doc) + '\n')

print(f"Saved complete NDJSON to {OUTPUT_NDJSON}")
