#!/usr/bin/env python3
"""Build the daily AI news JSON data."""

import json
import sys

date = sys.argv[1] if len(sys.argv) > 1 else "2026-05-27"

data = {
    "date": date,
    "insights": [
        {
            "title": "Dropbox CEO Drew Houston卸任：AI重塑SaaS格局，19年掌门人退场",
            "date": "2026-05-26",
            "summary": "Dropbox创始人Drew Houston在执掌公司19年后宣布卸任CEO，转任执行董事长。公司市值约60亿美元，较2018年IPO高点腰斩。AI浪潮对传统SaaS模式产生根本性冲击，营收近两年持平。产品主管Ashraf Alkarmi将接任CEO。",
            "link": "https://www.cnbc.com/2026/05/26/dropbox-ceo-drew-houston-ashraf-alkarmi.html"
        },
        {
            "title": "Meta启动8000人裁员，押注1450亿美元AI战略",
            "date": "2026-05-20",
            "summary": "Meta于5月20日开始执行10%全球裁员计划（约8000人），CEO扎克伯格全面转向AI优先战略。2026年资本支出预计高达1450亿美元。2026年全球科技行业已有超11万人被裁，AI成为主要驱动力。",
            "link": "https://finance.yahoo.com/sectors/technology/articles/meta-layoffs-2026-8-000-114209703.html"
        },
        {
            "title": "特朗普叫停AI行政令签署：不愿损害美国AI领先地位",
            "date": "2026-05-21",
            "summary": "特朗普在签署前数小时紧急叫停AI行政令，称部分条款可能削弱美国AI竞争优势。此前财政部长与美联储主席召集华尔街CEO紧急会议，警告Anthropic Mythos模型的网络安全风险。该行政令本将建立90天模型预发布审查框架。",
            "link": "https://www.siliconvalley.com/2026/05/21/ai-executive-order/"
        },
        {
            "title": "SpaceX IPO文件披露：xAI Q1亏损24亿，与Anthropic签150亿算力合同",
            "date": "2026-05-20",
            "summary": "SpaceX S-1招股书披露xAI Q1亏损24亿美元（同比暴增156%），资本支出77亿美元。同时向Anthropic出租300MW算力容量，月费12.5亿美元，合同至2029年5月。SpaceX计划2028年发射AI算力卫星。",
            "link": "https://aibusiness.com/generative-ai/spacex-ipo-filing-opens-up-xai-finances"
        },
        {
            "title": "OpenAI准备秘密提交IPO申请，估值7300亿美元",
            "date": "2026-05-20",
            "summary": "OpenAI正准备在未来几周秘密提交IPO申请，与高盛和摩根士丹利合作，最快2026年9月上市。私募市场估值已达7300亿美元，将成为史上最大AI公司IPO之一，与SpaceX、Anthropic共同掀起硅谷IPO浪潮。",
            "link": "https://www.nytimes.com/2026/05/20/technology/openai-ipo.html"
        },
        {
            "title": "Elon Musk在输掉OpenAI诉讼后提出AI全民基本收入方案",
            "date": "2026-05-26",
            "summary": "陪审团一致裁定Musk起诉OpenAI超出诉讼时效后，Musk转而提出全民收入方案应对AI造成的大规模失业。Anthropic CEO Dario Amodei也呼吁类似UBI措施，称'当前经济模式将不再适用'。Sam Altman则转向'集体所有权'模式。",
            "link": "https://finance-commerce.com/2026/05/elon-musk-universal-income-ai-job-losses/"
        },
        {
            "title": "HSBC CEO告诫员工'不要对抗AI'，银行业AI裁员潮开启",
            "date": "2026-05-23",
            "summary": "汇丰银行CEO向全体员工传达'不要对抗AI'，随着银行开始AI相关岗位裁减，员工担忧加剧。各大银行坦率评估AI将如何取代工作岗位。此前美国财长召集华尔街CEO讨论AI网络安全风险。",
            "link": "https://www.reuters.com/technology/artificial-intelligence/"
        }
    ],
    "papers": [
        {
            "title": "SkillOpt: Executive Strategy for Self-Evolving Agent Skills",
            "date": "2026-05-22",
            "summary": "微软研究院提出SkillOpt框架，为自进化AI Agent提供执行策略优化。Hugging Face当日#1论文（153+点赞）。提出了让AI Agent自动发现、学习和优化新技能的元学习策略。",
            "link": "https://huggingface.co/papers/2605.23904"
        },
        {
            "title": "PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion",
            "date": "2026-05-22",
            "summary": "NVIDIA研究团队提出PiD（Pixel Diffusion）方法，实现快速高分辨率潜在解码。显著提升扩散模型生成速度和质量，对图像/视频生成领域有重要影响。",
            "link": "https://arxiv.org/abs/2605.23902"
        },
        {
            "title": "MUSE-Autoskill: Self-Evolving Agents via Skill Creation, Memory, and Evaluation",
            "date": "2026-05-27",
            "summary": "字节跳动提出MUSE-Autoskill框架，AI Agent通过技能创建、记忆管理和评估进行自我进化。使Agent能在无人工干预下持续学习新技能并优化已有能力。",
            "link": "https://huggingface.co/papers/2605.27366"
        }
    ],
    "xPosts": [
        {
            "title": "Andrej Karpathy宣布加入Anthropic：'已加入Anthropic，期待回到R&D'",
            "date": "2026-05-19",
            "summary": "OpenAI联合创始人、前特斯拉AI总监Andrej Karpathy在X宣布加入Anthropic预训练团队。推文引发AI行业地震，被视为2026年最大人才流动事件。Karpathy表示'LLM前沿的接下来几年将尤为重要'。",
            "link": "https://x.com/karpathy/status/2056753169888334312"
        },
        {
            "title": "Elon Musk在输掉OpenAI诉讼后持续在X发声",
            "date": "2026-05-18",
            "summary": "陪审团裁定Musk起诉OpenAI超出诉讼时效后，Musk继续在X平台发帖评论判决。Altman庭审中被问及Dario Amodei等人对其'误导行为'的指控。Musk宣布将上诉第九巡回法院。",
            "link": "https://www.nytimes.com/live/2026/05/18/technology/openai-trial-verdict-altman-musk"
        },
        {
            "title": "Simon Willison揭示ChatGPT语音模式仍用旧版GPT-4o模型",
            "date": "2026-05-22",
            "summary": "知名开发者Simon Willison关注Karpathy的观察：ChatGPT语音模式仍在运行旧版GPT-4o模型（2024年4月截止），而Codex等高端模型已能自主重构整个代码库。揭示了不同AI访问点间日益扩大的能力差距。",
            "link": "https://dentro.de/ai/news/"
        }
    ],
    "discord": [
        {
            "title": "DEV社区热议：开源AI Agent工具包生态2026全景图",
            "date": "2026-05-22",
            "summary": "开发者社区发布2026年开源AI Agent工具包完整生态概述，涵盖MCP协议支持、生成式UI运行时等关键组件。社区指出工具链碎片化严重，多数讨论仅聚焦编排层面而忽略完整开发生命周期。",
            "link": "https://dev.to/anmolbaranwal/open-source-toolkit-for-building-ai-agents-in-2026-55h1"
        },
        {
            "title": "AI Daily Digest: Agentic Workflows、Coding Agents与具身AI",
            "date": "2026-05-20",
            "summary": "DEV社区AI日报汇总代理工作流、编码Agent和具身AI三大主题。技术核心关注点：LLM Agent与ROS机器人框架的集成正从研究演示走向生产部署考量。",
            "link": "https://dev.to/hiroki-ii-ai/ai-daily-digest-may-20-2026-agentic-workflows-coding-agents-embodied-ai-481"
        },
        {
            "title": "Reddit热议：2026年47个新Agent产品发布，五大差异化趋势",
            "date": "2026-05-25",
            "summary": "r/AI_Agents用户追踪47个2026年新兴Agent产品发布，分析最新一代五大差异化趋势。来源涵盖TechCrunch、Product Hunt、YC W26、a16z投资组合等，1-5月最有趣的AI产品来自Agent而非基础模型。",
            "link": "https://www.reddit.com/r/AI_Agents/comments/1tn12df/i_tracked_47_new_agent_products_launched_in_2026/"
        }
    ],
    "github": [
        {
            "title": "Understand-Anything：将任何代码转为交互式知识图谱",
            "date": "2026-05-27",
            "summary": "36K+星标，今日新增4697星。支持Claude Code、Codex、Cursor、Copilot、Gemini CLI等。将代码转化为可探索、可搜索、可提问的交互式知识图谱。TypeScript编写。",
            "link": "https://github.com/Lum1104/Understand-Anything"
        },
        {
            "title": "Anthropic Knowledge Work Plugins：知识工作者AI插件库",
            "date": "2026-05-27",
            "summary": "16.7K+星标，今日新增1718星。Anthropic官方开源的知识工作者插件库，用于Claude Cowork。Python编写，Apache 2.0开源。",
            "link": "https://github.com/anthropics/knowledge-work-plugins"
        },
        {
            "title": "ai-engineering-from-scratch：从零学习AI工程化",
            "date": "2026-05-27",
            "summary": "20.8K+星标，今日新增2155星。系统化AI工程学习资源库，涵盖学习-构建-交付完整流程。Python编写，适合入门到进阶AI开发者。",
            "link": "https://github.com/rohitg00/ai-engineering-from-scratch"
        }
    ],
    "hn": [
        {
            "title": "Dropbox CEO Drew Houston宣布卸任",
            "date": "2026-05-26",
            "summary": "Dropbox创始人Drew Houston执掌公司19年后宣布卸任转任执行董事长，引发HN 299点330+评论热议。讨论聚焦AI对SaaS商业模式的颠覆性影响及传统云服务商的未来。",
            "link": "https://news.ycombinator.com/item?id=48279453"
        },
        {
            "title": "外包+本地AI将比前沿大模型实验室更经济",
            "date": "2026-05-26",
            "summary": "深度分析文章在HN获250点143+评论。论证外包人力+本地AI推理组合即将比直接使用OpenAI/Anthropic等前沿实验室API更具经济效益，引发开发者对AI成本模型重新思考。",
            "link": "https://news.ycombinator.com/item?id=48278610"
        },
        {
            "title": "与LLM协作时应使用'无聊'的编程语言",
            "date": "2026-05-26",
            "summary": "HN热门文章（178点143评论）讨论AI编程最佳实践：使用Python/JavaScript等'无聊'语言与LLM协作更高效。因为训练数据充足，AI对主流语言理解更深，生成代码质量显著优于小众语言。",
            "link": "https://news.ycombinator.com/item?id=48237012"
        }
    ],
    "reddit": [
        {
            "title": "r/AI_Agents: 2026年47个新Agent产品发布大盘点",
            "date": "2026-05-25",
            "summary": "Reddit用户系统追踪2026年1-5月47个新兴Agent产品发布，分析五大差异化趋势。来源涵盖TC、PH、YC W26、a16z。讨论指出最有趣的AI产品正从基础模型转向Agent。",
            "link": "https://www.reddit.com/r/AI_Agents/comments/1tn12df/i_tracked_47_new_agent_products_launched_in_2026/"
        },
        {
            "title": "r/MachineLearning: COLM 2026论文评审热议",
            "date": "2026-05-23",
            "summary": "ML社区热议COLM 2026评审。讨论强调'无聊的工程'（监控、推理成本、延迟、评估、数据管道）对项目能否走出Demo至关重要，模型再强也离不开工程落地。",
            "link": "https://www.reddit.com/r/MachineLearning/comments/1tkuu66/colm_2026_reviewsdiscussion_d/"
        },
        {
            "title": "r/AI_Agents: 2026年最佳AI语音Agent评选",
            "date": "2026-05-24",
            "summary": "社区热议2026最佳AI语音Agent，涵盖入站客服、外呼销售、预约管理等真实业务场景。反映语音AI Agent从实验到商业落地的加速趋势。",
            "link": "https://www.reddit.com/r/AI_Agents/comments/1tm7dqu/what_are_the_best_ai_voice_agents_in_2026/"
        }
    ],
    "tools": [
        {
            "title": "Google AI Studio：零成本全栈Vibe Coding部署",
            "date": "2026-05-21",
            "summary": "Google I/O 2026宣布AI Studio与GCP深度集成，用户可零成本部署两个全栈应用（Cloud Run+Firestore+Cloud SQL+Firebase Auth），无需信用卡。AI Agent可自动推断合适数据库。",
            "link": "https://cloud.google.com/blog/products/databases/vibe-coded-ai-studio-apps-with-firestore-firebase-cloud-sql/"
        },
        {
            "title": "GitLab 19.0：Developer Flow将MR变为Agent工作流",
            "date": "2026-05-21",
            "summary": "GitLab 19.0发布，Developer Flow将传统MR转变为AI Agent驱动工作流。编码Agent评估标准从'自动补全多聪明'转向'多可靠帮助团队评审、合并、部署'。",
            "link": "https://nerova.ai/news/gitlab-19-0-developer-flow-merge-request-agents-may-2026"
        },
        {
            "title": "Chrome DevTools for Agents：为AI Coding Agent提供实时调试",
            "date": "2026-05-20",
            "summary": "Google I/O发布Chrome DevTools for Agents，为AI编码Agent提供实时验证、调试和代码优化可见性。已支持Antigravity及20+编码Agent平台。",
            "link": "https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/"
        }
    ],
    "agent": [
        {
            "title": "Google Gemini Spark：24/7个人AI Agent，即将支持MCP",
            "date": "2026-05-20",
            "summary": "Google I/O发布Gemini Spark，全天候AI Agent。确认数周内支持MCP协议，可在Canva、Instacart、OpenTable等第三方服务自主执行任务。",
            "link": "https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/"
        },
        {
            "title": "OpenAI Codex被Gartner评为企业AI编码Agent领导者",
            "date": "2026-05-22",
            "summary": "OpenAI入选Gartner企业AI编码Agent Magic Quadrant领导者象限，Codex周活用户超400万。与Dell合作混合/本地部署，与Cisco合作AI Defense平台。",
            "link": "https://openai.com/index/gartner-2026-agentic-coding-leader/"
        },
        {
            "title": "Cohere发布Command A+：首款完全Apache 2.0开源企业Agent模型",
            "date": "2026-05-23",
            "summary": "Cohere发布218B MoE模型Command A+（25B活跃参数），首款完全Apache 2.0开源企业模型。支持48种语言、128K上下文，Agent基准从37%跃升至85%，首创无损量化与原生引用功能。",
            "link": "https://venturebeat.com/technology/cohere-cracks-lossless-quantization-and-native-citations-with-first-full-apache-2-0-licensed-open-model-command-a"
        }
    ],
    "siliconValley": [
        {
            "title": "Cerebras晶圆级AI芯片IPO募资56亿美元，创AI IPO纪录",
            "date": "2026-05-14",
            "summary": "Cerebras Systems于5月14日上市，募资56亿美元、估值560亿美元，成为史上最大AI芯片IPO。晶圆级AI芯片技术路径获得资本市场认可，信号表明AI投资者热情依然高涨。",
            "link": "https://theberkshireedge.com/capital-ideas-what-is-this-cerebras-ipo/"
        },
        {
            "title": "SpaceX、OpenAI与An