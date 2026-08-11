SVG_PIN = r'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>'

with open('build_from_sanity.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed = 0
for i, line in enumerate(lines):
    if '128205' in line:
        # Replace the emoji entity + trailing space before loc variable
        if '&#128205; {p["loc"]}' in line:
            lines[i] = line.replace('&#128205; {p["loc"]}', SVG_PIN + '{p["loc"]}')
            fixed += 1
        elif '&amp;#128205; {p["loc"]}' in line:
            lines[i] = line.replace('&amp;#128205; {p["loc"]}', SVG_PIN + '{p["loc"]}')
            fixed += 1
        elif '&#128205; {chunk[0]["loc"]}' in line:
            lines[i] = line.replace('&#128205; {chunk[0]["loc"]}', SVG_PIN + '{chunk[0]["loc"]}')
            fixed += 1

with open('build_from_sanity.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Fixed {fixed} emoji references")
remaining = sum(1 for l in lines if '128205' in l)
print(f"Remaining: {remaining}")
