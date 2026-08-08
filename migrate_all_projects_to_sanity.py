import os
import json
import glob
import re
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

all_docs = []

html_files = glob.glob(os.path.join(BASE_DIR, "*.html"))

for filepath in html_files:
    filename = os.path.basename(filepath)
    if filename in EXCLUDED:
        continue
        
    slug = filename.replace('.html', '').strip()
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
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
    
    # Extract Hero Image / First Image
    hero_match = re.search(r'<div class="hero-img"><img.*?src="(.*?)"', content)
    hero_src = hero_match.group(1).strip() if hero_match else ''
    
    thumbnail_doc = None
    if hero_src and not hero_src.startswith('http'):
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
            
    # Extract Photos Array (initGallery call)
    init_match = re.search(r"initGallery\('(.*?)',\s*(\[.*?\])", content, re.DOTALL)
    gallery_docs = []
    
    if init_match:
        folder = init_match.group(1)
        files_json = init_match.group(2).replace("'", '"')
        try:
            files = json.loads(files_json)
            for f in files[:10]: # Max 10
                if isinstance(f, str) and not f.startswith('http'):
                    f_rel = os.path.join(folder, f) if folder else f
                    f_abs = os.path.join(BASE_DIR, f_rel).replace('\\', '/')
                    if os.path.exists(os.path.join(BASE_DIR, f_rel)):
                        gallery_docs.append({
                            "_key": f"img_{len(gallery_docs)+1}",
                            "_type": "image",
                            "caption": f"{title} View {len(gallery_docs)+1}",
                            "asset": {
                                "_type": "reference",
                                "_sanityAsset": f"image@file:///{f_abs}"
                            }
                        })
        except:
            pass
            
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

print(f"Extracted {len(all_docs)} total projects from website HTML files.")

with open(OUTPUT_NDJSON, 'w', encoding='utf-8') as f:
    for doc in all_docs:
        f.write(json.dumps(doc) + '\n')

print(f"Successfully generated NDJSON at {OUTPUT_NDJSON}")
