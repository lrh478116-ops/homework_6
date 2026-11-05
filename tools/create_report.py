"""Course report: python tools/create_report.py (ReportLab, Pillow, YaHei fonts)."""
from io import BytesIO
from pathlib import Path
from math import sin, cos, pi, floor
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, Flowable
from reportlab.lib import textsplit
from reportlab.platypus import paragraph as paragraph_module

# ReportLab's default Japanese kinsoku set omits several Chinese punctuation
# marks. Extend the process-local rules for both simple and rich paragraphs.
textsplit.ALL_CANNOT_START += '，；：？！）》”’'
paragraph_module.ALL_CANNOT_START = textsplit.ALL_CANNOT_START

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf'
ASSETS = ROOT / 'output/media/report'
TARGET = OUT / '石油勘探开发智能化可能性地图结课报告.pdf'
WIDTH = 166 * mm
INK = colors.HexColor('#253633')
GREEN = colors.HexColor('#286F62')
GRAY = colors.HexColor('#65746F')
PALE = colors.HexColor('#F1F5F3')
LINE = colors.HexColor('#D5DFDA')
ORANGE = colors.HexColor('#AC633E')
pdfmetrics.registerFont(TTFont('CN', 'C:/Windows/Fonts/msyh.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('CNB', 'C:/Windows/Fonts/msyhbd.ttc', subfontIndex=0))
pdfmetrics.registerFontFamily('CN', normal='CN', bold='CNB', italic='CN', boldItalic='CNB')
STYLES = {
    'title': ParagraphStyle('title', fontName='CNB', fontSize=26, leading=38, textColor=INK, alignment=TA_CENTER, spaceAfter=15),
    'subtitle': ParagraphStyle('subtitle', fontName='CN', fontSize=12, leading=21, textColor=GRAY, alignment=TA_CENTER, spaceAfter=12),
    'h1': ParagraphStyle('h1', fontName='CNB', fontSize=18, leading=26, textColor=INK, spaceAfter=12),
    'h2': ParagraphStyle('h2', fontName='CNB', fontSize=11.5, leading=18, textColor=GREEN, spaceBefore=9, spaceAfter=5),
    'body': ParagraphStyle('body', fontName='CN', fontSize=10, leading=17.5, textColor=INK, firstLineIndent=20, spaceAfter=7),
    'flat': ParagraphStyle('flat', fontName='CN', fontSize=9.5, leading=16, textColor=INK, spaceAfter=6),
    'caption': ParagraphStyle('caption', fontName='CN', fontSize=8, leading=12, textColor=GRAY, alignment=TA_CENTER, spaceBefore=5, spaceAfter=9),
    'small': ParagraphStyle('small', fontName='CN', fontSize=8, leading=12.5, textColor=GRAY, spaceAfter=6),
    'cell': ParagraphStyle('cell', fontName='CN', fontSize=8.7, leading=14, textColor=INK),
    'headcell': ParagraphStyle('headcell', fontName='CNB', fontSize=9, leading=14, textColor=colors.white),
    'note': ParagraphStyle('note', fontName='CN', fontSize=9.5, leading=17, textColor=INK, backColor=PALE, borderPadding=9, borderWidth=.5, borderColor=LINE, spaceBefore=9, spaceAfter=10),
}
for style in STYLES.values():
    style.wordWrap = 'CJK'


def p(text, style='body'):
    return Paragraph(text, STYLES[style])


def tbl(rows, widths):
    cells = [[p(str(v), 'headcell' if i == 0 else 'cell') for v in row] for i, row in enumerate(rows)]
    t = Table(cells, colWidths=[v * mm for v in widths], repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), GREEN),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PALE]),
        ('GRID', (0, 0), (-1, -1), .4, LINE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def shot(name, crop=None, max_height=99 * mm):
    im = PILImage.open(ASSETS / name).convert('RGB')
    if crop:
        im = im.crop(crop)
    scale = min(WIDTH / im.width, max_height / im.height)
    stream = BytesIO()
    im.save(stream, 'PNG')
    stream.seek(0)
    return Image(stream, width=im.width * scale, height=im.height * scale)


class Diagram(Flowable):
    """Code-derived educational diagrams, explicitly not UI screenshots."""
    def __init__(self, kind, height):
        super().__init__()
        self.kind, self.width, self.height = kind, WIDTH, height * mm

    def draw(self):
        c, w, h = self.canv, self.width, self.height
        c.setFillColor(PALE)
        c.roundRect(0, 0, w, h, 6, fill=1, stroke=0)

        def text(x, y, s, size=9, color=INK, bold=False):
            c.setFillColor(color)
            c.setFont('CNB' if bold else 'CN', size)
            c.drawString(x, y, s)

        def box(x, y, bw, bh, label, color=GREEN):
            c.setFillColor(colors.white)
            c.setStrokeColor(color)
            c.roundRect(x, y, bw, bh, 4, fill=1, stroke=1)
            text(x + 8, y + bh / 2 - 3, label, 9, color)

        def arrow(x1, y1, x2, y2):
            c.setStrokeColor(GRAY)
            c.line(x1, y1, x2, y2)
            c.line(x2-4, y2+3, x2, y2)
            c.line(x2-4, y2-3, x2, y2)

        if self.kind == 'layout':
            text(15, h-24, '参数编辑 → 合法性校验 → CSS 变量 → iframe 内真实排版', 10, GREEN, True)
            for x, bw, label, cols in [(16, 260, 'Desktop · 1100 px', 3), (301, 152, 'Mobile · 390 px', 1)]:
                box(x, 31, bw, h-74, '', GRAY)
                text(x+10, h-63, label, 9)
                c.setFillColor(GREEN)
                c.rect(x+12, h-81, bw-24, 6, fill=1, stroke=0)
                cw = (bw-24-8*(cols-1))/cols
                for k in range(3):
                    row, col = divmod(k, cols)
                    c.setFillColor(colors.HexColor('#D9E7E0'))
                    c.roundRect(x+12+col*(cw+8), h-111-row*32, cw, 25, 3, fill=1, stroke=0)
            text(16, 13, '先改变虚拟视口宽度触发重排，再按容器缩放显示；不是把同一张页面简单缩小。', 8)
        elif self.kind == 'baseline':
            for j, baseline in enumerate((0, 75)):
                ox = 35 + j*235
                text(ox, h-20, f'纵轴起点 {baseline}；数据均为 82 与 95', 9, GREEN, True)
                axis_y, chart_h = 30, h-62
                c.setStrokeColor(GRAY)
                c.line(ox, axis_y, ox+175, axis_y)
                c.line(ox, axis_y, ox, axis_y+chart_h)
                for tick in (baseline, 100):
                    ty = axis_y+(tick-baseline)/(100-baseline)*chart_h
                    text(ox-24, ty-3, str(tick), 8, GRAY)
                for k, value in enumerate((82, 95)):
                    bh = (value-baseline)/(100-baseline)*chart_h
                    c.setFillColor(GREEN if k==0 else ORANGE)
                    c.rect(ox+28+k*75, axis_y, 42, bh, stroke=0, fill=1)
                    text(ox+36+k*75, axis_y+bh+4, str(value), 8)
                text(ox+20, 11, f'柱高比 {(95-baseline)/(82-baseline):.2f}；数值比始终 1.16', 8)
        elif self.kind == 'series':
            # Match labs.js Math.round, including its integer rounding.
            values = [floor(24+7*sin(2*pi*i/7)+.16*i+3*cos(1.9*i)+.5) for i in range(56)]
            left, bottom, cw, ch = 35, 24, w-55, h-54
            def pt(i, value):
                return left+i/55*cw, bottom+(value-10)/40*ch
            for tick in (10, 30, 50):
                _, y = pt(0, tick)
                c.setStrokeColor(LINE)
                c.line(left, y, left+cw, y)
                text(9, y-3, str(tick), 8, GRAY)
            def path(points, color, lw):
                line = c.beginPath()
                line.moveTo(*points[0])
                for point in points[1:]:
                    line.lineTo(*point)
                c.setStrokeColor(color)
                c.setLineWidth(lw)
                c.drawPath(line)
            path([pt(i, v) for i, v in enumerate(values)], colors.HexColor('#B8CDC1'), 1)
            weekly = [(i+3, sum(values[i:i+7])/7) for i in range(0,56,7)]
            path([pt(i,v) for i,v in weekly], GREEN, 2)
            text(35, h-16, '浅线：56 个每日观测    深线：8 个每周均值（全部观测参与）', 9, GREEN)
            text(35, 8, '第 1 天', 8, GRAY)
            text(w-58, 8, '第 56 天', 8, GRAY)
        elif self.kind == 'process':
            for i, (label, detail) in enumerate([('专业背景', '对象 / 守恒 / 偏差'), ('案例流程', '输入 / 处理 / 输出'), ('案例演示', '参数 / 图形 / 判断')]):
                x = 15+i*155
                box(x, h-65, 130, 34, label)
                text(x+5, h-87, detail, 8)
                if i<2:
                    arrow(x+133, h-48, x+151, h-48)
            text(16, 19, '同一场景逐层展开：先知道“是什么”，再理解“怎样算”，最后观察“怎样变”。', 8)


story = []


def add(text, style='body'):
    if style == 'note':
        story.append(Spacer(1, 3*mm))
    story.append(p(text, style))
    if style == 'note':
        story.append(Spacer(1, 3*mm))


def section(title, subtitle):
    story.append(PageBreak())
    add(title, 'h1')
    add(subtitle, 'flat')


# Cover
story.append(Spacer(1, 30*mm))
add('可视化课程结课报告', 'subtitle')
add('五次作业的可视化实现<br/>与学习总结', 'title')
add('从页面布局、解释性图表到交互分析与领域应用', 'subtitle')
story.append(Spacer(1, 15*mm))
story.append(tbl([
    ['项目', '信息'], ['姓名 / 学号', '舒鼎立 / 2407040125'],
    ['报告范围', '可视化课程第一至第五次作业'], ['结课项目', '石油勘探开发智能化可能性地图'],
    ['结课案例', '第 12 类“运输”的 5 个子类别'], ['日期', '2026 年 11 月 5 日'],
], [38,128]))
story.append(Spacer(1, 17*mm))
add('报告重点：不以页面数量或装饰效果衡量作品，而从视觉编码、交互反馈、数据处理和专业概念表达四个角度，解释五次作业中值得总结的实现。', 'note')
add('依据本地五次作业的实际源码与存档截图编写。文中重绘图均注明用途；教学模拟不作为真实生产绩效或用户学习效果的证明。', 'small')

section('一  我对可视化的理解', '可视化不是数据的外包装，而是让问题、过程和结论变得可检查。')
add('完成五次作业后，我对可视化的认识从“把页面做清楚”逐渐扩展到“让读者通过图形思考”。第一次作业关注空间和布局，第二次用比较解释 AI 的作用，第三次让图表参与数据分析，第四次检验编码本身是否误导，第五次把图示、流程和计算结合到石油运输场景。它们不是五个互不相关的网站，而是同一种能力的递进练习。')
story.append(tbl([
    ['作业', '核心可视化问题', '最值得总结的实现'],
    ['第一次：布局实验室', '抽象布局规则怎样看得见？', '可编辑 CSS 参数与真实虚拟视口'],
    ['第二次：AI 观察站', '怎样比较收益和额外代价？', '统一尺度的分阶段条形图与 A/B 方案'],
    ['第三次：FrameFlow', '图表怎样进入分析过程？', '图表点击筛选、操作历史与多视图联动'],
    ['第四次：学习工作台', '图形编码怎样改变判断？', '基线、色带、时间聚合的控制变量实验'],
    ['第五次：石油案例门户', '陌生专业怎样讲清楚？', '背景图示、逐步流程和可操作的结果图'],
], [44,53,69]))
add('1. 编码必须与问题相匹配', 'h2')
add('比较数量适合用共同基线上的长度，观察变化适合用时间位置，理解工艺关系适合用节点与连线。颜色更适合辅助区分状态或突出重点，不应单独承担精确读数。由此，我更重视单位、图例、数值标签和统计口径，而不是图表是否足够复杂。')
add('2. 交互应当改变理解，而不是只增加动画', 'h2')
add('有意义的交互需要形成可解释的反馈：输入改变后，计算、图形和文字结论一起改变；筛选后，当前数据表和汇总同步更新；切换时间尺度时，读者能够看到哪些细节被保留、哪些被平均。交互的价值是让读者提出问题并检查答案。')
add('3. 可视化也需要呈现自己的边界', 'h2')
add('一个清晰的图也可能表达不可靠的结论。截断坐标轴会放大差异，聚合会隐藏波动，合成数据会产生看似精确的指标。因此，我认为好的作品既要突出信息，也要说明数据来源、建模假设与未验证项。报告中所说的“效果”，主要指实现所支持的阅读与探索方式，不代表已经进行学习效果实验。')

section('二  第一次作业：把布局规则变成可操作实验', '作品：页面布局实验室｜技术：原生 HTML、CSS、JavaScript、sandbox iframe')
add('第一次作业的重点不是统计图，而是把界面布局本身作为可视化对象。层级、间距、Flex、Grid 和响应式设计通常以属性和代码出现；实验室把“讲解、关键代码、演示”放在同一学习单元中，使读者能把规则与实际空间变化对应起来。')
story.append(Diagram('layout', 75))
add('图 1  根据源码重绘的布局实验机制示意；卡片仅表示重排关系，不是页面截图。', 'caption')
add('亮点一：将抽象变量映射到看得见的空间', 'h2')
add('界面将标题字号、卡片内边距、组间距、网格列数等作为可编辑变量。例如层级实验可修改 48 px 标题与 680 px 内容宽度；Grid 实验可以调整 12 列网格中的跨列数。输入通过合法性检查后写入状态，buildPreview 生成预览文档，再由 iframe.srcdoc 更新。错误输入会显示提示并保留最后一次有效状态，而不是让整个示例失效。')
add('亮点二：响应式变化来自真实视口宽度', 'h2')
add('设备按钮分别使用 1100、760、390 px 的虚拟视口；连续滑块可在 320 至 1200 px 间观察变化。实现先设置 iframe 的真实宽度，使内部媒体查询和网格规则重新排版，再用 transform 缩放以适应外层容器。这一区别很重要：读者看到的是换行、列数和留白的变化，而不仅是同一桌面布局的等比例缩小。')
add('亮点三：通过视觉邻近关系解释布局语义', 'h2')
add('间距实验把卡片内部间距、同组间距和区块间距分开调整；Flex 实验让对齐、分布和换行即时显现。这样，“哪些内容属于一组”不再仅靠文字解释，而由空间关系表达。中英双语和代码定位是辅助功能，真正的可视化亮点是变量与结果之间短而明确的反馈链。')
add('我的收获：空间布局也是信息编码。只有分组、层级和阅读顺序稳定，后续复杂图表才不会让读者在界面中迷路。', 'note')

section('三  第二次作业：把 AI 收益讲成可比较的过程', '作品：AI 新质生产力观察站｜技术：SVG 趋势图、比例条形图、参数模拟')
add('这一作业把“AI 能提高效率”的笼统判断拆成覆盖率、数据质量和复核成本三个可调整因素，再把总耗时拆成信息检索、分析判断、内容生产和复核交付四个环节。相比只展示一个提升百分比，分阶段图能够解释收益来自哪里，以及额外工作在哪里产生。')
story.append(shot('ai-lab.png', (240, 289, 1383, 984), 91*mm))
add('图 2  第二次作业存档截图局部：参数、当前结果与四阶段对比在同一视图。', 'caption')
add('亮点一：统一尺度使阶段差异可直接比较', 'h2')
add('四个阶段的条形均采用 0 至 50 分钟的统一范围。灰色代表原流程，蓝色代表 AI 协作，橙色强调额外复核负担，并保留分钟数。不能让每一行都按自己的最大值填满，否则短阶段和长阶段会看起来一样重要。当前模拟允许总耗时增加，因此图形没有把“AI 一定更好”写成预设结论。')
add('亮点二：一个计算结果驱动图、文字与导出', 'h2')
add('模型以覆盖率乘质量得到有效作用比例，按各环节的潜力系数减少耗时，再在复核阶段增加成本。模拟函数的结果被阶段条形、总耗时、吞吐量变化和 CSV 共同读取。默认参数下约 79.1 分钟与约 26.4% 的吞吐量变化是教学公式的计算结果，不是调查统计或企业预测。')
add('亮点三：用方案快照降低比较时的记忆负担', 'h2')
add('用户可保存 A、B 两套参数，系统分别重新计算各阶段耗时和差值。读者不必记住拖动滑块之前的数字，就能定位“复核成本是否抵消前面的收益”。趋势模块中的历史数据、能源估计与预测也分别标注；估计与预测使用不同样式，提醒读者不要把未来预测当作已发生事实。')
add('我的收获：解释性可视化不仅要告诉读者“相差多少”，还应通过拆分、共同尺度和对照说明“为什么相差”。', 'note')

section('四  第三次作业：让图表成为数据分析入口', '作品：FrameFlow 数据工作台｜技术：React、TypeScript、Recharts、数据处理流水线')
story.append(shot('frameflow.png', (233, 212, 1414, 779), 62*mm))
add('图 3  第三次作业存档截图局部：质量概况、时间趋势与分类比较共享当前数据。', 'caption')
add('亮点一：从“展示图表”走向“图表驱动筛选”', 'h2')
add('分类柱形或扇区点击后，DataChart 将原始类别值传给 onSelect；主界面据此创建 filter 操作并加入历史。当前数据表由 replay(source, steps.slice(0, cursor)) 重建，统计卡、图表和导出读取同一处理结果。因此，点击不仅高亮图形，也实际改变分析对象；撤销则能恢复之前的数据状态。')
add('亮点二：按分析问题提供不同图形，而非只换外观', 'h2')
add('折线和面积图用于趋势，条形图用于类别比较，环形图用于非负构成，散点图用于两个数值字段的关系，直方图用 12 个分箱观察分布。图表具备轴标签、提示框和直接读数。折线采用线性连接并关闭入场动画，避免额外平滑或运动制造不存在的数据形状。')
add('亮点三：让数据质量进入分析视野', 'h2')
add('工作台同时显示行数、字段数、缺失值、重复行以及表格预览，使“先检查数据，再解释图形”成为自然顺序。相关系数按成对有效数值计算，缺失不当作零；样本不足时不强行给出相关结论。字段概况与小型分布图帮助定位异常列，减少漂亮图形掩盖数据问题的风险。')
story.append(tbl([
    ['交互或限制', '实际含义', '读图时应注意'],
    ['点击类别', '生成筛选步骤并改变当前表', '全局分析范围改变，可撤销'],
    ['Brush 拖动范围', '仅调整图中的可见区间', '不等于筛选底层数据'],
    ['类别 / 散点数量限制', '最多展示 60 类 / 1500 个点', '绘图截取不等于全量统计'],
], [41,62,63]))
add('我的收获：联动的关键不是多个组件同时刷新，而是它们共享同一数据口径，并清楚区分筛选、显示范围与绘图截取。', 'note')

section('五  第四次作业：用实验揭示编码的影响', '作品：可视化导论学习工作台｜技术：原生 SVG、共享尺度函数、控制变量实验')
add('作品保留课程的 5 章、27 个小节，新增基线、颜色和时间粒度三个交互实验。原课程内容与原有演示不作为我的原创成果；我的重点是把概念整理成能“先预测、再操作、再解释”的学习活动。')
story.append(Diagram('baseline', 53))
add('图 4  根据基线实验重绘：数值不变，仅纵轴起点改变，柱高比例就由 1.16 变为 2.86。', 'caption')
add('亮点一：将误导性可视化变成可重复的对照', 'h2')
add('五组值固定为 82、86、89、91、95，滑块仅改变纵轴起点。柱高和刻度使用同一映射，避免轴与图形各算各的。起点为 75 时，95 与 82 的可见柱高比是 (95-75)/(82-75)=2.86，但真实数值比仍是 95/82=1.16。直接同时显示这两个比例，比只写“柱状图应从零开始”更能解释原因。')
add('亮点二：同一数据矩阵检验不同色带', 'h2')
add('颜色实验固定 4×9 个单元的数值和位置，仅切换顺序、发散、定性色带。数据跨越 -4 至 +4，发散色带以零为中心便于区分正负偏离；定性色带虽能区分类别，却不自然表达连续大小。每格保留数值标签，灰度预览用于检查亮度层次，且明确说明它不是色觉缺陷模拟。')
story.append(Diagram('series', 43))
add('图 5  根据源码生成的同组教学数据：每日波动与每周均值叠加，共享时间位置。', 'caption')
add('亮点三：时间聚合不是把原始点直接删掉', 'h2')
add('时间实验对 56 天数据按 1、7、14 天计算均值，分别形成 56、8、4 个显示点，所有原始观测都参与。聚合点放在原窗口中心，浅色原始线可保留作参照；提示框显示窗口信息，CSV 使用同一聚合结果。读者由此看到：长期趋势更清楚了，但周期和峰值细节也被削弱了。')

section('六  第五次作业：让专业背景与流程看得懂', '作品：石油勘探开发智能化可能性地图｜方向：第 12 类“运输”全部 5 个子类别')
add('学号末两位为 25，按 13 个类别循环对应第 12 类运输。本次完成管道泄漏、管道腐蚀、集输优化、油气计量、储罐监控五个案例。难点不只是给智能方法配图，而是让不了解石油专业的读者先知道被观测的对象、物理关系及输出要服务的决策。')
story.append(Diagram('process', 47))
add('图 6  案例的三层表达结构，根据门户实现重绘。', 'caption')
add('亮点一：用图形关系替代术语堆叠', 'h2')
add('专业背景采用声明式图示：守恒关系使用流程与公式布局，管壁和油气水结构使用分层图，多传感器信息使用融合图，井组、汇管与泵站使用网络图。图形由概念类型与语义字段生成，而非在五个页面中复制不同风格的图片。读者先形成对象关系，再进入异常检测、风险评分或优化任务。')
story.append(tbl([
    ['案例', '先解释的专业概念', '图示如何帮助理解'],
    ['管道泄漏', '入口、出口、管存与残差', '把守恒关系按信息流拆开'],
    ['管道腐蚀', '壁厚损失、环境与服役信息', '分层和融合说明多源影响'],
    ['集输优化', '井组到汇管、阀门、泵站', '拓扑明确控制量作用位置'],
    ['油气计量', '工况造成的系统偏差', '原始、校正与参考三者对照'],
    ['储罐监控', '液位变化与热异常证据', '多通道图说明为何需要融合'],
], [32,64,70]))
add('亮点二：每一步都说明输入、处理、输出', 'h2')
add('流程不只是“采集、训练、预测”的通用箭头。每一步用小型结构图呈现输入、处理和输出，并附预期效果与常见问题。例如腐蚀评估需要先将多源信息对齐到管段，再形成风险分区；集输优化需要同时检查输量和压力，而不能把最低能耗直接当成可执行方案。')
add('亮点三：用一致组件降低跨案例学习成本', 'h2')
add('背景图示由 conceptVisual 渲染，步骤图由 stepVisual 渲染；案例清单保存语义内容，主站负责呈现。新增可视化字段是可选项，教师原样例仍可沿用基础结构。这种复用不只便于维护，也让读者在切换案例时沿用同一种阅读方式。')

section('七  第五次作业：把计算结果变成可探索的判断', '可视化重点：参数输入、过程解释、结果图形和边界提示相互对应。')
story.append(shot('petro-network.png', (150, 442, 1289, 926), 77*mm))
add('图 7  第五次作业存档截图局部：集输网络连接设备结构、当前推荐动作与约束状态。', 'caption')
add('时序曲线：同时表达变化、阈值与事件位置', 'h2')
add('泄漏与储罐案例使用 SVG 折线、阈值线和事件线，让读者定位异常发生前后，而不只是读取报警状态。计量案例将原始读数、校正读数、参考真值并列为三条线，配合误差指标观察系统偏差是否减弱。线图表达变化形状，指标卡补充精确值，两者承担不同职责。')
add('风险矩阵：颜色定位重点，数值保留解释', 'h2')
add('腐蚀案例使用 HTML/CSS 网格呈现 32 个单元，颜色深浅由教学风险分数驱动；单元内显示百分比，悬停可查看壁厚损失与风险。它不是地理地图，也不是 SVG 图；位置主要承担分区浏览作用。页面注明风险分数不能替代剩余强度规范评价，避免把视觉上的“危险色”当成工程结论。')
add('网络图与控制开关：看到优化方案如何落到设备', 'h2')
add('集输案例通过 SVG 节点和连线表示井组、汇管与泵站，在对应位置标出阀位、泵速、流量和压力。改变目标输量或压力限制后，候选方案重新计算；约束开关使读者比较“能耗低”和“可执行”的区别。其他案例的关闭校正、减少特征或屏蔽通道，同样用于观察方法是否影响最终展示结果。')
add('需要如实说明的实现边界', 'h2')
add('本作业使用固定种子合成数据、显式公式、简化风险评分与枚举优化，没有训练机器学习或深度学习模型。计量页虽出现“训练域”字样，实际是手工设定的教学适用范围；报告不把它当成训练覆盖证据。泄漏与储罐图将不同单位的量共用纵轴也是现有不足，后续应改为共享时间轴的分面图。')
add('我的收获：领域可视化要把“对象在哪里、方法做什么、结果意味着什么”连起来，同时让简化假设和不能据此作出的判断保持可见。', 'note')

section('八  横向总结、学习收获与课程建议', '我更看重可解释的映射与一致的数据口径，而不是图形种类或页面装饰的数量。')
story.append(tbl([
    ['跨作业积累', '具体实现', '对理解的作用'],
    ['空间与位置', '布局重排、共同坐标、网络拓扑', '表达层级、大小和对象关系'],
    ['对照与控制变量', 'A/B 快照、固定数据切换基线/色带', '让变化的来源更明确'],
    ['可追溯的数据流', '统一计算对象、处理历史、聚合导出', '减少图表与数字互相矛盾'],
    ['细节按需展开', '悬停数值、步骤解释、字段概况', '兼顾总览与局部检查'],
    ['边界和诚实表达', '预测标记、样本限制、教学说明', '防止图形造成过度推断'],
], [39,67,60]))
add('1. 我的主要收获：把“为什么这样画”放到实现之前', 'h2')
add('第一次作业让我意识到层级和分组本身就在表达信息；第二、三次使我开始关心共同尺度和数据联动；第四次让我反过来检查图形是否会误导；第五次则要求把这些原则放到陌生专业中使用。对我而言，最大的变化是从选择图表组件，转向先判断读者需要比较、定位、解释还是探索。')
add('2. 当前作品仍有改进空间', 'h2')
add('交互可以帮助理解，但本次没有开展用户测试，因此不能量化学习效率的提升。FrameFlow 的类别和散点显示限制需要读者注意，类别过多时还可增加搜索与分页；第四次的灰度预览不能覆盖真实色觉差异；第五次应进一步拆分异量纲曲线，并统一“教学适用范围”等措辞。指出这些限制，也是对可视化诚实性的要求。')
add('3. 对课程的建议：增加“同数据，不同编码”的练习', 'h2')
add('建议给出一份固定数据，让学生分别改变坐标基线、色带、分箱数和时间粒度，解释哪些变化来自数据，哪些来自呈现方式。评分不仅看最终图形，还看单位、图例、统计口径和比较条件是否一致。这能让学生从会调用图表库，走向理解图表设计的后果。')
add('4. 对作业验收的建议：让交互解释成为必答内容', 'h2')
add('答辩可以要求展示一次参数变化、一次数据筛选及一次无效输入，说明从控件到计算再到图形的过程；同时标明合成数据、绘图截取和未验证结论。还可增加同学互测：让第一次打开网站的人完成一个明确任务，记录误读位置，再修改标签、尺度或布局。这样能把实现正确与沟通有效结合起来。')

section('附录  实现依据与图示说明', '本报告根据五次作业的当前本地文件整理；索引用于核对实现，不代替运行验收。')
add('A. 五次作业的源码位置', 'h2')
add('统一根目录：D:/可视化作业。以下路径均相对于该目录。正文着重说明已检查的实现机制，不把历史验收说明或截图自动视为本轮运行结果。', 'flat')
story.append(tbl([
    ['作业 / 本文位置', '主要文件与核对内容'],
    ['第一次 / 第二节', '第一次/2_website_source_code/index.html<br/>demoConfig、ensureDemoMounted、applyVirtualViewport：变量、输入校验、srcdoc 与虚拟视口。'],
    ['第二次 / 第三节', '第二次/ai-productivity/dist/model.js 与 dist/app.js<br/>simulate、comparePlans：四阶段耗时、参数快照、共同条形尺度与导出。'],
    ['第三次 / 第四节', '第3次/frameflow/src/App.tsx、src/Charts.tsx 与 src/engine.ts<br/>replay、DataChart、onSelect：处理历史、图表筛选、分箱与绘图限制。'],
    ['第四次 / 第五节', '第四次/vis-learning/site/labs.js、site/core.js 与 site/course.json<br/>基线映射、颜色矩阵、56 天序列与聚合；章节结构和课程来源。'],
    ['第五次 / 第六、七节', '第5次/petro-ai-atlas/case-src/shared/demo.js、各案例 case.json，以及主站可视化渲染实现<br/>时序图、风险网格、网络优化、图示字段与步骤输入输出。'],
], [38,128]))
add('B. 图片来源与原创边界', 'h2')
add('图 1、4、5、6 为根据已核对源码制作的报告重绘图，不冒充网站截图。图 5 使用与第四次作业相同的确定性教学序列公式，并按每七天取均值；没有引用新的外部数据。图 1 的卡片是布局关系示意，不表示实际页面的精确断点。', 'flat')
add('图 2 来自第二次作业 docs/screenshots/05-lab.png；图 3 来自第三次作业 docs/evidence/simple-desktop.png；图 7 来自第五次作业 output/media/screenshots/t3-demo.png。均为存档截图的局部裁切，未改写其中的指标。', 'flat')
add('第四次作业原课程来源为中国石油大学（华东）李昕《可视化导论》；原课程材料及原有演示保留来源。报告所总结的个人实现重点为学习工作台的组织方式与新增三项交互实验，不将原课程 27 个小节全部宣称为个人原创。', 'flat')
add('C. 本报告的证据边界', 'h2')
add('源码核对支持对设计和实现机制的说明；存档截图支持对当时页面呈现的描述。它们不构成本轮对五个历史网站的完整浏览器验收，更不构成真实用户学习效果或油田模型性能的独立评估。第五次教学模拟的数值不能用于生产、安全或维修决策。', 'flat')


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(22*mm, 14*mm, 188*mm, 14*mm)
    canvas.setFont('CN', 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(22*mm, 9*mm, '舒鼎立  2407040125  |  五次作业的可视化实现与学习总结')
    canvas.drawRightString(188*mm, 9*mm, f'{doc.page:02d}')
    canvas.restoreState()


OUT.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(TARGET), pagesize=A4, leftMargin=22*mm, rightMargin=22*mm,
    topMargin=18*mm, bottomMargin=21*mm,
    title='可视化课程结课报告：五次作业的可视化实现与学习总结',
    author='舒鼎立', subject='五次课程作业的可视化设计、技术实现、效果与反思')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(TARGET)
