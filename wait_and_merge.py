#!/usr/bin/env python3
"""Wait for all part files to exist, then merge them. Used by the orchestrator."""
import json, os, sys, time

date_str = sys.argv[1] if len(sys.argv) > 1 else None
if not date_str:
    from datetime import date
    date_str = date.today().strftime('%Y-%m-%d')

HOME = os.path.expanduser('~')
parts_dir = os.path.join(HOME, '.openclaw', 'workspace', 'ai-news-daily', 'data', 'parts')
data_dir = os.path.join(HOME, '.openclaw', 'workspace', 'ai-news-daily', 'data')

sections = [
    'insights', 'papers', 'xPosts', 'discord', 'github', 'hn',
    'reddit', 'tools', 'agent', 'siliconValley', 'mainlandChina'
]

# Wait up to 15 minutes for all parts
timeout = 900
interval = 10
waited = 0

while waited < timeout:
    missing = []
    for s in sections:
        f = os.path.join(parts_dir, f'{date_str}_{s}.json')
        if not os.path.exists(f):
            missing.append(s)
    if not missing:
        break
    print(f'Waiting for {len(missing)} sections: {", ".join(missing)} (waited {waited}s)')
    time.sleep(interval)
    waited += interval

# Merge
result = {"date": date_str}
for s in sections:
    f = os.path.join(parts_dir, f'{date_str}_{s}.json')
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as fp:
            part = json.load(fp)
        result[s] = part.get('items', [])
        print(f'  ✅ {s}: {len(result[s])} items')
    else:
        result[s] = []
        print(f'  ❌ {s}: missing')

output = os.path.join(data_dir, f'{date_str}.json')
with open(output, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

total = sum(len(v) for v in result.values() if isinstance(v, list))
print(f'\nMerged: {len([s for s in sections if result[s]])}/{len(sections)} sections, {total} items → {output}')
sys.exit(0)