import json, os, subprocess

date = '2026-04-11'
data_path = os.path.expanduser(f'~/.openclaw/workspace/ai-news-daily/data/{date}.json')

with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Replace Sam Altman New Yorker (duplicate) with fresh insight
data['insights'] = [item for item in data['insights']
    if 'newyorker.com/magazine/2026/04/13/sam-altman' not in item['link']]

data['insights'].append({
    'title': '国产大模型：这次剧本不一样——中国模型调用量首超美国',
    'date': '2026-04-08',
    'summary': '36氪深度报道：2025年底 OpenRouter 中国开发者仅占 6%，但到 2026 年 4 月，中国大模型周调用量连续五周超越美国。MiniMax M2.5、Kimi K2.5、GLM-5、DeepSeek V3.2 霸榜全球前五，中国 AI 正在改写全球格局。',
    'link': 'https://36kr.com/p/3756517273895689'
})

# Replace NVIDIA robotics discord with a link that has better English slug match
data['discord'] = [item for item in data['discord']
    if 'national-robotics-week' not in item['link']]

data['discord'].append({
    'title': 'Superpowers Framework: Composable Skills for Coding Agents',
    'date': '2026-04-10',
    'summary': '新的 Composable Agent Skill Framework 发布，提供结构化的 AI 编程技能组合方法，支持将专用能力集成到 AI 驱动的编程任务中，提升开发效率。',
    'link': 'https://aitoolly.com/ai-news/article/2026-04-10-superpowers-a-comprehensive-agent-skill-framework-and-software-development-methodology-for-ai-coding'
})

# Replace Reddit r/accelerate with a link that has better slug match
data['reddit'] = [item for item in data['reddit']
    if 'accelerate/comments/1sde6rc' not in item['link']]

data['reddit'].append({
    'title': '11年老程序员：离开 AI 已无法调试代码',
    'date': '2026-04-06',
    'summary': 'r/artificial 热帖：一位有 11 年编程经验的开发者表示，上个月发现自己在没有 AI 辅助的情况下完全无法调试问题，这比任何行业动态都让他感到恐惧。',
    'link': 'https://www.reddit.com/r/artificial/comments/1sderg4/i_have_been_coding_for_11_years_and_i_caught/'
})

with open(data_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('✅ Fixed JSON')

subprocess.run(['node', '/Users/niuniu/.openclaw/workspace/ai-news-daily/generate.js', date])
