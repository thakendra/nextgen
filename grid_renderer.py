def render_micasa_architecture(projects):
    if not projects:
        return '<div class="wrap" style="padding:40px 0; text-align:center; color:var(--mist);">No Architecture projects featured yet.</div>'
    
    rows = []
    p = projects[:]
    
    # Row 1: Small - Big (2 items)
    if len(p) >= 2:
        r1 = p[:2]
        p = p[2:]
        cards_html = f'''      <a href="{r1[0]['slug']}" class="pm-card pm-r43"><img src="{r1[0]['thumb']}?w=1200&amp;auto=format" alt="{r1[0]['title']}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{r1[0]['title']}</span><span class="pm-loc">&#128205; {r1[0]['loc']}</span></a>
      <a href="{r1[1]['slug']}" class="pm-card pm-r43"><img src="{r1[1]['thumb']}?w=1200&amp;auto=format" alt="{r1[1]['title']}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{r1[1]['title']}</span><span class="pm-loc">&#128205; {r1[1]['loc']}</span></a>'''
        rows.append(f'    <div class="port-grid-micasa pmr-small-big rv vis">\n{cards_html}\n    </div>')
    elif len(p) == 1:
        r1 = p[0]
        p = []
        cards_html = f'''      <a href="{r1['slug']}" class="pm-card pm-r43"><img src="{r1['thumb']}?w=1200&amp;auto=format" alt="{r1['title']}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{r1['title']}</span><span class="pm-loc">&#128205; {r1['loc']}</span></a>'''
        rows.append(f'    <div class="port-grid-micasa pmr-full rv vis">\n{cards_html}\n    </div>')

    # Row 2: 3-column (up to 3 items)
    if len(p) >= 3:
        r2 = p[:3]
        p = p[3:]
        c_html = '\n'.join([f'      <a href="{item["slug"]}" class="pm-card pm-r32"><img src="{item["thumb"]}?w=1200&amp;auto=format" alt="{item["title"]}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{item["title"]}</span><span class="pm-loc">&#128205; {item["loc"]}</span></a>' for item in r2])
        rows.append(f'    <div class="port-grid-micasa pmr-3 rv vis d1">\n{c_html}\n    </div>')
    elif len(p) == 2:
        r2 = p[:2]
        p = []
        c_html = '\n'.join([f'      <a href="{item["slug"]}" class="pm-card pm-r32"><img src="{item["thumb"]}?w=1200&amp;auto=format" alt="{item["title"]}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{item["title"]}</span><span class="pm-loc">&#128205; {item["loc"]}</span></a>' for item in r2])
        rows.append(f'    <div class="port-grid-micasa pmr-half rv vis d1">\n{c_html}\n    </div>')
    elif len(p) == 1:
        r2 = p[0]
        p = []
        c_html = f'      <a href="{r2["slug"]}" class="pm-card pm-r32"><img src="{r2["thumb"]}?w=1200&amp;auto=format" alt="{r2["title"]}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{r2["title"]}</span><span class="pm-loc">&#128205; {r2["loc"]}</span></a>'
        rows.append(f'    <div class="port-grid-micasa pmr-full rv vis d1">\n{c_html}\n    </div>')

    # Row 3: 3-column (up to 3 items)
    if len(p) >= 3:
        r3 = p[:3]
        p = p[3:]
        c_html = '\n'.join([f'      <a href="{item["slug"]}" class="pm-card pm-r43"><img src="{item["thumb"]}?w=1200&amp;auto=format" alt="{item["title"]}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{item["title"]}</span><span class="pm-loc">&#128205; {item["loc"]}</span></a>' for item in r3])
        rows.append(f'    <div class="port-grid-micasa pmr-3 rv vis d2">\n{c_html}\n    </div>')
    elif len(p) > 0:
        c_html = '\n'.join([f'      <a href="{item["slug"]}" class="pm-card pm-r43"><img src="{item["thumb"]}?w=1200&amp;auto=format" alt="{item["title"]}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{item["title"]}</span><span class="pm-loc">&#128205; {item["loc"]}</span></a>' for item in p])
        pmr_class = "pmr-half" if len(p) == 2 else "pmr-full"
        rows.append(f'    <div class="port-grid-micasa {pmr_class} rv vis d2">\n{c_html}\n    </div>')

    return '\n'.join(rows)

def render_micasa_interior(projects):
    if not projects:
        return '<div class="wrap" style="padding:40px 0; text-align:center; color:var(--mist);">No Interior projects featured yet.</div>'
    
    rows = []
    p = projects[:]
    
    # Row 1: Tall Half (2 dramatic hero items)
    if len(p) >= 2:
        r1 = p[:2]
        p = p[2:]
        cards_html = f'''      <a href="{r1[0]['slug']}" class="pm-card pm-tall"><img src="{r1[0]['thumb']}?w=1200&amp;auto=format" alt="{r1[0]['title']}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{r1[0]['title']}</span><span class="pm-loc">&#128205; {r1[0]['loc']}</span></a>
      <a href="{r1[1]['slug']}" class="pm-card pm-tall"><img src="{r1[1]['thumb']}?w=1200&amp;auto=format" alt="{r1[1]['title']}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{r1[1]['title']}</span><span class="pm-loc">&#128205; {r1[1]['loc']}</span></a>'''
        rows.append(f'    <div class="port-grid-micasa pmr-half rv vis">\n{cards_html}\n    </div>')
    elif len(p) == 1:
        r1 = p[0]
        p = []
        cards_html = f'''      <a href="{r1['slug']}" class="pm-card pm-tall"><img src="{r1['thumb']}?w=1200&amp;auto=format" alt="{r1['title']}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{r1['title']}</span><span class="pm-loc">&#128205; {r1['loc']}</span></a>'''
        rows.append(f'    <div class="port-grid-micasa pmr-full rv vis">\n{cards_html}\n    </div>')

    # Row 2: 3-column (3 items)
    if len(p) >= 3:
        r2 = p[:3]
        p = p[3:]
        c_html = '\n'.join([f'      <a href="{item["slug"]}" class="pm-card pm-r43"><img src="{item["thumb"]}?w=1200&amp;auto=format" alt="{item["title"]}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{item["title"]}</span><span class="pm-loc">&#128205; {item["loc"]}</span></a>' for item in r2])
        rows.append(f'    <div class="port-grid-micasa pmr-3 rv vis d1">\n{c_html}\n    </div>')
    elif len(p) == 2:
        r2 = p[:2]
        p = []
        c_html = '\n'.join([f'      <a href="{item["slug"]}" class="pm-card pm-r43"><img src="{item["thumb"]}?w=1200&amp;auto=format" alt="{item["title"]}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{item["title"]}</span><span class="pm-loc">&#128205; {item["loc"]}</span></a>' for item in r2])
        rows.append(f'    <div class="port-grid-micasa pmr-half rv vis d1">\n{c_html}\n    </div>')
    elif len(p) == 1:
        r2 = p[0]
        p = []
        c_html = f'      <a href="{r2["slug"]}" class="pm-card pm-r43"><img src="{r2["thumb"]}?w=1200&amp;auto=format" alt="{r2["title"]}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{r2["title"]}</span><span class="pm-loc">&#128205; {r2["loc"]}</span></a>'
        rows.append(f'    <div class="port-grid-micasa pmr-full rv vis d1">\n{c_html}\n    </div>')

    # Row 3: Big - Small (2 items)
    if len(p) >= 2:
        r3 = p[:2]
        p = p[2:]
        cards_html = f'''      <a href="{r3[0]['slug']}" class="pm-card pm-std"><img src="{r3[0]['thumb']}?w=1200&amp;auto=format" alt="{r3[0]['title']}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{r3[0]['title']}</span><span class="pm-loc">&#128205; {r3[0]['loc']}</span></a>
      <a href="{r3[1]['slug']}" class="pm-card pm-std"><img src="{r3[1]['thumb']}?w=1200&amp;auto=format" alt="{r3[1]['title']}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{r3[1]['title']}</span><span class="pm-loc">&#128205; {r3[1]['loc']}</span></a>'''
        rows.append(f'    <div class="port-grid-micasa pmr-big-small rv vis d2">\n{cards_html}\n    </div>')
    elif len(p) == 1:
        r3 = p[0]
        p = []
        cards_html = f'''      <a href="{r3['slug']}" class="pm-card pm-std"><img src="{r3['thumb']}?w=1200&amp;auto=format" alt="{r3['title']}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{r3['title']}</span><span class="pm-loc">&#128205; {r3['loc']}</span></a>'''
        rows.append(f'    <div class="port-grid-micasa pmr-full rv vis d2">\n{cards_html}\n    </div>')

    # Row 4: 3-column remaining
    if len(p) > 0:
        c_html = '\n'.join([f'      <a href="{item["slug"]}" class="pm-card pm-r43"><img src="{item["thumb"]}?w=1200&amp;auto=format" alt="{item["title"]}" loading="lazy"/><div class="pm-card-overlay"></div><span class="pm-name">{item["title"]}</span><span class="pm-loc">&#128205; {item["loc"]}</span></a>' for item in p])
        pmr_class = "pmr-3" if len(p) >= 3 else ("pmr-half" if len(p) == 2 else "pmr-full")
        rows.append(f'    <div class="port-grid-micasa {pmr_class} rv vis d3">\n{c_html}\n    </div>')

    return '\n'.join(rows)
