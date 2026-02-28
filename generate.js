/**
 * AI News Daily Generator
 * Generates static HTML pages from JSON data
 */

const fs = require('fs');
const path = require('path');

// ========== Anti-hallucination link validator ==========

// Fabricated link patterns (sequential/placeholder IDs, xxxxx slugs)
const FABRICATED_PATTERNS = [
  /\/comments\/x{3,}/i,                         // reddit /comments/xxxxx
  /\/item\?id=1234567[0-9]$/,                   // HN sequential fake IDs
  /\/status\/1[89]\d{16,17}$/,                   // X sequential fake status IDs
  /\/status\/19[0-9]{10,11}$/,                   // X short fake IDs
];

// Generic links that point to homepages instead of specific content
const GENERIC_LINK_RULES = [
  // X/Twitter profile pages (no /status/)
  { test: (u) => /^https?:\/\/(x\.com|twitter\.com)\/[^/]+\/?$/.test(u), sections: 'all' },
  // Reddit subreddit homepages (no /comments/)
  { test: (u) => /^https?:\/\/(www\.)?reddit\.com\/r\/[^/]+\/?$/.test(u), sections: 'all' },
  // HN homepage only
  { test: (u) => /^https?:\/\/news\.ycombinator\.com\/?$/.test(u), sections: 'all' },
  // Hugging Face homepage only
  { test: (u) => /^https?:\/\/huggingface\.co\/?$/.test(u), sections: 'all' },
  // Discord invite links (not specific content)
  { test: (u) => /^https?:\/\/discord\.(gg|com\/invite)\//.test(u), sections: ['discord'] },
];

/**
 * Extract keywords from a URL slug for coherence checking.
 * e.g. "steve-hanke-ai-yann-lecun-meta-hype-bubble" → ['steve','hanke','yann','lecun','hype','bubble']
 */
function extractSlugKeywords(url) {
  try {
    const u = new URL(url);
    // Take the path + any readable slug portions
    const slug = u.pathname.toLowerCase()
      .replace(/\.(html?|php|aspx?)$/i, '')
      .replace(/[/_]/g, '-');
    // Split on hyphens and filter short/common words
    const stopWords = new Set(['the','a','an','in','on','at','to','for','of','and','or','is','its',
      'by','with','from','as','that','this','how','what','why','who','when','where',
      'www','com','net','org','html','htm','php','news','article','articles','blog',
      'post','index','page','2026','2025','02','01','03','04','05','06','07','08','09',
      '10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25',
      '26','27','28','29','30','31','feb','mar','jan','apr','may','jun','jul','aug','sep',
      'oct','nov','dec','technology','tech']);
    return slug.split('-').filter(w => w.length > 2 && !stopWords.has(w));
  } catch { return []; }
}

/**
 * Extract keywords from a Chinese/English title.
 */
function extractTitleKeywords(title) {
  if (!title) return [];
  // For Chinese text, extract recognizable English/brand names and Chinese key terms
  const lower = title.toLowerCase();
  // Extract English words (brand names, proper nouns)
  const engWords = (lower.match(/[a-z][a-z0-9]+/g) || []).filter(w => w.length > 2);
  // Common brand/name mappings (Chinese → English keywords)
  const brandMap = {
    '人才': ['talent','hiring'], '薪资': ['salary','pay','compensation'],
    '资本支出': ['capex','spending','capital'], '融资': ['funding','raise','billion'],
    '芯片': ['chip','gpu','semiconductor'], '模型': ['model'],
    '开源': ['open','source','opensource'], '安全': ['security','safe'],
  };
  const extraKw = [];
  for (const [cn, en] of Object.entries(brandMap)) {
    if (title.includes(cn)) extraKw.push(...en);
  }
  return [...engWords, ...extraKw];
}

/**
 * Check if title and link URL slug are coherent.
 * Returns { coherent: boolean, reason?: string }
 * Uses a heuristic: if the URL slug has strong keywords that share ZERO overlap
 * with the title, it's likely a mismatch.
 */
function checkTitleLinkCoherence(title, link) {
  if (!title || !link) return { coherent: true }; // skip if missing

  const slugKw = extractSlugKeywords(link);
  const titleKw = extractTitleKeywords(title);

  // Need enough slug keywords to make a judgment (short URLs are ambiguous)
  if (slugKw.length < 3) return { coherent: true };
  if (titleKw.length < 2) return { coherent: true };

  // Check for ANY overlap (fuzzy: substring match of 4+ chars)
  let overlap = 0;
  for (const sk of slugKw) {
    for (const tk of titleKw) {
      if (sk.length >= 4 && tk.length >= 4) {
        if (sk.includes(tk) || tk.includes(sk)) {
          overlap++;
        }
      }
    }
  }

  if (overlap === 0) {
    return {
      coherent: false,
      reason: `title-link mismatch: title="${title.slice(0,50)}" has no keyword overlap with URL slug [${slugKw.slice(0,6).join(',')}]`
    };
  }
  return { coherent: true };
}

/**
 * Validate a link. Returns { valid: boolean, reason?: string }
 */
function validateLink(link, section) {
  if (!link) return { valid: false, reason: 'missing link' };

  // Check fabricated patterns
  for (const pattern of FABRICATED_PATTERNS) {
    if (pattern.test(link)) {
      return { valid: false, reason: `fabricated link: ${link}` };
    }
  }

  // Check generic links
  for (const rule of GENERIC_LINK_RULES) {
    if (rule.sections === 'all' || rule.sections.includes(section)) {
      if (rule.test(link)) {
        return { valid: false, reason: `generic link (not specific content): ${link}` };
      }
    }
  }

  return { valid: true };
}

/**
 * Filter items in a section, removing those with invalid links.
 * Returns { kept: Item[], removed: { item, reason }[] }
 */
function filterSection(items, sectionName) {
  if (!items || items.length === 0) return { kept: [], removed: [] };
  const kept = [];
  const removed = [];
  for (const item of items) {
    // Step 1: link structure validation
    const result = validateLink(item.link, sectionName);
    if (!result.valid) {
      removed.push({ title: item.title || item.name, reason: result.reason });
      continue;
    }
    // Step 2: title-link coherence check
    const coherence = checkTitleLinkCoherence(item.title || item.name, item.link);
    if (!coherence.coherent) {
      removed.push({ title: item.title || item.name, reason: coherence.reason });
      continue;
    }
    kept.push(item);
  }
  return { kept, removed };
}

/**
 * Sanitize all sections in data. Mutates data in place.
 * Returns a report of removed items.
 */
function sanitizeData(data) {
  const report = [];
  const sections = [
    'insights', 'newsletter', 'papers', 'xPosts', 'discord',
    'github', 'hn', 'reddit', 'tools', 'agent', 'siliconValley', 'mainlandChina'
  ];
  for (const section of sections) {
    if (!data[section] || data[section].length === 0) continue;
    const { kept, removed } = filterSection(data[section], section);
    if (removed.length > 0) {
      data[section] = kept;
      report.push({ section, removed });
    }
  }
  return report;
}

// ========== End anti-hallucination ==========

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
    meta: (item) => `📅 ${item.date}`
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
  const stripped = { ...item };
  delete stripped.screenshot;
  return generateCard(stripped, i, { 
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
      // GitHub Pages 仓库部署，需要加 /ai-news-daily 前缀
      item.screenshot = '/ai-news-daily' + item.screenshot;
    }
    return item;
  };

  // 对所有有截图的模块进行转换
  if (data.insights) data.insights = data.insights.map(convertItem);
  if (data.xPosts) data.xPosts = data.xPosts.map(convertItem);
  if (data.github) data.github = data.github.map(convertItem);
  if (data.discord) data.discord = data.discord.map(convertItem);
  if (data.hn) data.hn = data.hn.map(convertItem);
  if (data.reddit) data.reddit = data.reddit.map(convertItem);
  if (data.tools) data.tools = data.tools.map(convertItem);
  if (data.agent) data.agent = data.agent.map(convertItem);
  if (data.siliconValley) data.siliconValley = data.siliconValley.map(convertItem);
  if (data.mainlandChina) data.mainlandChina = data.mainlandChina.map(convertItem);
    if (data.papers) data.papers = data.papers.map(convertItem);
  return data;
}

// Generate full HTML page
function generatePage(data, template, dateStr) {
  // Anti-hallucination: sanitize data before rendering
  const report = sanitizeData(data);
  if (report.length > 0) {
    console.log(`  ⚠️  Link sanitizer removed items for ${dateStr || 'unknown'}:`);
    for (const { section, removed } of report) {
      for (const r of removed) {
        console.log(`    🗑  [${section}] ${r.title} — ${r.reason}`);
      }
    }
  }

  // Convert screenshot paths for GitHub Pages
  data = convertScreenshotPaths(data);

  let content = '';

  // Core people insights
  content += generateSection('🌟 核心人物洞察', '🌟', data.insights, generateInsightsCard);

  // Newsletter (hidden)
  // content += generateSection('📧 Newsletter 精选', '📧', data.newsletter, generateNewsletterCard);
  
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
  
  // Get all JSON files (or specific date from command line)
  const args = process.argv.slice(2);
  const dateArg = args[0]; // Optional: specific date like "2026-02-21"
  
  let jsonFiles;
  if (dateArg) {
    // Generate single date
    jsonFiles = [`${dateArg}.json`];
  } else {
    // Generate all dates (default behavior)
    jsonFiles = fs.readdirSync(dataDir).filter(f => f.endsWith('.json'));
  }
  
  // Generate pages for each date
  for (const jsonFile of jsonFiles) {
    const dateStr = jsonFile.replace('.json', '');
    const dataFile = path.join(dataDir, jsonFile);
    
    if (!fs.existsSync(dataFile)) {
      console.error(`❌ Data file not found: ${dataFile}`);
      continue;
    }
    
    console.log(`📅 Generating page for ${dateStr}...`);
    const data = JSON.parse(fs.readFileSync(dataFile, 'utf-8'));
    const html = generatePage(data, template, dateStr);
    
    // Write to both root (for GitHub Pages) and public directory
    const outputPath = path.join(publicDir, `${dateStr}.html`);
    const rootPath = path.join(__dirname, `${dateStr}.html`);
    fs.writeFileSync(outputPath, html);
    fs.writeFileSync(rootPath, html);
    console.log(`✅ Generated: ${dateStr}.html`);
  }
  
  // Generate index (always regenerate for all dates)
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
  fs.writeFileSync(path.join(__dirname, 'index.html'), indexHtml);
  console.log(`✅ Generated: index.html`);
  
  console.log('🎉 All pages generated successfully!');
}

main();
