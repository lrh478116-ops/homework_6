import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { spawnSync } from 'node:child_process';

const root = path.resolve(import.meta.dirname, '..');
const sourceRoot = path.join(root, 'case-src');
const distRoot = path.join(root, 'dist');

const expected = [
  ['管道泄漏智能检测', 'pipeline-leak-detection', 't1'],
  ['管道腐蚀智能评估', 'pipeline-corrosion-assessment', 't2'],
  ['集输系统工况优化', 'gathering-network-optimization', 't3'],
  ['油气计量智能校正', 'multiphase-meter-calibration', 't4'],
  ['储罐液位与泄漏智能监控', 'tank-level-leak-monitoring', 't5']
];

const errors = [];
const ids = new Set();

function fail(message) {
  errors.push(message);
}

for (const [sceneName, id, sceneId] of expected) {
  const manifestPath = path.join(sourceRoot, id, 'case.json');
  if (!fs.existsSync(manifestPath)) {
    fail(`缺少案例清单：${id}`);
    continue;
  }
  let manifest;
  try {
    manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  } catch (error) {
    fail(`${id} 的 case.json 无法解析：${error.message}`);
    continue;
  }
  if (manifest.id !== id) fail(`${id} 的 manifest.id 不一致`);
  if (manifest.sceneId !== sceneId) fail(`${id} 应绑定 ${sceneId}，实际为 ${manifest.sceneId}`);
  if (ids.has(manifest.id)) fail(`案例 id 重复：${manifest.id}`);
  ids.add(manifest.id);
  if (!Array.isArray(manifest.methods) || !manifest.methods.length) fail(`${id} 缺少 AI 方法标签`);
  const background = manifest.tabs?.background;
  if (!background || !Array.isArray(background.sections) || background.sections.length < 4) {
    fail(`${id} 的专业背景不足四段`);
  } else {
    background.sections.forEach((section, index) => {
      if (!section.title || !section.html) fail(`${id} 背景第 ${index + 1} 段缺标题或正文`);
      if (!section.visual || !section.visual.type) fail(`${id} 背景第 ${index + 1} 段缺声明式可视化`);
    });
  }
  if (!Array.isArray(background?.judge) || background.judge.length !== 4) {
    fail(`${id} 的 30 秒判断区必须正好包含四项`);
  }
  const workflow = manifest.tabs?.workflow;
  if (!workflow || !Array.isArray(workflow.steps) || workflow.steps.length < 4) {
    fail(`${id} 的案例流程不足四步`);
  } else {
    workflow.steps.forEach((step, index) => {
      if (!step.name || !step.do || !step.effect || !step.trap) fail(`${id} 流程第 ${index + 1} 步字段不全`);
      if (!step.visual?.input || !step.visual?.process || !step.visual?.output) {
        fail(`${id} 流程第 ${index + 1} 步缺输入处理输出图示`);
      }
    });
  }
  const demo = manifest.tabs?.demo;
  if (!demo || demo.mode !== 'page' || demo.html !== 'demo/index.html') fail(`${id} 没有声明整页沙箱演示`);
  const configPath = path.join(sourceRoot, id, 'config.js');
  if (!fs.existsSync(configPath)) fail(`${id} 缺少演示配置`);
  const zipPath = path.join(root, 'output', 'cases', `运输-${sceneName}.zip`);
  if (!fs.existsSync(zipPath)) {
    fail(`缺少最终压缩包：运输-${sceneName}.zip`);
  } else {
    const script = [
      'Add-Type -AssemblyName System.IO.Compression.FileSystem',
      `$a=[System.IO.Compression.ZipFile]::OpenRead('${zipPath.replaceAll("'", "''")}')`,
      'try{$a.Entries|ForEach-Object FullName}finally{$a.Dispose()}'
    ].join(';');
    const result = spawnSync('powershell.exe', ['-NoLogo', '-NoProfile', '-Command', script], { encoding: 'utf8' });
    const names = result.stdout.trim().split(/\r?\n/).filter(Boolean);
    const required = ['case.json', 'demo/index.html', 'demo/demo.css', 'demo/config.js', 'demo/demo.js'];
    if (result.status !== 0) fail(`${id} 的 ZIP 无法读取：${result.stderr.trim()}`);
    required.forEach((name) => { if (!names.includes(name)) fail(`${id} 的 ZIP 缺少标准路径 ${name}`); });
    if (names.some((name) => name.includes('\\'))) fail(`${id} 的 ZIP 使用了非标准反斜杠路径`);
  }
}

const uploader = path.join(distRoot, 'assets', 'core', 'case-upload.js');
const kit = path.join(distRoot, 'assets', 'core', 'kit.js');
if (fs.existsSync(uploader)) {
  const source = fs.readFileSync(uploader, 'utf8');
  if (!source.includes('sanitizeHTML')) fail('上传路径缺少 HTML 允许列表清洗');
  if (!source.includes('registerBundled')) fail('上传路径缺少同源内置案例注册接口');
}
if (fs.existsSync(kit)) {
  const source = fs.readFileSync(kit, 'utf8');
  if (!source.includes('conceptVisual')) fail('渲染工具箱缺少背景概念图组件');
  if (!source.includes('stepVisual')) fail('渲染工具箱缺少流程步骤图组件');
}

if (errors.length) {
  console.error(`CASE VALIDATION FAILED (${errors.length})`);
  errors.forEach((error) => console.error(`- ${error}`));
  process.exit(1);
}

console.log(`CASE VALIDATION PASSED (${expected.length} transport cases)`);
