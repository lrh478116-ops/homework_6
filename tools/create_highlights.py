from pathlib import Path
from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "doc"
OUT.mkdir(parents=True, exist_ok=True)
TARGET = OUT / "网站关键亮点说明.docx"
IMG = ROOT / "output" / "media" / "screenshots"

INK = "23302F"
JADE = "286F62"
PALE = "EAF3F0"
LINE = "D9E1DE"
CLAY = "A6614F"


def set_cell_shading(cell, color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), color)


def set_cell_border(cell, color=LINE, size="4"):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = "w:" + edge
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:color"), color)


def font(run, size=None, bold=None, color=INK):
    run.font.name = "Microsoft YaHei"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    run.font.color.rgb = RGBColor.from_string(color)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run("第 ")
    font(run, 8, color="6A7472")
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    paragraph._p.append(fld)
    run = paragraph.add_run(" 页")
    font(run, 8, color="6A7472")


def add_heading(doc, text, level=1):
    p = doc.add_paragraph(style=f"Heading {level}")
    p.paragraph_format.space_before = Pt(14 if level == 1 else 9)
    p.paragraph_format.space_after = Pt(5)
    run = p.add_run(text)
    font(run, 18 if level == 1 else 13, True, INK if level == 1 else JADE)
    return p


def add_body(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.35
    if bold_prefix and text.startswith(bold_prefix):
        r = p.add_run(bold_prefix)
        font(r, 10.5, True, JADE)
        r = p.add_run(text[len(bold_prefix):])
        font(r, 10.5)
    else:
        r = p.add_run(text)
        font(r, 10.5)
    return p


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text)
    font(r, 8.5, color="687270")


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    hdr = table.rows[0].cells
    for i, value in enumerate(headers):
        hdr[i].text = ""
        set_cell_shading(hdr[i], JADE)
        set_cell_border(hdr[i], "FFFFFF")
        hdr[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        r = hdr[i].paragraphs[0].add_run(value)
        font(r, 9, True, "FFFFFF")
        if widths:
            hdr[i].width = Inches(widths[i])
    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = ""
            set_cell_shading(cells[i], "FFFFFF" if len(table.rows) % 2 else "F6F8F7")
            set_cell_border(cells[i])
            cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(str(value))
            font(r, 8.5)
            if widths:
                cells[i].width = Inches(widths[i])
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return table


doc = Document()
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.top_margin = Inches(0.68)
section.bottom_margin = Inches(0.62)
section.left_margin = Inches(0.72)
section.right_margin = Inches(0.72)
section.header_distance = Inches(0.28)
section.footer_distance = Inches(0.3)

styles = doc.styles
styles["Normal"].font.name = "Microsoft YaHei"
styles["Normal"]._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
styles["Normal"].font.size = Pt(10.5)
for name in ("Title", "Heading 1", "Heading 2"):
    styles[name].font.name = "Microsoft YaHei"
    styles[name]._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    styles[name].font.color.rgb = RGBColor.from_string("000000")

header = section.header.paragraphs[0]
header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = header.add_run("石油勘探开发智能化可能性地图  网站关键亮点")
font(r, 8, True, JADE)
add_page_number(section.footer.paragraphs[0])

title = doc.add_paragraph(style="Title")
title.paragraph_format.space_after = Pt(7)
r = title.add_run("石油勘探开发智能化可能性地图网站关键亮点")
font(r, 25, True, "000000")

meta = doc.add_paragraph()
meta.paragraph_format.space_after = Pt(12)
for i, text in enumerate(["舒鼎立", "学号 2407040125", "第 12 类 运输", "2026 年 11 月 5 日"]):
    if i:
        rr = meta.add_run("   ·   ")
        font(rr, 9, color="89918F")
    rr = meta.add_run(text)
    font(rr, 9, i < 2, JADE if i < 3 else "687270")

intro = doc.add_table(rows=1, cols=1)
intro.alignment = WD_TABLE_ALIGNMENT.CENTER
cell = intro.cell(0, 0)
set_cell_shading(cell, PALE)
set_cell_border(cell, "A9C9C0", "7")
p = cell.paragraphs[0]
p.paragraph_format.space_after = Pt(0)
r = p.add_run("交付结论  ")
font(r, 10.5, True, JADE)
r = p.add_run("我完成了运输环节全部 5 个子类别案例，并将其接入同一个纯前端门户。每个案例都能独立打包上传，也能在发布站点直接浏览；专业背景、案例流程和数据演示均有可视化表达。")
font(r, 10.5)

add_heading(doc, "一 交付范围", 1)
add_body(doc, "网站保留原框架的 13 个石油勘探开发环节和 61 个候选场景，并新增运输环节 5 个可运行案例。案例包与站内版本来自同一份源数据，减少单独维护造成的内容差异。")
add_table(doc, ["交付项", "数量", "说明"], [
    ["运输案例", "5 个", "覆盖 t1 至 t5 全部必做子类别"],
    ["独立案例包", "5 个 ZIP", "文件名采用 运输 小类别 形式"],
    ["门户网站", "1 套", "纯 HTML CSS JavaScript 无后端"],
    ["可视化层次", "3 层", "专业背景 案例流程 交互演示"],
    ["负向控制", "5 组", "用于验证关键模型输入确实改变结果"]
], [1.35, 1.0, 4.45])

doc.add_picture(str(IMG / "home.png"), width=Inches(6.75))
add_caption(doc, "图 1  门户总览 13 个环节与 61 个场景保留在统一导航中")

doc.add_page_break()
add_heading(doc, "二 已实现的五个案例", 1)
add_table(doc, ["场景", "智能方法", "核心业务量", "反事实检查"], [
    ["管道泄漏智能检测", "时序异常检测", "进出口质量平衡残差", "泄漏调为零后由已检测变为未报警"],
    ["管道腐蚀智能评估", "多源风险模型", "壁厚损失与环境风险", "仅壁厚后最高风险由 62% 变为 27%"],
    ["集输系统工况优化", "约束优化", "流量 压力 能耗", "关闭约束后推荐变为不可执行"],
    ["油气计量智能校正", "回归校正", "原始读数与参考真值误差", "关闭校正后误差改善归零"],
    ["储罐液位泄漏监控", "多模态异常检测", "液位残差与热异常", "屏蔽热通道后由已检测变为未报警"]
], [1.55, 1.15, 2.0, 2.35])

add_heading(doc, "三 我认为做得好的部分", 1)
add_body(doc, "1 业务机理和智能方法形成一条链。 每个案例先解释石油场景中的物理量，再说明模型读取哪些数据、如何计算以及输出用于什么决策。例如泄漏案例不是直接展示分类结果，而是先构造质量平衡残差，再用健康窗口标准化并做连续越阈确认。")
add_body(doc, "2 可视化覆盖三个部分。 专业背景使用流程、分层、融合和边界图解释概念；案例流程的每一步都显示输入、处理和输出；案例演示把控制参数、现场计算指标和图形结果放在同一视图中。")
add_body(doc, "3 交互结果可反事实验证。 五个演示都提供负向控制。关闭约束、关闭校正或屏蔽传感器通道后，结果会按计算链发生变化，而不是只改变按钮文字或说明文本。")
add_body(doc, "4 明确说明证据边界。 页面统一标记固定种子、教学合成数据和非现场性能结论，防止把演示中的检测延迟或误差改善误写成真实生产绩效。")

doc.add_picture(str(IMG / "t3-demo.png"), width=Inches(6.75))
add_caption(doc, "图 2  集输工况优化演示同时显示目标 输量压力边界 推荐动作和可执行性")

doc.add_page_break()
add_heading(doc, "四 兼容性与可维护性", 1)
add_body(doc, "原网站的添加案例入口保持不变。新案例继续使用 case.json 加 demo 文件夹的契约，其他同学按原样制作的案例仍可上传。框架只增加向后兼容的 visual 字段；旧案例没有这些字段时仍按原样渲染。")
add_body(doc, "五个案例采用单一源构建。构建脚本同时生成站内注册文件和独立 ZIP，因此站内演示、提交压缩包与文档所描述的案例来自同一份配置。")
add_table(doc, ["正式链路", "当前实现"], [
    ["案例清单", "case.json 定义场景 方法 背景 流程和演示入口"],
    ["站内注册", "CaseImport.registerBundled 复用上传案例的 toCase 转换"],
    ["主页面消费", "Cases.register 后由场景页真实读取并生成三个标签页"],
    ["演示执行", "demo 页面进入 sandbox iframe 运行 不污染主站"],
    ["上传安全", "主站正文用 HTML 允许列表清洗 演示脚本仍在沙箱执行"]
], [1.55, 5.2])

add_heading(doc, "五 当前验证证据", 1)
add_body(doc, "静态校验命令通过 5 个运输案例，检查场景绑定、四段专业背景、四步流程、声明式可视化、演示入口、配置文件、独立 ZIP 和框架组件。")
add_body(doc, "真实浏览器检查确认 t1 至 t5 都能进入案例演示，均显示教学合成数据、实验控制、现场计算指标和从石油场景到智能化决策的解释。泄漏、腐蚀、集输、计量和储罐五组反事实均改变了业务结果。")
add_body(doc, "未验证项也保留在页面中：合成数据不能证明现场检测率、误报率、节能收益或计量准确度。真实部署前仍需历史事件、盲测数据、工程规范和现场联锁验证。")

add_heading(doc, "六 提交文件说明", 1)
add_table(doc, ["目录", "用途"], [
    ["dist", "可直接发布的网站文件"],
    ["output cases", "五个独立案例压缩包"],
    ["output doc", "网站关键亮点说明"],
    ["output pdf", "课程结课报告"],
    ["output video", "不超过五分钟的讲解视频与讲稿"]
], [1.55, 5.2])

doc.core_properties.title = "石油勘探开发智能化可能性地图网站关键亮点"
doc.core_properties.author = "舒鼎立"
doc.core_properties.subject = "课程大作业网站关键亮点说明"
doc.save(TARGET)
print(TARGET)
