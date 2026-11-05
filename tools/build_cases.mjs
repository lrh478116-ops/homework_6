import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const sourceRoot = path.join(root, 'case-src');
const sharedRoot = path.join(sourceRoot, 'shared');
const outputRoot = path.join(root, 'output', 'cases');
const downloadRoot = path.join(root, 'dist', 'downloads', 'cases');
const stagingRoot = path.join(root, '.build', 'cases');
const bundlePath = path.join(root, 'dist', 'assets', 'cases', 'transport-bundled.case.js');

const cases = [
  ['pipeline-leak-detection', '运输-管道泄漏智能检测.zip'],
  ['pipeline-corrosion-assessment', '运输-管道腐蚀智能评估.zip'],
  ['gathering-network-optimization', '运输-集输系统工况优化.zip'],
  ['multiphase-meter-calibration', '运输-油气计量智能校正.zip'],
  ['tank-level-leak-monitoring', '运输-储罐液位与泄漏智能监控.zip']
];

const crcTable = new Uint32Array(256);
for (let n = 0; n < 256; n += 1) {
  let c = n;
  for (let k = 0; k < 8; k += 1) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
  crcTable[n] = c >>> 0;
}

function crc32(bytes) {
  let c = 0xFFFFFFFF;
  for (const byte of bytes) c = crcTable[(c ^ byte) & 0xFF] ^ (c >>> 8);
  return (c ^ 0xFFFFFFFF) >>> 0;
}

function makeStoredZip(entries) {
  // 固定时间戳使相同源码生成逐字节一致的提交包；路径统一使用 ZIP 标准的正斜杠。
  const dosTime = (12 << 11);
  const dosDate = ((2026 - 1980) << 9) | (11 << 5) | 5;
  const locals = [];
  const centrals = [];
  let offset = 0;

  for (const entry of entries) {
    const name = entry.name.replaceAll('\\', '/');
    const nameBytes = Buffer.from(name, 'utf8');
    const data = Buffer.isBuffer(entry.data) ? entry.data : Buffer.from(entry.data);
    const crc = crc32(data);

    const local = Buffer.alloc(30 + nameBytes.length);
    local.writeUInt32LE(0x04034b50, 0);
    local.writeUInt16LE(20, 4);
    local.writeUInt16LE(0x0800, 6);
    local.writeUInt16LE(0, 8);
    local.writeUInt16LE(dosTime, 10);
    local.writeUInt16LE(dosDate, 12);
    local.writeUInt32LE(crc, 14);
    local.writeUInt32LE(data.length, 18);
    local.writeUInt32LE(data.length, 22);
    local.writeUInt16LE(nameBytes.length, 26);
    nameBytes.copy(local, 30);

    const central = Buffer.alloc(46 + nameBytes.length);
    central.writeUInt32LE(0x02014b50, 0);
    central.writeUInt16LE(20, 4);
    central.writeUInt16LE(20, 6);
    central.writeUInt16LE(0x0800, 8);
    central.writeUInt16LE(0, 10);
    central.writeUInt16LE(dosTime, 12);
    central.writeUInt16LE(dosDate, 14);
    central.writeUInt32LE(crc, 16);
    central.writeUInt32LE(data.length, 20);
    central.writeUInt32LE(data.length, 24);
    central.writeUInt16LE(nameBytes.length, 28);
    central.writeUInt32LE(offset, 42);
    nameBytes.copy(central, 46);

    locals.push(local, data);
    centrals.push(central);
    offset += local.length + data.length;
  }

  const centralSize = centrals.reduce((sum, entry) => sum + entry.length, 0);
  const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0);
  end.writeUInt16LE(entries.length, 8);
  end.writeUInt16LE(entries.length, 10);
  end.writeUInt32LE(centralSize, 12);
  end.writeUInt32LE(offset, 16);
  return Buffer.concat([...locals, ...centrals, end]);
}

for (const dir of [outputRoot, downloadRoot, stagingRoot]) fs.mkdirSync(dir, { recursive: true });
fs.rmSync(stagingRoot, { recursive: true, force: true });
fs.mkdirSync(stagingRoot, { recursive: true });

const records = [];
for (const [id, zipName] of cases) {
  const src = path.join(sourceRoot, id);
  const pkg = JSON.parse(fs.readFileSync(path.join(src, 'case.json'), 'utf8'));
  const stage = path.join(stagingRoot, id);
  const demo = path.join(stage, 'demo');
  fs.mkdirSync(demo, { recursive: true });
  fs.copyFileSync(path.join(src, 'case.json'), path.join(stage, 'case.json'));
  fs.copyFileSync(path.join(sharedRoot, 'index.html'), path.join(demo, 'index.html'));
  fs.copyFileSync(path.join(sharedRoot, 'demo.css'), path.join(demo, 'demo.css'));
  fs.copyFileSync(path.join(sharedRoot, 'demo.js'), path.join(demo, 'demo.js'));
  fs.copyFileSync(path.join(src, 'config.js'), path.join(demo, 'config.js'));

  const files = ['demo/index.html', 'demo/demo.css', 'demo/config.js', 'demo/demo.js'].map((name) => {
    const abs = path.join(stage, ...name.split('/'));
    const data = fs.readFileSync(abs, 'utf8');
    return { name, size: Buffer.byteLength(data), mime: name.endsWith('.html') ? 'text/html' : name.endsWith('.css') ? 'text/css' : 'text/javascript', enc: 'text', data };
  });
  records.push({ pkg, meta: { id: pkg.id, sceneId: pkg.sceneId, title: pkg.title, version: pkg.version, updated: pkg.updated, methods: pkg.methods }, files, source: 'bundled' });

  const out = path.join(outputRoot, zipName);
  const zipEntries = [
    { name: 'case.json', data: fs.readFileSync(path.join(stage, 'case.json')) },
    ...files.map((file) => ({ name: file.name, data: fs.readFileSync(path.join(stage, ...file.name.split('/'))) }))
  ];
  fs.writeFileSync(out, makeStoredZip(zipEntries));
  fs.copyFileSync(out, path.join(downloadRoot, zipName));
}

const js = `/* 自动生成：tools/build_cases.mjs。请勿手改。 */\n(function(){\n  var records=${JSON.stringify(records).replaceAll('</script', '<\\/script')};\n  if(!window.CaseImport||!window.CaseImport.registerBundled){throw new Error('CaseImport.registerBundled 未就绪');}\n  window.CaseImport.registerBundled(records);\n})();\n`;
fs.writeFileSync(bundlePath, js, 'utf8');
console.log(`Built ${records.length} case ZIPs and ${path.relative(root, bundlePath)}`);
