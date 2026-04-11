import json, os, subprocess

date = '2026-04-11'
data_path = os.path.expanduser(f'~/.openclaw/workspace/ai-news-daily/data/{date}.json')

with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data['discord'] = data['discord'][:3]

with open(data_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('✅ Trimmed discord to 3')

subprocess.run(['node', '/Users/niuniu/.openclaw/workspace/ai-news-daily/generate.js', date])
