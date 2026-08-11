# -*- coding: utf-8 -*-
"""One-off repair for meta text on pages the Sanity build never regenerates.

Category pages, blog, careers, the SEO landing pages and the orphaned project
files left behind by old slugs all carry hand-written meta descriptions. Some
still hold mojibake and most are shorter than search engines want.

Pages generated from Sanity are cleaned in build_from_sanity.py instead, so
running this afterwards is harmless — their copy is already tidy.

    python clean_static_meta.py
"""
import glob
import html as ht
import io
import os
import re

from copy_clean import clean_text, expand_description, MIN_LEN

BASE = os.path.dirname(os.path.abspath(__file__))

META_PATTERNS = (
    re.compile(r'(<meta name="description" content=")(.*?)("\s*/?>)', re.S),
    re.compile(r'(<meta property="og:description" content=")(.*?)("\s*/?>)', re.S),
    re.compile(r'(<meta name="twitter:description" content=")(.*?)("\s*/?>)', re.S),
)


def rewrite(html):
    """Clean, and where needed lengthen, every description meta on the page."""
    changed = False

    for pattern in META_PATTERNS:
        m = pattern.search(html)
        if not m:
            continue
        raw = m.group(2)
        text = clean_text(ht.unescape(raw))
        if len(text) < MIN_LEN:
            text = expand_description(text)
        # Only " and & need escaping inside a double-quoted attribute.
        escaped = text.replace('&', '&amp;').replace('"', '&quot;')
        if escaped != raw:
            html = html[:m.start()] + m.group(1) + escaped + m.group(3) + html[m.end():]
            changed = True

    return html, changed


def main():
    files = sorted(glob.glob(os.path.join(BASE, '*.html')) +
                   glob.glob(os.path.join(BASE, 'blogs', '*.html')))
    touched = 0
    for path in files:
        html = io.open(path, encoding='utf-8').read()
        new, changed = rewrite(html)
        if changed:
            io.open(path, 'w', encoding='utf-8').write(new)
            touched += 1
            print('  cleaned:', os.path.relpath(path, BASE))
    print('pages updated: %d / %d' % (touched, len(files)))


if __name__ == '__main__':
    main()
