/**
 * AI News Daily Generator
 * Generates static HTML pages from JSON data
 */

const fs = require('fs');
const path = require('path');

// Helper function to escape HTML
function escapeHtml(text) {
  if (!text) return '';
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// Unified card generator - 所有模块使用相同样式 .card
function generateCard(item, index, options = {}) {
  const { title, meta, priority = false } = options;
  const titleText = item.title || item.name;
  const metaText = meta ? meta(item) : '';
  
  let html = `
    <div class="card${priority ? ' card--priority' : ''}">
      <h3>${index + 1}. ${escapeHtml(titleText)}</h3>
      ${metaText ? `<div class="meta">${metaText}</div>` : ''}
      <p>${escapeHtml(item.summary || item.description)}</p>
  `;

  // Add screenshot if available
  if (item.screenshot) {
    html += `<img class="screenshot" src="${item.screenshot}" alt="${escapeHtml(titleText)}">`;
  }

  // Add link if available
  if (item.link) {
    html += `<a class="link" href="${item.link}" target="_blank">🔗 原文链接</a>`;
  }
  
  // Add stars for GitHub
  if (item.stars) {
    html += `<p style="margin-top: 8px; font-size: 0.875rem;">⭐ ${item.stars} Stars</p>`;
  }

  html += `</div>`;
  return html;
}

// Section generator - 统一使用 card 样式
function generateSection(title, icon, items, cardGenerator) {
  if (!items || items.length === 0) return '';
  
  // 从标题中移除emoji，保留纯文字
  const titleText = title.replace(/^[^\s]+\s+/, '');
  
  let html = `
    <section class="section">
      <div class="section-header">
        <span class="icon">${icon}</span>
        <h2>${titleText}</h2>
      </div>
  `;
  
  html += items.map((item, i) => cardGenerator(item, i)).join('');
  html += `</section>`;
  return html;
}

// Card generators for each category
function generateInsightsCard(item, i) {
  return generateCard(item, i, { 
    meta: (item) => `👤 <span class="author">${escapeHtml(item.author)}</span> · ${item.date}`
  });
}

function generateNewsletterCard(item, i) {
  return generateCard(item, i, {
    meta: (item) => `📰 来源: ${escapeHtml(item.source)}`
  });
}

function generatePaperCard(item, i) {
  return generateCard(item, i, {
    meta: (item) => `👤 ${escapeHtml(item.authors)}`
  });
}

function generateXPostCard(item, i) {
  return generateCard(item, i, { 
    meta: (item) => `👤 <span class="author">${escapeHtml(item.author)}</span> · ${item.date}`
  });
}

function generateDiscordCard(item, i) {
  return generateCard(item, i, {
    meta: (item) => `💬 ${escapeHtml(item.server)}`
  });
}

function generateGitHubCard(item, i) {
  return generateCard(item, i);
}

function generateHNCard(item, i) {
  return generateCard(item, i, {
    meta: (item) => `⬆️ ${item.score} Points`
  });
}

function generateRedditCard(item, i) {
  return generateCard(item, i, {
    meta: (item) => `reddit: ${escapeHtml(item.subreddit)}`
  });
}

function generateToolCard(item, i) {
  return generateCard(item, i);
}

function generateAgentCard(item, i) {
  return generateCard(item, i, {
    meta: (item) => `🤖 ${escapeHtml(item.source)}`
  });
}

function generateSiliconValleyCard(item, i) {
  return generateCard(item, i);
}

function generateMainlandChinaCard(item, i) {
  return generateCard(item, i);
}

// Convert screenshot paths for GitHub Pages
function convertScreenshotPaths(data) {
  const convertItem = (item) => {
    if (item.screenshot && item.screenshot.startsWith('/')) {
      item.screenshot = '/ai-news-daily/public' + item.screenshot;
    }
    return item;
  };

  if (data.insights) data.insights = data.insights.map(convertItem);
  if (data.xPosts) data.xPosts = data.xPosts.map(convertItem);
  return data;
}

// Generate full HTML page
function generatePage(data, template) {
  // Convert screenshot paths for GitHub Pages
  data = convertScreenshotPaths(data);

  let content = '';

  // Core people insights
  content += generateSection('🌟 核心人物洞察', '🌟', data.insights, generateInsightsCard);

  // Newsletter
  content += generateSection('📧 Newsletter 精选', '📧', data.newsletter, generateNewsletterCard);

  // Papers
  content += generateSection('📚 Hugging Face 热门论文', '📚', data.papers, generatePaperCard);

  // X posts
  content += generateSection('𝕏 X AI 动态', '𝕏', data.xPosts, generateXPostCard);

  // Discord
  content += generateSection('💬 Discord 社区精选', '💬', data.discord, generateDiscordCard);

  // GitHub
  content += generateSection('💻 GitHub Trending AI', '💻', data.github, generateGitHubCard);

  // HN
  content += generateSection('🔝 Hacker News 热门', '🔝', data.hn, generateHNCard);

  // Reddit
  content += generateSection('🤖 Reddit AI 社区', '🤖', data.reddit, generateRedditCard);

  // Tools
  content += generateSection('🛠️ AI 应用工具箱', '🛠️', data.tools, generateToolCard);

  // Agent
  content += generateSection('🦾 Agent 热门资讯', '🦾', data.agent, generateAgentCard);

  // Silicon Valley
  content += generateSection('🏙️ 硅谷热点新闻', '🏙️', data.siliconValley, generateSiliconValleyCard);

  // Mainland China
  content += generateSection('🇨🇳 大陆智能体动态', '🇨🇳', data.mainlandChina, generateMainlandChinaCard);

  // Calculate total items
  const total = (data.insights?.length || 0) +
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

  // Replace placeholders
  let html = template
    .replace('{{date}}', formatDate(new Date()))
    .replace('{{date}}', formatDate(new Date())) // for body content
    .replace('{{content}}', content)
    .replace('{{items_core_people}}', data.insights ? data.insights.length : 0)
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
    .replace('{{items_mainland_china}}', data.mainlandChina ? data.mainlandChina.length : 0)
    .replace('{{total_items}}', total)
    .replace('{{time}}', new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }));

  return html;
}

// Format date
function formatDate(date) {
  return date.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    weekday: 'long'
  });
}

// Generate index page
function generateIndex(pages, template) {
  const sortedPages = pages.sort((a, b) => new Date(b.date) - new Date(a.date));
  
  const links = sortedPages.slice(0, 30).map(page => {
    return `<a href="${page.filename}" class="link">${page.date}</a>`;
  }).join(' · ');

  return template
    .replace('{{date}}', formatDate(new Date()))
    .replace('{{links}}', links)
    .replace('{{time}}', new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }));
}

// Main function
function main() {
  const dataDir = path.join(__dirname, 'data');
  const publicDir = path.join(__dirname, 'public');
  const templatePath = path.join(__dirname, 'template.html');
  const indexTemplatePath = path.join(__dirname, 'index-template.html');
  
  // Read template
  const template = fs.readFileSync(templatePath, 'utf-8');
  
  // Get today's date string
  const today = new Date();
  const dateStr = today.toISOString().split('T')[0];
  const dataFile = path.join(dataDir, `${dateStr}.json`);
  
  console.log(`📅 Generating page for ${dateStr}...`);
  
  // Read data
  if (!fs.existsSync(dataFile)) {
    console.error(`❌ Data file not found: ${dataFile}`);
    process.exit(1);
  }
  
  const data = JSON.parse(fs.readFileSync(dataFile, 'utf-8'));
  
  // Generate page
  const html = generatePage(data, template);
  
  // Write to file
  const outputPath = path.join(publicDir, `${dateStr}.html`);
  fs.writeFileSync(outputPath, html);
  console.log(`✅ Generated: ${dateStr}.html`);
  
  // Generate index
  const pages = fs.readdirSync(dataDir)
    .filter(f => f.endsWith('.json'))
    .map(f => {
      const d = JSON.parse(fs.readFileSync(path.join(dataDir, f), 'utf-8'));
      return {
        date: d.date,
        filename: `${d.date}.html`
      };
    });
  
  // Try to read index template, fallback to main template
  let indexTemplate = template;
  if (fs.existsSync(indexTemplatePath)) {
    indexTemplate = fs.readFileSync(indexTemplatePath, 'utf-8');
  }
  
  const indexHtml = generateIndex(pages, indexTemplate);
  fs.writeFileSync(path.join(publicDir, 'index.html'), indexHtml);
  console.log(`✅ Generated: index.html`);
  
  console.log('🎉 All pages generated successfully!');
}

main();
