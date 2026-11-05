import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const root = path.resolve(import.meta.dirname, '..');
const dist = path.join(root, 'dist');
const errors = [];

function fail(message) {
  errors.push(message);
}

const htmlFiles = [];
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const absolute = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(absolute);
    else if (entry.name.endsWith('.html')) htmlFiles.push(absolute);
  }
}

walk(dist);
for (const htmlPath of htmlFiles) {
  const source = fs.readFileSync(htmlPath, 'utf8');
  const activeSource = source.replace(/<!--[\s\S]*?-->/g, '');
  const base = path.dirname(htmlPath);
  for (const match of activeSource.matchAll(/(?:src|href)=["']([^"']+)["']/g)) {
    const raw = match[1];
    if (/^(?:https?:|mailto:|tel:|data:|#)/i.test(raw)) continue;
    if (raw.startsWith('/')) {
      fail(`${path.relative(root, htmlPath)} 使用站点根绝对路径：${raw}`);
      continue;
    }
    const clean = raw.split(/[?#]/, 1)[0];
    if (!clean) continue;
    const target = path.resolve(base, ...clean.split('/'));
    if (!fs.existsSync(target)) fail(`${path.relative(root, htmlPath)} 引用了不存在的文件：${raw}`);
  }
}

const indexPath = path.join(dist, 'index.html');
const index = fs.readFileSync(indexPath, 'utf8');
const activeIndex = index.replace(/<!--[\s\S]*?-->/g, '');
const uploadPos = activeIndex.indexOf('case-upload.js');
const bundlePos = activeIndex.indexOf('transport-bundled.case.js');
const shellPos = activeIndex.indexOf('shell.js');
if (!(uploadPos >= 0 && bundlePos > uploadPos && shellPos > bundlePos)) {
  fail('入口脚本顺序错误：上传注册器 → 运输内置案例 → shell 必须依次加载');
}

const bundle = fs.readFileSync(path.join(dist, 'assets', 'cases', 'transport-bundled.case.js'), 'utf8');
for (const id of [
  'pipeline-leak-detection',
  'pipeline-corrosion-assessment',
  'gathering-network-optimization',
  'multiphase-meter-calibration',
  'tank-level-leak-monitoring'
]) {
  if (!bundle.includes(`"id":"${id}"`)) fail(`站内案例注册包缺少 ${id}`);
}

const manifestFiles = fs.readdirSync(path.join(root, 'case-src'), { withFileTypes: true })
  .filter((entry) => entry.isDirectory() && entry.name !== 'shared')
  .map((entry) => path.join(root, 'case-src', entry.name, 'case.json'));
for (const manifestPath of manifestFiles) {
  const raw = fs.readFileSync(manifestPath, 'utf8');
  if (/\son[a-z]+\s*=|javascript:/i.test(raw)) {
    fail(`${path.relative(root, manifestPath)} 含危险事件属性或 javascript: URL`);
  }
}

if (errors.length) {
  console.error(`DIST VALIDATION FAILED (${errors.length})`);
  errors.forEach((error) => console.error(`- ${error}`));
  process.exit(1);
}

console.log(`DIST VALIDATION PASSED (${htmlFiles.length} HTML files, 5 bundled cases)`);
