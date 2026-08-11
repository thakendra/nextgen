# -*- coding: utf-8 -*-
"""Tell Bing/Yandex which URLs changed, via the IndexNow protocol.

Without this, a newly published project page waits days for a crawler to
notice it. IndexNow gets it looked at in minutes.

Ownership is proved by hosting KEY at https://nextgeninterior.com/<KEY>.txt —
that file must be deployed before the first ping, or the API answers 403.

URLs come from sitemap.xml, so whatever the build considers public is exactly
what gets submitted.

    python ping_indexnow.py            # submit every URL in the sitemap
    python ping_indexnow.py --dry-run  # print the payload, send nothing
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

KEY = "379f8581522c55333d2da688aa273a29"
HOST = "nextgeninterior.com"
ENDPOINT = "https://api.indexnow.org/indexnow"
BASE = os.path.dirname(os.path.abspath(__file__))

# IndexNow caps a single submission at 10,000 URLs.
MAX_URLS = 10000


def sitemap_urls():
    path = os.path.join(BASE, "sitemap.xml")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return re.findall(r"<loc>\s*(.*?)\s*</loc>", f.read())


def submit(urls, dry_run=False):
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": "https://%s/%s.txt" % (HOST, KEY),
        "urlList": urls[:MAX_URLS],
    }

    if dry_run:
        print(json.dumps(payload, indent=2)[:800])
        return True

    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            # 200 = accepted, 202 = accepted but key still being verified.
            print("IndexNow: submitted %d URLs (HTTP %d)" % (len(payload["urlList"]), res.status))
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")[:200]
        if e.code == 403:
            print("IndexNow: 403 — key file not reachable at %s. "
                  "Deploy %s.txt to the site root first." % (payload["keyLocation"], KEY))
        else:
            print("IndexNow: HTTP %d — %s" % (e.code, body))
    except Exception as e:
        print("IndexNow: skipped (%s)" % e)
    return False


def main():
    urls = sitemap_urls()
    if not urls:
        print("IndexNow: no URLs found in sitemap.xml, nothing to submit.")
        return
    submit(urls, dry_run="--dry-run" in sys.argv)


if __name__ == "__main__":
    main()
