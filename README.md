# 石油勘探开发的智能化可能性地图

课程大作业提交仓库。作者：舒鼎立（2407040125）。学号末两位为 25，按 13 个类别循环对应第 12 类“运输”，因此本项目完整实现运输环节的 5 个子类别案例。

## 在线网站

GitHub Pages：<https://lrh478116-ops.github.io/homework_6/>

站点是纯前端应用，不依赖后端、数据库或在线推理服务。首次发布由 `.github/workflows/pages.yml` 自动把 `dist/` 部署到 GitHub Pages。

## 已实现案例

1. 管道泄漏智能检测：质量平衡残差 + 时序异常检测。
2. 管道腐蚀智能评估：壁厚、环境与服役信息的多源风险分区。
3. 集输系统工况优化：流量/压力硬约束下的泵阀协同。
4. 油气计量智能校正：工况特征驱动的计量偏差补偿。
5. 储罐液位与泄漏智能监控：液位质量平衡与热异常融合。

每个案例都有专业背景、案例流程和案例演示。专业概念与流程步骤使用声明式图示，演示指标由当前参数与固定种子合成数据在浏览器中实时计算，并包含至少一种反事实或负向控制。页面明确说明这些结果不是现场性能结论。

## 提交文件

- 网站发布目录：[`dist/`](dist/)
- 五个独立案例压缩包：[`output/cases/`](output/cases/)
- 网站关键亮点说明：[`output/doc/网站关键亮点说明.docx`](output/doc/%E7%BD%91%E7%AB%99%E5%85%B3%E9%94%AE%E4%BA%AE%E7%82%B9%E8%AF%B4%E6%98%8E.docx)
- 结课报告：[`output/pdf/石油勘探开发智能化可能性地图结课报告.pdf`](output/pdf/%E7%9F%B3%E6%B2%B9%E5%8B%98%E6%8E%A2%E5%BC%80%E5%8F%91%E6%99%BA%E8%83%BD%E5%8C%96%E5%8F%AF%E8%83%BD%E6%80%A7%E5%9C%B0%E5%9B%BE%E7%BB%93%E8%AF%BE%E6%8A%A5%E5%91%8A.pdf)
- 讲解视频与讲稿：[`output/video/`](output/video/)
- 单一案例源：[`case-src/`](case-src/)
- 构建与验证脚本：[`tools/`](tools/) 与 [`tests/`](tests/)
- 验收记录：[`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md)

结课报告已根据五次作业重写为“可视化课程结课报告：五次作业的可视化实现与学习总结”，共 10 页（封面 1 页、正文与附录 9 页）。重点分析布局实验、AI 效率对比、FrameFlow 数据联动、可视化编码实验以及石油案例图示，配有 7 幅图和实现索引。为保持提交链接不变，沿用原 PDF 文件名；其他提交文件未随本次报告修订而改变。

报告重建与结构检查（需要 Python、ReportLab、Pillow、pypdf、pdfplumber，以及 Windows 微软雅黑字体）：

```powershell
python tools/create_report.py
python tests/validate_report.py
```

结构检查不代替逐页视觉检查，也不代表重新验收五个历史网站。

## 本地运行

直接打开 `dist/index.html` 即可。若浏览器对本地 `file://` 的脚本策略较严格，可在仓库根目录运行：

```powershell
python -m http.server 8765 --directory dist
```

然后访问 <http://127.0.0.1:8765/>。

## 重新构建与校验

本机需要 Node.js 与 PowerShell：

```powershell
node tools/build_cases.mjs
node tests/validate_cases.mjs
node tests/validate_dist.mjs
```

构建脚本从 `case-src/` 同时生成站内案例注册文件和 5 个独立 ZIP，避免网站版本与提交案例包发生内容漂移。

## 添加案例兼容性

五个 ZIP 解压后均保持教师框架约定的结构：

```text
case.json
demo/
  index.html
  demo.css
  config.js
  demo.js
```

在网站中点击“添加案例”，选择解压后的案例目录即可校验并接入。演示代码只在沙箱 iframe 中执行；背景正文进入主页面前经过允许列表清洗。
