import urllib.request
import urllib.parse
import json

query = """*[defined(_type) && (_type == "project" || _id in path("drafts.**"))]{
    _id,
    title,
    "slug": slug.current
}"""

url = f"https://gpyk0ky0.api.sanity.io/v2021-10-21/data/query/production?query={urllib.parse.quote(query)}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode())
    print("Found total:", len(data['result']))
    for p in data['result']:
        print(f" - {p['_id']}: {p.get('title')} ({p.get('slug')})")
