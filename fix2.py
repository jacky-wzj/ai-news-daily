import json

with open('data/2026-03-21.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix reddit second item - title must match URL slug keywords
data['reddit'][1] = {
    "title": "The Actual State of AI Engineering In 2026",
    "date": "2026-03-20",
    "summary": "r/aiengineering热帖讨论2026年AI Engineering的真实状态，从模型选型到Agent部署的实战经验分享，以及AI对工程师就业市场的实际影响。",
    "link": "https://www.reddit.com/r/aiengineering/comments/1rf7myh/the_actual_state_of_ai_engineering_in_2026/"
}

with open('data/2026-03-21.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('Fixed!')
