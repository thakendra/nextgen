with open('build_from_sanity.py', 'r', encoding='utf-8') as f:
    content = f.read()

svg_pin = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>'

# Replace emoji references in card loc spans (2-col rows)
old1 = '>&amp;#128205; {p["loc"]}<'
new1 = '>' + svg_pin + '{p["loc"]}<'
content = content.replace(old1, new1)

# Replace emoji references in card loc spans (1-col fallback)
old2 = '>&amp;#128205; {chunk[0]["loc"]}<'
new2 = '>' + svg_pin + '{chunk[0]["loc"]}<'
content = content.replace(old2, new2)

with open('build_from_sanity.py', 'w', encoding='utf-8') as f:
    f.write(content)

remaining = content.count('128205')
print(f'Done. Remaining 128205 references: {remaining}')
