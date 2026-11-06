"""Generate a one-page, anonymous A4 résumé template.

Run: python tools/create_resume_template.py
The output contains placeholders only; no student or personal identifiers.
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'output/pdf/简洁简历模板.pdf'
TARGET.parent.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont('ResumeCN', 'C:/Windows/Fonts/msyh.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('ResumeCNB', 'C:/Windows/Fonts/msyhbd.ttc', subfontIndex=0))
pdfmetrics.registerFontFamily('ResumeCN', normal='ResumeCN', bold='ResumeCNB')

INK = colors.HexColor('#253238')
ACCENT = colors.HexColor('#2D625C')
MUTED = colors.HexColor('#69767A')
RULE = colors.HexColor('#D6DEDF')
PALE = colors.HexColor('#F3F7F6')
W, H = A4
LEFT, RIGHT = 22 * mm, W - 22 * mm
CONTENT = RIGHT - LEFT

body = ParagraphStyle('body', fontName='ResumeCN', fontSize=9.3, leading=15.8, textColor=INK, wordWrap='CJK')
hint = ParagraphStyle('hint', parent=body, fontSize=8.4, leading=14.2, textColor=MUTED)
small = ParagraphStyle('small', parent=body, fontSize=8.2, leading=13.5)


def para(c, text, x, top, width=CONTENT, style=body):
    obj = Paragraph(text, style)
    _, height = obj.wrap(width, H)
    obj.drawOn(c, x, top - height)
    return top - height


def section(c, title, y):
    c.setFillColor(ACCENT)
    c.roundRect(LEFT, y - 5, 3, 14, 1.5, stroke=0, fill=1)
    c.setFont('ResumeCNB', 10.5)
    c.setFillColor(INK)
    c.drawString(LEFT + 11, y - 1, title)
    c.setStrokeColor(RULE)
    c.setLineWidth(.7)
    c.line(LEFT + 88, y - 3, RIGHT, y - 3)


def title_row(c, left, right, y):
    c.setFont('ResumeCNB', 9.3)
    c.setFillColor(INK)
    c.drawString(LEFT, y, left)
    c.setFont('ResumeCN', 8.4)
    c.setFillColor(MUTED)
    c.drawRightString(RIGHT, y, right)


def bullet(c, text, y):
    c.setFillColor(ACCENT)
    c.circle(LEFT + 3, y - 4, 1.6, stroke=0, fill=1)
    para(c, text, LEFT + 13, y, CONTENT - 13, small)


c = canvas.Canvas(str(TARGET), pagesize=A4)
c.setTitle('简洁单页简历模板')
c.setAuthor('Résumé Template')
c.setSubject('Anonymous one-page résumé template with placeholders only')

# Header: target direction and optional contact channels, with no real identity.
c.setFillColor(ACCENT)
c.rect(LEFT, H - 47, 23, 3, fill=1, stroke=0)
c.setFont('ResumeCN', 8.2)
c.setFillColor(MUTED)
c.drawString(LEFT, H - 62, '简历模板  /  RESUME')
c.setFont('ResumeCNB', 21)
c.setFillColor(INK)
c.drawString(LEFT, H - 95, '[目标岗位 / 研究方向]')
para(c, '邮箱：[填写]　　电话：[填写]　　城市：[可选]　　作品链接：[可选]', LEFT, H - 109, style=hint)
c.setStrokeColor(RULE)
c.setLineWidth(.8)
c.line(LEFT, H - 135, RIGHT, H - 135)

section(c, '个人概述', H - 159)
c.setFillColor(PALE)
c.roundRect(LEFT, H - 221, CONTENT, 49, 4, fill=1, stroke=0)
para(c, '[用 2-3 句话概括目标方向、核心能力，以及最能证明能力的项目或成果。<br/>避免空泛形容词，优先写可核验的事实。]', LEFT + 12, H - 183, CONTENT - 24, hint)

section(c, '教育背景', H - 242)
title_row(c, '[学校 / 学院]　[学位 / 专业]', '[起止年月]', H - 269)
para(c, '[研究方向、相关课程或毕业课题；保留与目标方向最相关的内容。]', LEFT, H - 280, style=hint)

section(c, '专业技能', H - 321)
para(c, '<b>技术工具</b>　[语言 / 框架 / 数据与可视化工具，按熟练程度排序]', LEFT, H - 342)
para(c, '<b>领域能力</b>　[算法、数据分析、系统设计或实验方法；写出具体能力]', LEFT, H - 362)

section(c, '代表项目 / 科研', H - 405)
title_row(c, '[项目名称一]　[职责 / 角色]', '[起止年月]', H - 432)
bullet(c, '<b>问题</b>：[具体场景、数据或用户需求，以及需要解决的核心问题。]', H - 442)
bullet(c, '<b>实现</b>：[采用的方法与个人负责部分；说明关键技术选择。]', H - 459)
bullet(c, '<b>结果</b>：[可核验的指标、交付物、链接或结论；注明评估口径。]', H - 476)

c.setStrokeColor(RULE)
c.line(LEFT, H - 501, RIGHT, H - 501)
title_row(c, '[项目名称二]　[职责 / 角色]', '[起止年月]', H - 520)
bullet(c, '<b>问题</b>：[一句话说明目标、约束与评价方式。]', H - 530)
bullet(c, '<b>实现</b>：[关键步骤、可视化/工程实现或方法改进。]', H - 547)
bullet(c, '<b>结果</b>：[量化结果或可展示成果；没有指标时说明实际产出。]', H - 564)

section(c, '实践经历', H - 609)
title_row(c, '[团队 / 组织]　[岗位或职责]', '[起止年月]', H - 636)
para(c, '[说明承担的任务、协作范围、使用的方法，以及最终完成的交付。]', LEFT, H - 647, style=hint)

section(c, '成果与补充', H - 693)
para(c, '<b>成果</b>　[论文 / 开源 / 比赛 / 证书，仅列与目标方向相关的内容]', LEFT, H - 715)
para(c, '<b>链接</b>　[作品集 / 代码仓库 / 论文页面，可选]', LEFT, H - 735)

c.setStrokeColor(RULE)
c.line(LEFT, 48, RIGHT, 48)
c.setFont('ResumeCN', 7.5)
c.setFillColor(MUTED)
c.drawString(LEFT, 34, '填写提示：用真实经历替换方括号内容；无关栏目可删除，尽量保持一页。')
c.drawRightString(RIGHT, 34, 'A4  ·  单栏')
c.showPage()
c.save()
print(TARGET)
