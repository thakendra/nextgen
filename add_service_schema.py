# -*- coding: utf-8 -*-
"""Add Service schema to the ten department pages.

Every page on the site already carries BreadcrumbList, project pages carry
CreativeWork and blog posts carry Article — but the department pages, which are
the ones meant to rank for "<service> Nepal" queries, described themselves to
Google as nothing more than a breadcrumb trail. Service schema tells Google what
is actually offered, by whom, and where, which is what makes a page eligible to
be understood as a service rather than a photo gallery.

Safe to re-run: a page that already has a Service block is skipped, so this can
be run again after new department pages are added.
"""
import os
import re

SITE = 'https://nextgeninterior.com'

PROVIDER = {
    'name': 'NextGen Interiors & Architects',
    'url': SITE,
    'telephone': '+977-9849151220',
    'locality': 'Baluwatar, Kathmandu',
}

# name / serviceType come from the primary keyword each page is meant to own,
# so the schema and the page's title agree on what the page is about.
DEPARTMENTS = {
    'architecture.html': (
        'architecture',
        'Architecture & Building Design in Nepal',
        'Architectural design',
        'Architectural design for homes, hotels, institutions and commercial buildings across Nepal — concept design through construction drawings and site supervision.',
    ),
    'interiors.html': (
        'interiors',
        'Interior Design in Kathmandu, Nepal',
        'Interior design',
        'Turnkey interior design for residences, hotels, offices and retail spaces in Kathmandu and across Nepal — space planning, joinery detailing, materials and execution.',
    ),
    'residential.html': (
        'residential',
        'Residential Architecture & Home Interior Design in Nepal',
        'Residential design',
        'Home design and residential interiors across Nepal — private houses, villas, apartments and farmhouses, from planning permission drawings to finished handover.',
    ),
    'commercial.html': (
        'commercial',
        'Commercial Interior Design in Nepal',
        'Commercial interior design',
        'Commercial interiors and fit-outs in Nepal — retail stores, showrooms, clinics, salons and mixed-use commercial spaces designed for footfall and brand.',
    ),
    'hospitality.html': (
        'hospitality',
        'Hotel & Resort Design in Nepal',
        'Hospitality design',
        'Hotel, resort, restaurant and bar design across Nepal — guest room layouts, public areas, banquet halls and full hospitality interior architecture.',
    ),
    'healthcare.html': (
        'healthcare',
        'Healthcare & Clinic Interior Design in Nepal',
        'Healthcare interior design',
        'Healthcare interiors in Nepal — hospitals, clinics, pharmacies and skin care centres designed for hygiene, patient flow and regulatory compliance.',
    ),
    'education.html': (
        'education',
        'School & Educational Architecture in Nepal',
        'Educational facility design',
        'Educational architecture and interiors in Nepal — schools, colleges, libraries and campus buildings designed for daylight, acoustics and safety.',
    ),
    'workplace.html': (
        'workplace',
        'Office & Workplace Interior Design in Kathmandu',
        'Workplace interior design',
        'Office interior design and workplace fit-outs in Kathmandu and across Nepal — corporate offices, coworking spaces and executive cabins.',
    ),
    'club-resort.html': (
        'club-resort',
        'Club & Resort Design in Nepal',
        'Club and resort design',
        'Club, resort and wellness facility design in Nepal — banquet halls, clubhouses, spas and leisure architecture with full interior delivery.',
    ),
    'dpr-landscaping.html': (
        'dpr-landscaping',
        'DPR Consulting & Landscape Design in Nepal',
        'Detailed Project Report and landscape design',
        'Detailed Project Reports (DPR), feasibility studies, master-planning and landscape architecture in Nepal — the upstream work that makes construction run to budget.',
    ),
}

AREA_SERVED = """[
        { "@type": "Country", "name": "Nepal" },
        { "@type": "City", "name": "Kathmandu" },
        { "@type": "City", "name": "Lalitpur" },
        { "@type": "City", "name": "Bhaktapur" },
        { "@type": "City", "name": "Pokhara" },
        { "@type": "City", "name": "Chitwan" }
      ]"""

BLOCK = '''  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Service",
    "@id": "{site}/{slug}#service",
    "name": "{name}",
    "serviceType": "{service_type}",
    "description": "{description}",
    "url": "{site}/{slug}",
    "provider": {{
      "@type": "Organization",
      "name": "{provider_name}",
      "url": "{site}",
      "telephone": "{telephone}",
      "address": {{
        "@type": "PostalAddress",
        "addressLocality": "{locality}",
        "addressCountry": "NP"
      }}
    }},
    "areaServed": {area_served}
  }}
  </script>
'''


def has_service_schema(markup):
    for block in re.findall(r'<script type="application/ld\\+json">(.*?)</script>', markup, re.S):
        if '"Service"' in block:
            return True
    return False


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    added = skipped = 0
    for filename, (slug, name, service_type, description) in DEPARTMENTS.items():
        path = os.path.join(base, filename)
        if not os.path.exists(path):
            print('  ! missing: %s' % filename)
            continue
        markup = open(path, encoding='utf-8', errors='ignore').read()
        if has_service_schema(markup):
            print('  = %-24s already has Service schema' % filename)
            skipped += 1
            continue
        block = BLOCK.format(
            site=SITE, slug=slug, name=name, service_type=service_type,
            description=description, provider_name=PROVIDER['name'],
            telephone=PROVIDER['telephone'], locality=PROVIDER['locality'],
            area_served=AREA_SERVED,
        )
        if '</head>' not in markup:
            print('  ! %s has no </head>' % filename)
            continue
        markup = markup.replace('</head>', block + '</head>', 1)
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(markup)
        print('  + %-24s Service schema added' % filename)
        added += 1
    print('%d added, %d already present.' % (added, skipped))


if __name__ == '__main__':
    main()
