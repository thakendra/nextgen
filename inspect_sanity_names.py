import urllib.request
import urllib.parse
import json

# Fetch all project documents from Sanity
query = '*[_type == "project"]{_id, title, location, eyebrow, mainCategory, subCategory, featuredOnHome}'
url = f"https://gpyk0ky0.api.sanity.io/v2021-10-21/data/query/production?query={urllib.parse.quote(query)}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

with urllib.request.urlopen(req) as res:
    projects = json.loads(res.read().decode())['result']
    print(f"Loaded {len(projects)} projects from Sanity:")
    for p in projects:
        print(f" - {p.get('_id')}: {p.get('title')} | Loc: {p.get('location')}")
