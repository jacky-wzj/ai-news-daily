#!/usr/bin/env node

/**
 * AI News Daily Webpage Generator
 * Generates static HTML pages for daily AI news
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  templatePath: './template.html',
  dataDir: './data',
  screenshotsDir: './public/screenshots',
  dateStr: new Date().toISOString().split('T')[0],
};

// Read template
function readTemplate() {
  return fs.readFileSync(CONFIG.templatePath, 'utf8');
}

// Format date for display
function formatDate(date) {
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  });
}

// Generate HTML for a single item
function generateItemHTML(item, index) {
  let html = `
    <div class="item priority">
      <h3>${index + 1}. ${item.title}</h3>
      <div class="meta">👤 ${item.author} - ${item.date}</div>
      <p>${item.summary}</p>
  `;

  if (item.screenshot) {
    html += `<img class="screenshot" src="${item.screenshot}" alt="${item.title}">`;
  }

  if (item.link) {
    html += `<a class="link" href="${item.link}" target="_blank">🔗 原文链接</a>`;
  }

  html += `</div>`;
  return html;
}

// Generate HTML for newsletter items
function generateNewsletterHTML(items) {
  return items.map((item, i) => `
    <div class="item">
      <h3>${i + 1}. ${item.title}</h3>
      <div class="meta">📰 来源: ${item.source}</div>
      <p>${item.summary}</p>
      <a class="link" href="${item.link}" target="_blank">🔗 原文链接</a>
    </div>
  `).join('');
}

// Generate HTML for paper items
function generatePaperHTML(items) {
  return items.map((item, i) => `
    <div class="item">
      <h3>${i + 1}. ${item.title}</h3>
      <div class="meta">👤 ${item.authors}</div>
      <p>${item.summary}</p>
      <a class="link" href="${item.link}" target="_blank">📄 论文链接</a>
    </div>
  `).join('');
}

// Generate HTML for GitHub items
function generateGitHubHTML(items) {
  return items.map((item, i) => `
    <div class="card">
      <h4>${i + 1}. ${item.name}</h4>
      <p>${item.description}</p>
      <p>⭐ ${item.stars} Stars</p>
      <a class="link" href="${item.link}" target="_blank">🔗 GitHub 链接</a>
    </div>
  `).join('');
}

// Generate HTML for X posts
function generateXPostHTML(items) {
  return items.map((item, i) => `
    <div class="item priority">
      <h3>${i + 1}. ${item.title}</h3>
      <div class="meta">👤 ${item.author} - ${item.date}</div>
      <p>${item.summary}</p>
      ${item.screenshot ? `<img class="screenshot" src="${item.screenshot}" alt="${item.title}">` : ''}
      <a class="link" href="${item.link}" target="_blank">🔗 原文链接</a>
    </div>
  `).join('');
}

// Generate HTML for Discord items
function generateDiscordHTML(items) {
  return items.map((item, i) => `
    <div class="item">
      <h3>${i + 1}. ${item.title}</h3>
      <div class="meta">💬 来源: ${item.server}</div>
      <p>${item.summary}</p>
      <a class="link" href="${item.link}" target="_blank">🔗 原文链接</a>
    </div>
  `).join('');
}

// Generate HTML for HN items
function generateHNHTML(items) {
  return items.map((item, i) => `
    <div class="item">
      <h3>${i + 1}. ${item.title}</h3>
      <div class="meta">⬆️ ${item.score} Points</div>
      <p>${item.summary}</p>
      <a class="link" href="${item.link}" target="_blank">🔗 原文链接</a>
    </div>
  `).join('');
}

// Generate HTML for Reddit items
function generateRedditHTML(items) {
  return items.map((item, i) => `
    <div class="item">
      <h3>${i + 1}. ${item.title}</h3>
      <div class="meta"> reddit: ${item.subreddit}</div>
      <p>${item.summary}</p>
      <a class="link" href="${item.link}" target="_blank">🔗 原文链接</a>
    </div>
  `).join('');
}

// Generate HTML for tool items
function generateToolHTML(items) {
  return items.map((item, i) => `
    <div class="card">
      <h4>${i + 1}. ${item.name}</h4>
      <p>${item.description}</p>
      <a class="link" href="${item.link}" target="_blank">🔗 工具链接</a>
    </div>
  `).join('');
}

// Generate HTML for Agent items
function generateAgentHTML(items) {
  return items.map((item, i) => `
    <div class="item">
      <h3>${i + 1}. ${item.title}</h3>
      <div class="meta">🤖 ${item.source}</div>
      <p>${item.summary}</p>
      <a class="link" href="${item.link}" target="_blank">🔗 原文链接</a>
    </div>
  `).join('');
}

// Generate HTML for Silicon Valley items
function generateSiliconValleyHTML(items) {
  return items.map((item, i) => `
    <div class="item">
      <h3>${i + 1}. ${item.title}</h3>
      <p>${item.summary}</p>
      <a class="link" href="${item.link}" target="_blank">🔗 原文链接</a>
    </div>
  `).join('');
}

// Generate HTML for Mainland China items
function generateMainlandChinaHTML(items) {
  return items.map((item, i) => `
    <div class="item">
      <h3>${i + 1}. ${item.title}</h3>
      <p>${item.summary}</p>
      <a class="link" href="${item.link}" target="_blank">🔗 原文链接</a>
    </div>
  `).join('');
}

// Convert screenshot paths for GitHub Pages
function convertScreenshotPaths(data) {
  const convertItem = (item) => {
    if (item.screenshot && item.screenshot.startsWith('/')) {
      item.screenshot = '/ai-news-daily/public' + item.screenshot;
    }
    return item;
  };

  if (data.corePeople) data.corePeople = data.corePeople.map(convertItem);
  if (data.xPosts) data.xPosts = data.xPosts.map(convertItem);
  return data;
}

// Generate full HTML page
function generatePage(data, template) {
  // Convert screenshot paths for GitHub Pages
  data = convertScreenshotPaths(data);

  let content = '';

  // Core people insights
  if (data.corePeople && data.corePeople.length > 0) {
    content += `<h2>🌟 核心人物洞察</h2>`;
    data.corePeople.forEach((item, i) => {
      content += generateItemHTML(item, i);
    });
  }

  // Newsletter
  if (data.newsletter && data.newsletter.length > 0) {
    content += `<h2>📧 Newsletter 精选</h2>`;
    content += generateNewsletterHTML(data.newsletter);
  }

  // Papers
  if (data.papers && data.papers.length > 0) {
    content += `<h2>📚 Hugging Face 热门论文</h2>`;
    content += generatePaperHTML(data.papers);
  }

  // X posts
  if (data.xPosts && data.xPosts.length > 0) {
    content += `<h2>𝕏 X AI 动态</h2>`;
    content += generateXPostHTML(data.xPosts);
  }

  // Discord
  if (data.discord && data.discord.length > 0) {
    content += `<h2>💬 Discord 社区精选</h2>`;
    content += generateDiscordHTML(data.discord);
  }

  // GitHub
  if (data.github && data.github.length > 0) {
    content += `<h2>💻 GitHub Trending AI</h2>`;
    content += generateGitHubHTML(data.github);
  }

  // HN
  if (data.hn && data.hn.length > 0) {
    content += `<h2>🔝 Hacker News 热门讨论</h2>`;
    content += generateHNHTML(data.hn);
  }

  // Reddit
  if (data.reddit && data.reddit.length > 0) {
    content += `<h2>🤖 Reddit AI 社区精选</h2>`;
    content += generateRedditHTML(data.reddit);
  }

  // Tools
  if (data.tools && data.tools.length > 0) {
    content += `<h2>🛠️ AI 应用工具箱</h2>`;
    content += `<div class="grid">${generateToolHTML(data.tools)}</div>`;
  }

  // Agent
  if (data.agent && data.agent.length > 0) {
    content += `<h2>🦾 Agent 热门资讯</h2>`;
    content += generateAgentHTML(data.agent);
  }

  // Silicon Valley
  if (data.siliconValley && data.siliconValley.length > 0) {
    content += `<h2>🏙️ 硅谷热点新闻</h2>`;
    content += generateSiliconValleyHTML(data.siliconValley);
  }

  // Mainland China
  if (data.mainlandChina && data.mainlandChina.length > 0) {
    content += `<h2>🇨🇳 大陆智能体动态</h2>`;
    content += generateMainlandChinaHTML(data.mainlandChina);
  }

  // Replace placeholders
  let html = template
    .replace('{{date}}', formatDate(new Date()))
    .replace('{{content}}', content)
    .replace('{{items_core_people}}', data.corePeople ? data.corePeople.length : 0)
    .replace('{{items_newsletter}}', data.newsletter ? data.newsletter.length : 0)
    .replace('{{items_papers}}', data.papers ? data.papers.length : 0)
    .replace('{{items_x_posts}}', data.xPosts ? data.xPosts.length : 0)
    .replace('{{items_discord}}', data.discord ? data.discord.length : 0)
    .replace('{{items_github}}', data.github ? data.github.length : 0)
    .replace('{{items_hn}}', data.hn ? data.hn.length : 0)
    .replace('{{items_reddit}}', data.reddit ? data.reddit.length : 0)
    .replace('{{items_tools}}', data.tools ? data.tools.length : 0)
    .replace('{{items_agent}}', data.agent ? data.agent.length : 0)
    .replace('{{items_silicon_valley}}', data.siliconValley ? data.siliconValley.length : 0)
    .replace('{{items_mainland_china}}', data.mainlandChina ? data.mainlandChina.length : 0);

  // Calculate total
  const total = (data.corePeople?.length || 0) +
    (data.newsletter?.length || 0) +
    (data.papers?.length || 0) +
    (data.xPosts?.length || 0) +
    (data.discord?.length || 0) +
    (data.github?.length || 0) +
    (data.hn?.length || 0) +
    (data.reddit?.length || 0) +
    (data.tools?.length || 0) +
    (data.agent?.length || 0) +
    (data.siliconValley?.length || 0) +
    (data.mainlandChina?.length || 0);

  html = html.replace('{{total_items}}', total);

  return html;
}

// Generate index page
function generateIndex(pages, template) {
  const pageLinks = pages
    .sort((a, b) => b.localeCompare(a))
    .map(date => {
      const link = `./${date}.html`;
      const formattedDate = formatDate(new Date(date));
      return `<a href="${link}" class="date-link">${formattedDate}</a>`;
    })
    .join('');

  // Generate full HTML for index page (not using template {{content}} placeholder)
  const dateStr = formatDate(new Date());
  const time = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
  
  let html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📰 AI 资讯日报 - ${dateStr}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; line-height: 1.6; }
        .container { max-width: 900px; margin: 0 auto; padding: 20px; }
        header { text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; margin-bottom: 30px; }
        header h1 { font-size: 2.5em; margin-bottom: 10px; }
        header p { opacity: 0.9; }
        .nav { display: flex; justify-content: center; gap: 15px; margin: 20px 0; flex-wrap: wrap; }
        .nav a { padding: 10px 20px; background: white; color: #667eea; text-decoration: none; border-radius: 25px; font-weight: 500; transition: transform 0.2s; }
        .nav a:hover { transform: scale(1.05); }
        .section { background: white; border-radius: 12px; padding: 25px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .section h2 { color: #667eea; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #f0f0f0; }
        .date-list { display: flex; flex-direction: column; gap: 10px; }
        .date-link { padding: 15px 20px; background: #f8f9fa; border-radius: 8px; color: #333; text-decoration: none; transition: all 0.2s; }
        .date-link:hover { background: #667eea; color: white; transform: translateX(5px); }
        .stats { display: flex; justify-content: center; gap: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; margin: 20px 0; }
        .stat { text-align: center; }
        .stat .num { font-size: 2em; font-weight: bold; color: #667eea; }
        .stat .label { color: #888; font-size: 0.9em; }
        footer { text-align: center; padding: 30px; color: #888; }
    </style>
</head>
<body>
    <header>
        <h1>📰 AI 资讯日报</h1>
        <p>${dateStr} | 精选高质量 AI 资讯</p>
    </header>
    
    <div class="container">
        <div class="stats">
            <div class="stat"><div class="num">${pages.length}</div><div class="label">已发布日报</div></div>
        </div>

        <section id="history" class="section">
            <h2>📅 历史日报</h2>
            <div class="date-list">${pageLinks}</div>
        </section>
    </div>

    <footer>
        <p>🤖 AI 资讯日报 | 每日 ${time} 自动更新</p>
    </footer>
</body>
</html>`;

  return html;
}

// Main function
function main() {
  try {
    console.log(`📅 Generating page for ${CONFIG.dateStr}...`);

    const template = readTemplate();
    const dataPath = path.join(CONFIG.dataDir, `${CONFIG.dateStr}.json`);

    if (!fs.existsSync(dataPath)) {
      console.log(`⚠️ No data file found for ${CONFIG.dateStr}, generating empty page...`);
    }

    const data = fs.existsSync(dataPath)
      ? JSON.parse(fs.readFileSync(dataPath, 'utf8'))
      : {};

    // Generate daily page
    const pageHtml = generatePage(data, template);
    fs.writeFileSync(`${CONFIG.dateStr}.html`, pageHtml);
    console.log(`✅ Generated: ${CONFIG.dateStr}.html`);

    // Generate index
    const pages = fs.readdirSync('.')
      .filter(f => f.match(/^\d{4}-\d{2}-\d{2}\.html$/))
      .map(f => f.replace('.html', ''));

    const indexHtml = generateIndex(pages, template);
    fs.writeFileSync('index.html', indexHtml);
    console.log(`✅ Generated index.html`);

    console.log(`🎉 All pages generated successfully!`);
  } catch (error) {
    console.error('Error generating pages:', error);
    process.exit(1);
  }
}

main();
