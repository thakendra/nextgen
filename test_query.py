import urllib.request
import urllib.parse
import json

query = """*[_type == "project"]{
    title,
    "thumbnail": coalesce(thumbnail.asset->url, thumbnail.asset.asset->url),
    "gallery": coalesce(galleryImages[].asset.asset->url, galleryImages[].asset->url)
}"""

url = f"https://gpyk0ky0.api.sanity.io/v2021-10-21/data/query/production?query={urllib.parse.quote(query)}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode())
    for p in data['result']:
        print(p['title'], "Thumbnail:", bool(p['thumbnail']), "Gallery count:", len(p.get('gallery') or []))
