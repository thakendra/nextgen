# -*- coding: utf-8 -*-
"""Bring every page's <title> and meta description inside the lengths Google
actually renders, without rewriting the copy by hand.

Why this exists: an over-long title is truncated with an ellipsis in the SERP,
and an over-long description is the most common reason Google throws away your
description and writes its own snippet from page text. Both were sitewide here
(27 titles over 60 characters, 35 descriptions over 160).

Two rules, both conservative — they shorten, they never invent:

  Titles   Most long titles are 'Primary keyword | Secondary keyword | Brand'.
           The middle segment is dropped first, then the brand is shortened to
           'NextGen', then, only if still over, the last segment is dropped.
           The primary keyword — the first segment — is never touched.

  Descriptions
           Cut on a sentence boundary, keeping whole sentences while they fit.
           If even the first sentence is too long, cut at the last comma before
           the limit and close it with a full stop, so the result always reads
           as a finished sentence rather than a fragment.

og:title / twitter:title and the matching description tags are kept in sync,
because a page whose social tags disagree with its <title> sends Google mixed
signals about which one to trust.

Run `python optimize_meta.py --dry-run` to review every change first.
"""
import glob
import html
import os
import re
import sys

TITLE_MAX = 60
DESC_MAX = 160
DESC_MIN_KEEP = 100   # never cut a description below this; leave it long instead

BRAND_LONG = ['NextGen Interiors & Architects', 'NextGen Interiors and Architects',
              'NextGen Interiors', 'NextGen']
SEPARATORS = ['|', '—', '–', '-']

TITLE_RE = re.compile(r'(<title>)(.*?)(</title>)', re.S | re.I)


def _meta_re(attr, name):
    return re.compile(r'(<meta\s+%s="%s"\s+content=")(.*?)(")' % (attr, re.escape(name)), re.I | re.S)


DESC_RE = _meta_re('name', 'description')
OG_TITLE_RE = _meta_re('property', 'og:title')
OG_DESC_RE = _meta_re('property', 'og:description')
TW_TITLE_RE = _meta_re('name', 'twitter:title')
TW_DESC_RE = _meta_re('name', 'twitter:description')


def split_segments(title):
    """Split a title on its separator, returning (parts, separator)."""
    for sep in SEPARATORS:
        pattern = ' %s ' % sep
        if pattern in title:
            return [p.strip() for p in title.split(pattern)], sep
    return [title], None


def shorten_title(title):
    """Shorten to TITLE_MAX while protecting the primary keyword and the brand."""
    if len(title) <= TITLE_MAX:
        return title

    parts, sep = split_segments(title)
    if sep is None:
        return title  # single phrase — shortening it would mean rewriting it

    joiner = ' %s ' % sep

    # 1. Drop middle segments, keeping the primary keyword and the brand.
    while len(parts) > 2 and len(joiner.join(parts)) > TITLE_MAX:
        parts.pop(1)
    if len(joiner.join(parts)) <= TITLE_MAX:
        return joiner.join(parts)

    # 2. Shorten a long brand tail to just 'NextGen'.
    if len(parts) > 1 and any(parts[-1].startswith(b) for b in BRAND_LONG):
        parts[-1] = 'NextGen'
        if len(joiner.join(parts)) <= TITLE_MAX:
            return joiner.join(parts)

    # 3. Last resort: keep the primary keyword alone. Only worth losing the
    #    brand when the title is meaningfully over — a couple of characters
    #    past the limit costs less than dropping the company name.
    rebuilt = joiner.join(parts)
    if len(rebuilt) > TITLE_MAX + 5 and len(parts[0]) <= TITLE_MAX:
        return parts[0]
    return rebuilt


_SENTENCE_SPLIT = re.compile(r'(?<=[.!?])\s+')


def shorten_description(desc):
    """Trim to DESC_MAX on a sentence boundary; never end mid-thought."""
    desc = desc.strip()
    if len(desc) <= DESC_MAX:
        return desc

    candidates = []

    # Whole sentences while they fit.
    kept = ''
    for sentence in _SENTENCE_SPLIT.split(desc):
        candidate = (kept + ' ' + sentence).strip() if kept else sentence
        if len(candidate) > DESC_MAX:
            break
        kept = candidate
    if kept:
        candidates.append(kept)

    # Cut at the last clause boundary that fits, closed with a full stop. This
    # usually keeps more of the copy than dropping a whole sentence would.
    window = desc[:DESC_MAX]
    cut = max(window.rfind(', '), window.rfind('; '))
    if cut > 0:
        candidates.append(window[:cut].rstrip(' ,;') + '.')

    usable = [c for c in candidates if DESC_MIN_KEEP <= len(c) <= DESC_MAX]
    if usable:
        return max(usable, key=len)   # keep as much of the original as fits
    # Nothing sensible to cut on; leave it long rather than publish a fragment.
    return desc


def apply_to_file(path, dry_run):
    raw = open(path, encoding='utf-8', errors='ignore').read()
    original = raw
    changes = []

    match = TITLE_RE.search(raw)
    if match:
        current = html.unescape(match.group(2))
        shortened = shorten_title(current)
        if shortened != current:
            encoded = html.escape(shortened, quote=False)
            raw = TITLE_RE.sub(lambda m: m.group(1) + encoded + m.group(3), raw, count=1)
            for pattern in (OG_TITLE_RE, TW_TITLE_RE):
                raw = pattern.sub(lambda m: m.group(1) + html.escape(shortened) + m.group(3), raw, count=1)
            changes.append(('title', len(current), len(shortened), current, shortened))

    match = DESC_RE.search(raw)
    if match:
        current = html.unescape(match.group(2))
        shortened = shorten_description(current)
        if shortened != current:
            encoded = html.escape(shortened)
            for pattern in (DESC_RE, OG_DESC_RE, TW_DESC_RE):
                raw = pattern.sub(lambda m: m.group(1) + encoded + m.group(3), raw, count=1)
            changes.append(('desc', len(current), len(shortened), current, shortened))

    if changes and not dry_run and raw != original:
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(raw)
    return changes


def main():
    dry_run = '--dry-run' in sys.argv
    base = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base)
    targets = (sorted(glob.glob('*.html'))
               + sorted(glob.glob('blogs/*.html'))
               + sorted(glob.glob('locations/*.html')))

    touched = 0
    for path in targets:
        changes = apply_to_file(path, dry_run)
        if not changes:
            continue
        touched += 1
        print('\n%s' % path)
        for kind, before_len, after_len, before, after in changes:
            print('  %s %d -> %d' % (kind, before_len, after_len))
            print('    - %s' % before)
            print('    + %s' % after)
    print('\n%s%d of %d pages need meta changes.'
          % ('[dry run] ' if dry_run else '', touched, len(targets)))


if __name__ == '__main__':
    main()
