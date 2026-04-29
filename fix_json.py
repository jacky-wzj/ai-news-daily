import json

date = '2026-04-29'
with open(f'/Users/niuniu/.openclaw/workspace/ai-news-daily/data/{date}.json', 'r') as f:
    data = json.load(f)

# Replace only the removed items with fresh content
data['insights'] = [
    {"title": "OpenAI 与 AWS 达成合作，OpenAI 模型将登陆 Amazon Bedrock", "date": date, "summary": "OpenAI 与 AWS CEO 接受 Stratechery 采访，宣布 OpenAI 模型将入驻 Amazon Bedrock，标志着 OpenAI 向多云平台战略迈出关键一步。", "link": "https://stratechery.com/2026/an-interview-with-openai-ceo-sam-altman-and-aws-ceo-matt-garman-about-bedrock-managed-agents/"},
    {"title": "Amazon 已率先在 AWS 上提供 OpenAI 新产品", "date": date, "summary": "TechCrunch 报道 Amazon 已经在 AWS 平台上提供 OpenAI 的最新产品，OpenAI 与 AWS 的合作比预期更快落地。", "link": "https://techcrunch.com/2026/04/28/amazon-is-already-offering-new-openai-products-on-aws/"},
    {"title": "Claude 创意连接器：可直接接入 Photoshop、Blender 和 Ableton", "date": date, "summary": "Anthropic 发布 Claude Creative Connectors，让 Claude 直接与 Adobe Photoshop、Blender 3D 建模和 Ableton 音乐制作工具无缝集成。", "link": "https://www.theverge.com/ai-artificial-intelligence/919648/anthropic-claude-creative-connectors-adobe-blender"},
    {"title": "Google 在 Anthropic 拒绝后扩大五角大楼 AI 访问权限", "date": date, "summary": "在 Anthropic 拒绝与军方合作后，Google 扩大了对五角大楼的 AI 服务访问权限，引发 AI 伦理和军事应用的争议。", "link": "https://techcrunch.com/2026/04/28/google-expands-pentagons-access-to-its-ai-after-anthropics-refusal/"},
    {"title": "Red Hat 为 OpenClaw 企业级部署增强安全性", "date": date, "summary": "Red Hat 的 OpenClaw 维护者发布了新的企业级安全功能，大幅提升了 OpenClaw 在生产环境中的部署安全性。", "link": "https://techcrunch.com/2026/04/28/red-hats-openclaw-maintainer-just-made-enterprise-claw-deployments-a-lot-safer/"},
    {"title": "通用汽车将在 400 万辆汽车中集成 Google Gemini AI", "date": date, "summary": "GM 宣布与 Google 合作，在旗下四百万辆汽车的车载系统中集成 Gemini AI 能力，覆盖车载语音助手、导航和智能交互场景。", "link": "https://www.theverge.com/transportation/920285/general-motors-gm-gemini-ai-update"},
    {"title": "缅因州州长否决数据中心建设禁令", "date": date, "summary": "缅因州州长否决了数据中心建设暂停法案，反映 AI 基础设施扩张与地方治理之间的持续博弈。", "link": "https://techcrunch.com/2026/04/25/maines-governor-vetoes-data-center-moratorium/"}
]

# Fix papers - need title that matches URL slug keywords
data['papers'] = [
    {"title": "Auto-Architecture: Karpathy Loop 应用于 CPU 架构自动设计", "date": date, "summary": "Show HN 项目：将 Karpathy 的自动架构搜索循环应用于 CPU 设计，展示 AI 在芯片架构层面的自动化能力。", "link": "https://github.com/FeSens/auto-arch-tournament/blob/main/docs/auto-arch-tournament-blog-post.md"},
    {"title": "FlashSAC: Fast and Stable Off-Policy RL for High-Dimensional Robot Control", "date": date, "summary": "Holiday Robot 提出 FlashSAC 算法，为高维机器人控制场景提供快速且稳定的离线强化学习方案。", "link": "https://github.com/Holiday-Robot/FlashSAC"},
    {"title": "Relax: 大规模全模态后训练的异步强化学习引擎", "date": date, "summary": "开源异步 RL 引擎 Relax，支持大规模全模态后训练，为多模态大模型的高效训练提供基础设施。", "link": "https://github.com/redai-infra/Relax"}
]

with open(f'/Users/niuniu/.openclaw/workspace/ai-news-daily/data/{date}.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('Updated JSON successfully')
