#!/usr/bin/env python3
"""Merge individual section part files into the final daily JSON for ai-news-daily."""
import json
import sys
import os
from datetime import date as dt_date

date_str = sys.argv[1] if len(sys.argv) > 1 else dt_date.today().strftime('%Y-%m-%d')

HOME = os.path.expanduser('~')
WORKSPACE = os.path.join(HOME, '.openclaw', 'workspace', 'ai-news-daily')
data_dir = os.path.join(WORKSPACE, 'data')
parts_dir = os.path.join(data_dir, 'parts')

# Ensure directories exist
os.makedirs(parts_dir, exist_ok=True)

sections = [
    'insights', 'papers', 'xPosts', 'discord', 'github', 'hn',
    'reddit', 'tools', 'agent', 'siliconValley', 'mainlandChina'
]

result = {"date": date_str}
missing = []
total_items = 0

for section in sections:
    part_file = os.path.join(parts_dir, f'{date_str}_{section}.json')
    if os.path.exists(part_file):
        try:
            with open(part_file, 'r', encoding='utf-8') as f:
                part = json.load(f)
            items = part.get('items', [])
            result[section] = items
            total_items += len(items)
            print(f'  ✅ {section}: {len(items)} items from {part_file}')
        except (json.JSONDecodeError, IOError) as e:
            print(f'  ⚠️  {section}: invalid JSON in {part_file} ({e})')
            result[section] = []
            missing.append(section)
    else:
        print(f'  ❌ {section}: missing file {part_file}')
        result[section] = []
        missing.append(section)

# Write final merged JSON
output = os.path.join(data_dir, f'{date_str}.json')
with open(output, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

section_count = sum(1 for v in result.values() if isinstance(v, list) and len(v) > 0)
print(f'\n📊 Merged: {section_count}/11 sections, {total_items} total items → {output}')

if missing:
    print(f'⚠️  Missing sections ({len(missing)}): {", ".join(missing)}')
    # Still exit 0 so the pipeline continues with partial data
    sys.exit(0)
else:
    print('✅ All 11 sections present.')
    sys.exit(0)