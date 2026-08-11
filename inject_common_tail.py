# -*- coding: utf-8 -*-
"""Stamp the shared page tail (contact + partners + footer + WhatsApp bubble)
into every static HTML page, and point every "Contact" nav link at the page's
own #contact section instead of bouncing the visitor back to the homepage.

Idempotent: re-running replaces the previously injected tail rather than
stacking a second copy. Generated project pages get the same tail from
build_from_sanity.py, so this script does not need to touch them.

    python inject_common_tail.py
"""
import glob
import io
import os

from common_tail import COMMON_TAIL, CSS_LINK

BASE = os.path.dirname(os.path.abspath(__file__))

# Where the old tail can begin, in document order. The earliest one present in
# the page wins, so pages that already have a contact block get it replaced
# rather than duplicated.
START_ANCHORS = (
    '<!-- ===== COMMON TAIL',
    '<section class="contact',
    '<!-- PARTNER BRANDS -->',
    '<section class="partners-section"',
    '<footer class="footer">',
    '<footer',
)


def tail_bounds(html):
    """(start, end) of the region to replace, or None if there's no footer."""
    starts = [html.find(a) for a in START_ANCHORS]
    starts = [i for i in starts if i != -1]
    if not starts:
        return None
    start = min(starts)

    # Stop before the page's own scripts: they run the .rv reveal observer and
    # must stay after the injected markup or the new sections never fade in.
    end = html.find('<script', start)
    if end == -1:
        end = html.find('</body>', start)
    if end == -1:
        return None
    return start, end


def add_css_link(html):
    if 'site-common.css' in html:
        return html, False
    head_end = html.find('</head>')
    if head_end == -1:
        return html, False
    return html[:head_end] + '  ' + CSS_LINK + '\n' + html[head_end:], True


def main():
    files = sorted(glob.glob(os.path.join(BASE, '*.html')) +
                   glob.glob(os.path.join(BASE, 'blogs', '*.html')))

    injected = linked = relinked = skipped = 0
    for path in files:
        name = os.path.relpath(path, BASE)
        html = io.open(path, encoding='utf-8').read()
        original = html

        html, did_link = add_css_link(html)
        if did_link:
            linked += 1

        bounds = tail_bounds(html)
        if bounds:
            start, end = bounds
            html = html[:start] + COMMON_TAIL + '\n' + html[end:]
            injected += 1
        else:
            print('  ! no footer found, skipped tail:', name)

        # Every page now owns a #contact section — keep the link in-page.
        before = html
        html = html.replace('href="/#contact"', 'href="#contact"')
        if html != before:
            relinked += 1

        if html != original:
            io.open(path, 'w', encoding='utf-8').write(html)
        else:
            skipped += 1

    print('tail injected: %d | css linked: %d | contact links localised: %d | unchanged: %d'
          % (injected, linked, relinked, skipped))


if __name__ == '__main__':
    main()
