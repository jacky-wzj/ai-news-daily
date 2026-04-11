import subprocess, os, datetime

os.chdir('/Users/niuniu/.openclaw/workspace/ai-news-daily')

# git add -A
r = subprocess.run(['git', 'add', '-A'], capture_output=True, text=True)
print('git add:', r.returncode, r.stderr.strip() or 'ok')

# git commit
date = datetime.date.today().strftime('%Y-%m-%d')
r = subprocess.run(['git', 'commit', '-m', f'Update: {date}'], capture_output=True, text=True)
print('git commit:', r.returncode, r.stdout.strip() or r.stderr.strip())

# git push
r = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True, timeout=60)
print('git push:', r.returncode, r.stdout.strip() or r.stderr.strip())
