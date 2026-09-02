# -*- coding: utf-8 -*-
"""Text hygiene for CMS copy on its way into the generated HTML.

Two jobs:

1. `clean_text` repairs text that was pasted into Sanity with a broken
   encoding — UTF-8 bytes that got read as Windows-1252, which is why
   "Lokanthali Residence — Private Home" is stored as
   "Lokanthali Residence â€\u201d Private Home". It also tidies the
   punctuation slips that come with hand entry: doubled spaces, a comma with
   no space after it, stray curly quotes.

2. `expand_description` pads a too-short meta description with category,
   location and service context. Bing flags anything much under ~120
   characters; search engines show up to roughly 155.

Neither function touches the Sanity documents — this is display-time repair,
so the CMS still holds the original text and should be cleaned separately.
"""
import re

# The tell-tale characters of a cp1252/utf-8 mix-up. Cheap pre-check so we
# only attempt the round-trip on text that actually looks broken.
_MOJIBAKE_HINT = re.compile(u'[\u00e2\u00c3\u00c2]')

_MULTISPACE = re.compile(r'[ \t]{2,}')
_COMMA_NO_SPACE = re.compile(r',(?=[^\s\d])')
_SPACE_BEFORE_PUNCT = re.compile(r'\s+([,.;:])')
# A curly quote used as a dash: " ” " between words.
_QUOTE_AS_DASH = re.compile(u'\\s+[\u201c\u201d]\\s+')
# A curly quote left dangling at the start or end of a fragment.
_STRAY_QUOTE = re.compile(u'(?<=\\w)[\u201c\u201d](?=\\s|$)|(?<=^)[\u201c\u201d]\\s*')


def fix_mojibake(text):
    """Undo a cp1252-decoded-as-utf8 round trip, when that is what happened."""
    if not text or not _MOJIBAKE_HINT.search(text):
        return text
    try:
        repaired = text.encode('cp1252').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text  # Not this kind of damage — leave it alone.
    # Only accept the repair if it actually removed the damage.
    return repaired if not _MOJIBAKE_HINT.search(repaired) else text


def clean_text(text):
    """Repair encoding damage and normalise hand-entry punctuation."""
    if not text:
        return text
    out = fix_mojibake(text)
    out = _QUOTE_AS_DASH.sub(u' \u2014 ', out)
    out = _STRAY_QUOTE.sub('', out)
    out = _SPACE_BEFORE_PUNCT.sub(r'\1', out)
    out = _COMMA_NO_SPACE.sub(', ', out)
    out = _MULTISPACE.sub(' ', out)
    return out.strip()


MIN_LEN = 120
MAX_LEN = 155

_SUB_LABEL = {
    'residential': 'residential interiors',
    'commercial': 'commercial interiors',
    'hospitality': 'hospitality design',
    'healthcare': 'healthcare interiors',
    'education': 'education interiors',
    'workplace': 'workplace interiors',
    'club-resort': 'club & resort design',
    'dpr-landscaping': 'DPR & landscape design',
}


def expand_description(desc, title='', location='', main_cat='', sub_cat=''):
    """Pad a short meta description with real context until it reads full.

    Clauses are appended whole — never truncated mid-word — and only while
    they still fit inside MAX_LEN, so the result stays a proper sentence.
    """
    desc = clean_text(desc) or ''
    if len(desc) >= MIN_LEN:
        return desc[:MAX_LEN].rstrip(' ,;-') if len(desc) > MAX_LEN else desc

    if desc and not desc.endswith(('.', '!', '?')):
        desc += '.'

    discipline = 'architecture' if (main_cat or '').lower() == 'architecture' else 'interior design'
    speciality = _SUB_LABEL.get((sub_cat or '').lower(), discipline)

    # Deliberately no location here: the CMS location field often disagrees
    # with the place already named in the description (Balkot vs Maharajgunj),
    # and appending it would put both in the same sentence. The brand name is
    # left out too \u2014 the base description almost always says it already.
    clauses = [
        u'%s \u2014 turnkey design from concept to handover.' % speciality.capitalize(),
        u'See photos, materials and design details.',
        u'Bespoke architecture and interior design across Nepal.',
    ]

    for clause in clauses:
        if len(desc) >= MIN_LEN:
            break
        candidate = (desc + ' ' + clause).strip() if desc else clause
        if len(candidate) <= MAX_LEN:
            desc = candidate

    return desc.strip()
