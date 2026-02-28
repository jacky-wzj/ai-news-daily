/**
 * 钉钉机器人推送脚本
 * 使用加签方式认证
 * 
 * Usage: node dingtalk-notify.js <url> [title]
 * Example: node dingtalk-notify.js https://jacky-wzj.github.io/ai-news-daily/2026-02-28.html "2026-02-28 AI资讯日报"
 */

const crypto = require('crypto');
const https = require('https');
const http = require('http');

const WEBHOOK = 'https://oapi.dingtalk.com/robot/send?access_token=f3762153d0b1631cf323bd0010aec5d0ba4548e11917fd3c48e9a7637660713b';
const SECRET = 'SECd2d72abd2f03dca176a88f0f25a16b0477cbd0aeba1228f9d3cbb38a2054a26e';

function generateSign() {
  const timestamp = Date.now();
  const stringToSign = `${timestamp}\n${SECRET}`;
  const hmac = crypto.createHmac('sha256', SECRET).update(stringToSign).digest('base64');
  const sign = encodeURIComponent(hmac);
  return { timestamp, sign };
}

function sendMessage(content) {
  return new Promise((resolve, reject) => {
    const { timestamp, sign } = generateSign();
    const url = `${WEBHOOK}&timestamp=${timestamp}&sign=${sign}`;

    const body = JSON.stringify({
      msgtype: 'markdown',
      markdown: {
        title: content.title,
        text: content.text
      }
    });

    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      port: 443,
      path: parsed.pathname + parsed.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.errcode === 0) {
            console.log('✅ 钉钉消息发送成功');
            resolve(result);
          } else {
            console.error('❌ 钉钉发送失败:', result);
            reject(new Error(`DingTalk error: ${result.errmsg}`));
          }
        } catch (e) {
          console.error('❌ 解析响应失败:', data);
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  const args = process.argv.slice(2);
  const pageUrl = args[0];
  const title = args[1] || `AI 资讯日报`;

  if (!pageUrl) {
    console.error('Usage: node dingtalk-notify.js <url> [title]');
    process.exit(1);
  }

  const today = new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    timeZone: 'Asia/Shanghai'
  });

  const text = `### 📰 ${title}\n\n` +
    `📅 ${today}\n\n` +
    `[👉 点击查看今日 AI 资讯](${pageUrl})`;

  await sendMessage({ title, text });
}

main().catch(err => {
  console.error('Fatal:', err.message);
  process.exit(1);
});
