import urllib.request
import urllib.parse
import json

query = """*[_type == "project"]{
    _id,
    title,
    "isDraft": _id in path("drafts.**")
}"""

url = f"https://gpyk0ky0.api.sanity.io/v2021-10-21/data/query/production?query={urllib.parse.quote(query)}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode())
    for p in data['result']:
        print(f"[{'DRAFT' if p.get('isDraft') else 'PUBLISHED'}] {p.get('title')} ({p['_id']})")
