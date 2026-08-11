import urllib.request
import urllib.parse
import json

query = """*[_type == "project"] | order(_createdAt desc){
    title,
    "slug": slug.current,
    mainCategory,
    subCategory,
    featuredOnHome,
    "thumbnailUrl": coalesce(thumbnail.asset->url, thumbnail.asset.asset->url, galleryImages[0].asset.asset->url, galleryImages[0].asset->url)
}"""

url = f"https://gpyk0ky0.api.sanity.io/v2021-10-21/data/query/production?query={urllib.parse.quote(query)}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    docs = json.loads(res.read().decode())['result']
    print(f"Total projects in Sanity: {len(docs)}")
    for d in docs:
        print(f"• Title: {d.get('title')} | Main: {d.get('mainCategory')} | Sub: {d.get('subCategory')} | Featured: {d.get('featuredOnHome')} | Thumb: {bool(d.get('thumbnailUrl'))}")
