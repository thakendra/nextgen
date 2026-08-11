import urllib.request
import urllib.parse
import json

query = """*[_type == "project"] | order(_createdAt desc){
    _id,
    title,
    "slug": slug.current,
    _createdAt,
    _updatedAt
}"""

url = f"https://gpyk0ky0.api.sanity.io/v2021-10-21/data/query/production?query={urllib.parse.quote(query)}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode())
    docs = data['result']
    print(f"Total projects in Sanity: {len(docs)}\n")
    print("--- User / Dashboard Uploaded Projects ---")
    dashboard_docs = [d for d in docs if not d['_id'].startswith('project-')]
    for d in dashboard_docs:
        print(f"ID: {d['_id']} | Title: {d.get('title')} | Slug: {d.get('slug')}")
        
    print("\n--- System / Old Imported Projects (starting with project-) ---")
    imported_docs = [d for d in docs if d['_id'].startswith('project-')]
    for d in imported_docs:
        print(f"ID: {d['_id']} | Title: {d.get('title')} | Slug: {d.get('slug')}")
