import urllib.request, urllib.parse, json

query = '*[_type == "project" && (slug.current == "surkhet-hotel-exterior" || slug.current == "kawality-banquet-hall")]{title, slug, "gallery": galleryImages[]{ "url": coalesce(asset->url, asset.asset->url) }.url}'
url = f'https://gpyk0ky0.api.sanity.io/v2021-10-21/data/query/production?query={urllib.parse.quote(query)}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode())['result']
    for p in data:
        print("=== " + p['title'] + " ===")
        for img in p.get('gallery') or []:
            print(img)
