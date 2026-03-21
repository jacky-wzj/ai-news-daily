const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data/2026-03-21.json','utf8'));
const seen = JSON.parse(fs.readFileSync('seen_urls.json','utf8'));
const newUrls = [];
for (const key of Object.keys(data)) {
  if (Array.isArray(data[key])) {
    for (const item of data[key]) {
      if (item.link && !seen.urls.includes(item.link)) {
        newUrls.push(item.link);
      }
    }
  }
}
seen.urls.push(...newUrls);
seen.lastUpdated = '2026-03-21';
fs.writeFileSync('seen_urls.json', JSON.stringify(seen, null, 2));
console.log('Added', newUrls.length, 'new URLs');
