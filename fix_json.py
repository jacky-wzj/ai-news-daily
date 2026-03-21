import json

# Read existing JSON
with open('data/2026-03-21.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix github: replace first item (was filtered as dup)
data['github'][0] = {
    "title": "GitNexus知识图谱引擎17K Stars：让AI编码Agent理解代码全局架构",
    "date": "2026-03-21",
    "summary": "GitNexus将代码库索引为知识图谱，暴露每个依赖、调用链和执行流，通过MCP让AI编码Agent不再盲目修改代码。2月发布至今Stars突破17.4K。",
    "link": "https://byteiota.com/gitnexus-transforms-ai-coding-with-knowledge-graphs/"
}

# Fix reddit: replace second item (dup tomshardware)
data['reddit'][1] = {
    "title": "2026年AI工程现状：Reddit社区大讨论",
    "date": "2026-03-20",
    "summary": "r/aiengineering热帖讨论2026年AI工程的真实状态，从模型选型到Agent部署的实战经验分享，以及AI对工程师就业市场的实际影响。",
    "link": "https://www.reddit.com/r/aiengineering/comments/1rf7myh/the_actual_state_of_ai_engineering_in_2026/"
}

# Fix agent: replace third item (link mismatch)
data['agent'][2] = {
    "title": "2026年Agent从Chatbot走向基础设施：Reddit热议范式转变",
    "date": "2026-03-21",
    "summary": "Reddit r/AI_Agents热帖指出2024是Chatbot之年，2026年AI正变得像电网一样无形且必要——静默处理数据同步、邮件分类、能源优化。Agent正在消失于日常基础设施中。",
    "link": "https://www.reddit.com/r/AI_Agents/comments/1rvvz4z/2024_was_the_year_of_the_chatbot_2026_is_the_year/"
}

# Fix siliconValley: replace third item (link mismatch)
data['siliconValley'][2] = {
    "title": "Hunter Alpha引发规模定律质疑：中国模型的成本效率冲击",
    "date": "2026-03-21",
    "summary": "分析认为Hunter Alpha（疑似小米MiMo-V2-Pro）以极低训练成本实现万亿参数，如果属实将彻底颠覆AI规模定律。硅谷巨头面临来自中国的又一次成本效率冲击。",
    "link": "https://efficienist.com/what-is-hunter-alpha-openrouter-model-could-actually-be-xiaomi-mimo-v2-pro/"
}

with open('data/2026-03-21.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('JSON updated!')
