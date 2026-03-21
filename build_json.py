import json

data = {
  "date": "2026-03-21",
  "insights": [
    {
      "title": "Anthropic vs 五角大楼：AI安全红线之争白热化",
      "date": "2026-03-21",
      "summary": "五角大楼将Anthropic列为「供应链风险」，因其拒绝在军事系统中移除AI安全护栏。Anthropic提起诉讼反击，法庭文件揭示双方曾接近达成协议。这场冲突正在重新定义AI伦理与国家安全的边界。",
      "link": "https://techcrunch.com/2026/03/20/new-court-filing-reveals-pentagon-told-anthropic-the-two-sides-were-nearly-aligned-a-week-after-trump-declared-the-relationship-kaput/"
    },
    {
      "title": "Hunter Alpha谜团揭晓：万亿参数模型疑似小米MiMo-V2-Pro",
      "date": "2026-03-21",
      "summary": "3月11日匿名上线OpenRouter的Hunter Alpha模型（1万亿参数、100万token上下文），被开发者广泛猜测为DeepSeek V4，最新证据指向小米MiMo-V2-Pro。中国AI暗战进入隐身测试新阶段。",
      "link": "https://www.technology.org/2026/03/19/whos-that-ai-the-mystery-model-everyone-blamed-on-deepseek-turned-out-to-be-xiaomi/"
    },
    {
      "title": "GPT-5.4 Mini/Nano发布：免费用户也能用准旗舰级AI",
      "date": "2026-03-21",
      "summary": "OpenAI发布GPT-5.4 mini和nano两款紧凑模型，mini版本响应速度提升2倍以上，现已向免费和Go用户开放。在编程和多模态理解上较GPT-5.0 mini大幅提升。",
      "link": "https://9to5mac.com/2026/03/17/openai-releases-gpt-5-4-mini-and-nano-its-most-capable-small-models-yet/"
    },
    {
      "title": "腾讯QClaw（龙虾）邀请制测试：AI接入微信生态",
      "date": "2026-03-21",
      "summary": "3月18日腾讯低调开放QClaw测试，基于OpenClaw技能体系，可直接操作微信完成任务。马化腾亲自转发产品矩阵文章，腾讯市值因此暴涨3500亿。企业微信同步开放OpenClaw机器人接入。",
      "link": "https://36kr.com/p/3728581722092039"
    },
    {
      "title": "AI编码工具大横评：Claude Code vs Cursor vs Windsurf vs Devin（2026年3月）",
      "date": "2026-03-21",
      "summary": "DEV Community发布2026年3月AI编码工具全面对比，Opus 4.6编码智能领先，Codex CLI沙盒安全性最佳，Cursor在2026年初加入OS级沙盒。AGENTS.md已成为所有主流AI编码工具的标配。",
      "link": "https://dev.to/bridgeace/bridge-ace-vs-claude-code-vs-cursor-vs-windsurf-vs-devin-an-honest-comparison-march-2026-1de0"
    },
    {
      "title": "2026年3月：12+新AI模型集中发布，行业进入「模型爆炸」期",
      "date": "2026-03-21",
      "summary": "仅3月一个月内就有超过12个重要AI模型发布，包括GPT-5.4系列、Hunter Alpha、腾讯混元等。模型竞赛从参数规模转向效率和场景落地，Agentic AI成为主旋律。",
      "link": "https://www.devflokers.com/blog/new-ai-model-releases-open-source-projects-march-18-19-2026"
    },
    {
      "title": "HN热议：Agent编程正在颠覆软件工程最佳实践",
      "date": "2026-03-21",
      "summary": "Hacker News热帖引发争论：AI Agent编码工具正让开发者集体放弃多年积累的编程/安全最佳实践，软件质量和确定性被牺牲。但也有人展示Agent辅助开发的高质量产出流程。",
      "link": "https://news.ycombinator.com/item?id=47444816"
    }
  ],
  "papers": [
    {
      "title": "BIGMAS: 受脑启发的图多智能体系统用于LLM推理",
      "date": "2026-03-20",
      "summary": "提出Brain-Inspired Graph Multi-Agent Systems，在Game24、Six Fives和Tower of London任务上，基于6个前沿LLM验证BIGMAS持续提升推理性能，超越ReAct等现有多Agent基线。",
      "link": "https://arxiv.org/abs/2603.15371"
    },
    {
      "title": "InterveneBench: LLM在真实社会系统中的干预推理基准",
      "date": "2026-03-16",
      "summary": "针对LLM在因果研究设计中的局限性，提出InterveneBench基准和多Agent框架STRIDES，在干预推理任务上显著超越SOTA推理模型。",
      "link": "https://arxiv.org/abs/2603.15542"
    },
    {
      "title": "Helium: 从数据系统视角优化Agent工作流的LLM服务",
      "date": "2026-03-20",
      "summary": "将经典查询优化原理应用于LLM Agent服务，Helium在多种工作负载上实现最高1.56倍的加速，为Agentic AI的大规模部署提供系统级优化方案。",
      "link": "https://arxiv.org/abs/2603.16104"
    }
  ],
  "xPosts": [
    {
      "title": "AI安全社区声援Anthropic对抗五角大楼施压",
      "date": "2026-03-20",
      "summary": "Anthropic因拒绝取消AI安全限制被国防部列为供应链风险后，Google DeepMind首席科学家Jeff Dean等AI研究者公开表态支持AI安全底线。",
      "link": "https://www.wired.com/story/department-of-defense-responds-to-anthropic-lawsuit/"
    },
    {
      "title": "开发者热议Hunter Alpha身份之谜：从DeepSeek V4到小米MiMo",
      "date": "2026-03-19",
      "summary": "OpenRouter上万亿参数匿名模型引发开发者社区大范围讨论和基准测试，最初被认为是DeepSeek V4，后有证据指向小米MiMo-V2-Pro。",
      "link": "https://mashable.com/article/mystery-ai-model-hunter-alpha-may-be-deepseek-in-disguise"
    },
    {
      "title": "AGENTS.md成为AI编码Agent标配：20+工具原生支持",
      "date": "2026-03-21",
      "summary": "截至2026年3月，GitHub Copilot、Cursor、Windsurf、Codex CLI、Devin等20+工具已原生解析AGENTS.md。开发者社区讨论这一新标准如何改变人机协作编码方式。",
      "link": "https://particula.tech/blog/agents-md-ai-coding-agent-configuration"
    }
  ],
  "discord": [
    {
      "title": "AI编码Agent安全性争论：Discord社区分两派",
      "date": "2026-03-21",
      "summary": "围绕HN热帖「Agent stuff is making me lose respect for our industry」，Discord AI社区展开激烈辩论，一方担忧安全最佳实践被抛弃，另一方展示高质量Agent工作流。",
      "link": "https://news.ycombinator.com/item?id=47444816"
    },
    {
      "title": "Stanford OpenJarvis：本地优先AI Agent框架引发隐私讨论",
      "date": "2026-03-20",
      "summary": "Stanford发布OpenJarvis开源框架，支持完全在设备端运行的个人AI Agent，具备工具调用、记忆和持续学习能力。Discord隐私AI社区热议其对云端Agent模式的挑战。",
      "link": "https://dataconomy.com/2026/03/16/openjarvis-local-first-ai-agents-that-run-entirely-on-device/"
    },
    {
      "title": "GPT-5.4 mini上线免费版ChatGPT：Discord开发者社区测评反馈",
      "date": "2026-03-21",
      "summary": "GPT-5.4 mini向免费用户开放后，Discord多个AI开发者频道涌入大量测评对比，重点关注其subagent能力和多模态理解的提升。",
      "link": "https://dataconomy.com/2026/03/18/openai-releases-gpt-5-4-mini-and-nano-models/"
    }
  ],
  "github": [
    {
      "title": "GitNexus冲上7.3K Stars：解决AI编码危机的版本管理工具",
      "date": "2026-03-21",
      "summary": "GitNexus专为AI编码场景设计的版本管理工具在GitHub Trending霸榜，解决Agent编码带来的代码质量和追踪问题，Stars数突破7.3K。",
      "link": "https://byteiota.com/gitnexus-hits-7-3k-stars-fixing-ai-coding-crisis/"
    },
    {
      "title": "NemoClaw开源Agent框架登陆GitHub",
      "date": "2026-03-20",
      "summary": "NVIDIA在GTC 2026发布的NemoClaw企业级Agent框架开源上线GitHub，专注安全治理和隐私保护，为生产环境Agent部署提供基础设施。",
      "link": "https://popularaitools.ai/nvidia-gtc-2026-nemoclaw/"
    },
    {
      "title": "Bridge ACE：自托管开源AI IDE新选手",
      "date": "2026-03-21",
      "summary": "Bridge ACE作为完全自托管的开源AI IDE在GitHub开源，支持Claude/Codex/Qwen多模型，Apache 2.0协议，无需云端依赖。",
      "link": "https://dev.to/bridgeace/bridge-ace-vs-claude-code-vs-cursor-vs-windsurf-vs-devin-an-honest-comparison-march-2026-1de0"
    }
  ],
  "hn": [
    {
      "title": "Agent stuff is really making me lose respect for our industry",
      "date": "2026-03-21",
      "summary": "HN热帖引发大量讨论：Agent编码工具让开发者集体放弃编程安全最佳实践，确定性被牺牲。评论区从愤怒到务实，折射行业对AI Agent的复杂情绪。",
      "link": "https://news.ycombinator.com/item?id=47444816"
    },
    {
      "title": "I'm OK being left behind, thanks — 拒绝AI焦虑的声音",
      "date": "2026-03-21",
      "summary": "HN热帖讨论AI时代的选择焦虑，有人选择不追赶AI浪潮。评论区理性分析当前AI工具的真实生产力增益，认为onboarding成本仍然较高。",
      "link": "https://news.ycombinator.com/item?id=47454341"
    },
    {
      "title": "如何评估LLM输出太AI味的问题",
      "date": "2026-03-21",
      "summary": "创业者分享构建内容生成工具时面临的核心工程挑战：让模型停止使用delve、testament等AI味词汇。HN社区分享各种去AI味的技术方案。",
      "link": "https://news.ycombinator.com/item?id=47450556"
    }
  ],
  "reddit": [
    {
      "title": "Anthropic vs 五角大楼：军方用户反对替换Claude",
      "date": "2026-03-20",
      "summary": "Reuters报道显示，尽管Hegseth要求五角大楼放弃Anthropic的Claude，但军方用户强烈反对，认为替换并不容易。Reddit AI社区深度讨论AI公司对军方说不的权利。",
      "link": "https://www.reuters.com/business/hegseth-wants-pentagon-dump-anthropics-claude-military-users-say-its-not-so-easy-2026-03-19/"
    },
    {
      "title": "GTC 2026实时讨论：Jensen Huang两小时演讲全面复盘",
      "date": "2026-03-20",
      "summary": "Tom's Hardware的GTC 2026直播博客配合Reddit讨论，对Vera Rubin架构和NemoClaw进行技术分析，讨论Rubin GPU对消费级市场的影响时间线。",
      "link": "https://www.tomshardware.com/news/live/nvidia-gtc-2026-keynote-live-blog-jensen-huang"
    },
    {
      "title": "2月全球AI APP下载报告：ChatGPT领先但增速放缓",
      "date": "2026-03-19",
      "summary": "点点数据显示2026年2月全球原生AI APP下载3.5亿次，ChatGPT和Gemini领先但均出现下滑，豆包下降明显，即梦AI挤入前五，DeepSeek跌出榜单。",
      "link": "https://36kr.com/p/3725337174995713"
    }
  ],
  "tools": [
    {
      "title": "Google Pixel March Drop：Circle to Search + Magic Cue新AI功能",
      "date": "2026-03-19",
      "summary": "Google发布3月Pixel Drop更新，Circle to Search获得新的个性化能力，Magic Cue提供餐饮建议，Watch增加安全功能，AI功能持续深入日常场景。",
      "link": "https://blog.google/products-and-platforms/devices/pixel/march-2026-pixel-drop/"
    },
    {
      "title": "Stanford OpenJarvis：完全离线运行的个人AI Agent框架",
      "date": "2026-03-20",
      "summary": "Stanford开源OpenJarvis框架，支持在本地设备上构建带工具调用、记忆和持续学习的个人AI Agent，数据永不离开设备，隐私优先。",
      "link": "https://dataconomy.com/2026/03/16/openjarvis-local-first-ai-agents-that-run-entirely-on-device/"
    },
    {
      "title": "GPT-5.4 mini向免费用户开放：支持Thinking模式和subagent",
      "date": "2026-03-18",
      "summary": "OpenAI将GPT-5.4 mini部署到ChatGPT免费版，通过Thinking功能开放，并新增subagent能力。在视觉和编码基准测试上大幅超越前代mini模型。",
      "link": "https://www.androidheadlines.com/2026/03/openai-gpt-5-4-mini-nano-launch-free-chatgpt.html"
    }
  ],
  "agent": [
    {
      "title": "LLM Web Agent为何失败？层级规划视角的深度分析",
      "date": "2026-03-18",
      "summary": "arXiv新论文从层级规划角度系统分析LLM Web Agent的失败原因，发现提升感知定位和自适应控制（而非仅高层推理）才是实现人类级可靠性的关键。",
      "link": "https://arxiv.org/abs/2603.14248"
    },
    {
      "title": "OpenJarvis：Stanford打造本地优先Agent框架，挑战云端模式",
      "date": "2026-03-20",
      "summary": "Stanford发布的OpenJarvis框架让个人AI Agent完全在本地运行，具备工具使用、记忆持久化和增量学习能力。这标志着Agent范式从云端向边缘设备的重要转移。",
      "link": "https://www.marktechpost.com/2026/03/12/stanford-researchers-release-openjarvis-a-local-first-framework-for-building-on-device-personal-ai-agents-with-tools-memory-and-learning/"
    },
    {
      "title": "AI编码Agent全面对比：安全沙盒成为差异化关键",
      "date": "2026-03-21",
      "summary": "2026年3月AI编码Agent工具大横评显示，Codex CLI拥有Linux内核级沙盒，Claude Code使用namespace隔离，Cursor在2026年初加入OS级沙盒。安全性成为编码Agent的核心竞争力。",
      "link": "https://murphye.medium.com/i-compared-every-major-ai-coding-tool-so-you-dont-have-to-f05a6915c0d4"
    }
  ],
  "siliconValley": [
    {
      "title": "Anthropic起诉美国政府：AI伦理公司的生存之战",
      "date": "2026-03-20",
      "summary": "Anthropic因坚持AI安全底线被五角大楼列为供应链风险后提起两项诉讼。$200M军事合同破裂，Trump公开施压，但军方用户抵制替换Claude。这是AI行业史上最重大的伦理对抗事件。",
      "link": "https://www.newyorker.com/news/annals-of-inquiry/the-pentagon-went-to-war-with-anthropic-whats-really-at-stake"
    },
    {
      "title": "OpenAI GPT-5.4 mini/nano发布：小模型大能力",
      "date": "2026-03-19",
      "summary": "OpenAI发布GPT-5.4 mini和nano两款小型模型，mini版向免费用户开放，nano版面向端侧部署。小模型赛道竞争白热化，AI民主化加速。",
      "link": "https://9to5google.com/2026/03/17/openai-gpt-5-4-mini-nano-models/"
    },
    {
      "title": "Hunter Alpha背后的六百万美元威胁：规模定律被颠覆？",
      "date": "2026-03-21",
      "summary": "分析认为Hunter Alpha（疑似小米MiMo-V2-Pro）以极低训练成本实现万亿参数，如果属实将彻底颠覆AI规模定律。硅谷巨头面临来自中国的又一次成本效率冲击。",
      "link": "https://sakab4ever.com/blog/the-6-million-threat-how-deepseeks-new-model-is-bankrupting-the-scaling-laws"
    }
  ],
  "mainlandChina": [
    {
      "title": "腾讯QClaw（龙虾）低调开测：AI Agent接入微信生态",
      "date": "2026-03-18",
      "summary": "腾讯以邀请制测试形式发布QClaw，可直接操作微信完成任务，兼容OpenClaw技能体系。马化腾凌晨转发，腾讯市值暴涨3500亿。但体验反馈显示产品仍较粗糙。",
      "link": "https://36kr.com/p/3728581722092039"
    },
    {
      "title": "Hunter Alpha身份反转：从DeepSeek V4到小米MiMo-V2-Pro",
      "date": "2026-03-19",
      "summary": "OpenRouter上匿名万亿参数模型Hunter Alpha引发全球开发者猜测是DeepSeek V4，最新调查指向小米。小米在AI大模型领域的隐秘布局曝光，中国AI竞争格局再添变数。",
      "link": "https://efficienist.com/what-is-hunter-alpha-openrouter-model-could-actually-be-xiaomi-mimo-v2-pro/"
    },
    {
      "title": "腾讯AI急行军：微信生态的AI化与混元大模型4月对决",
      "date": "2026-03-21",
      "summary": "马化腾承认腾讯AI起步慢，但正在全力追赶。QClaw上线、企业微信接入Agent、混元登顶LMArena榜单。4月将迎来DeepSeek V4与腾讯混元的关键对决，微信等超级场景成为胜负手。",
      "link": "https://www.huxiu.com/article/4842068.html"
    }
  ]
}

with open('data/2026-03-21.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('JSON written and validated!')
