from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)
TARGET = OUT / "石油勘探开发智能化可能性地图结课报告.pdf"
IMG = ROOT / "output" / "media" / "screenshots"

font_path = Path("C:/Windows/Fonts/msyh.ttc")
font_bold_path = Path("C:/Windows/Fonts/msyhbd.ttc")
pdfmetrics.registerFont(TTFont("YaHei", str(font_path), subfontIndex=0))
pdfmetrics.registerFont(TTFont("YaHeiB", str(font_bold_path), subfontIndex=0))

JADE = colors.HexColor("#286F62")
INK = colors.HexColor("#23302F")
MUTED = colors.HexColor("#687270")
PALE = colors.HexColor("#EAF3F0")
LINE = colors.HexColor("#D9E1DE")
CLAY = colors.HexColor("#A6614F")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CNTitle", fontName="YaHeiB", fontSize=25, leading=34, textColor=INK, alignment=TA_CENTER, spaceAfter=16))
styles.add(ParagraphStyle(name="CNSub", fontName="YaHei", fontSize=11, leading=18, textColor=MUTED, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="CNH1", fontName="YaHeiB", fontSize=17, leading=23, textColor=INK, spaceBefore=3, spaceAfter=9))
styles.add(ParagraphStyle(name="CNH2", fontName="YaHeiB", fontSize=12.5, leading=18, textColor=JADE, spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle(name="CNBody", fontName="YaHei", fontSize=10.5, leading=18, textColor=INK, alignment=TA_LEFT, firstLineIndent=21, spaceAfter=7))
styles.add(ParagraphStyle(name="CNNoIndent", fontName="YaHei", fontSize=10, leading=17, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="CNSmall", fontName="YaHei", fontSize=8.5, leading=13, textColor=MUTED, alignment=TA_CENTER, spaceAfter=8))
styles.add(ParagraphStyle(name="CNQuote", fontName="YaHei", fontSize=10, leading=17, textColor=INK, backColor=PALE, borderColor=JADE, borderWidth=0.7, borderPadding=9, spaceBefore=5, spaceAfter=10))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(22 * mm, 14 * mm, 188 * mm, 14 * mm)
    canvas.setFont("YaHei", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(22 * mm, 9 * mm, "舒鼎立  2407040125  石油勘探开发智能化可能性地图")
    canvas.drawRightString(188 * mm, 9 * mm, f"第 {doc.page} 页")
    canvas.restoreState()


def p(text, style="CNBody"):
    return Paragraph(text, styles[style])


def table(data, widths):
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "YaHeiB"),
        ("FONTNAME", (0, 1), (-1, -1), "YaHei"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("LEADING", (0, 0), (-1, -1), 13),
        ("BACKGROUND", (0, 0), (-1, 0), JADE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("TEXTCOLOR", (0, 1), (-1, -1), INK),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9F8")]),
    ]))
    return t


story = []
story.append(Spacer(1, 32 * mm))
story.append(p("课程大作业结课报告", "CNSub"))
story.append(Spacer(1, 8 * mm))
story.append(p("石油勘探开发智能化可能性地图", "CNTitle"))
story.append(Spacer(1, 10 * mm))
cover = Table([
    [Paragraph("项目类别", styles["CNNoIndent"]), Paragraph("第 12 类 运输", styles["CNNoIndent"])],
    [Paragraph("姓名", styles["CNNoIndent"]), Paragraph("舒鼎立", styles["CNNoIndent"])],
    [Paragraph("学号", styles["CNNoIndent"]), Paragraph("2407040125", styles["CNNoIndent"])],
    [Paragraph("完成案例", styles["CNNoIndent"]), Paragraph("5 个运输环节智能化案例", styles["CNNoIndent"])],
    [Paragraph("完成日期", styles["CNNoIndent"]), Paragraph("2026 年 11 月 5 日", styles["CNNoIndent"])],
], colWidths=[38 * mm, 92 * mm], hAlign="CENTER")
cover.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "YaHei"),
    ("GRID", (0, 0), (-1, -1), 0.45, LINE),
    ("BACKGROUND", (0, 0), (0, -1), PALE),
    ("TEXTCOLOR", (0, 0), (0, -1), JADE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
]))
story.append(cover)
story.append(Spacer(1, 24 * mm))
story.append(p("本报告记录网站的可视化设计、五个案例的技术实现、当前验证证据和我对课程的建议。演示数据为固定种子的教学合成数据，报告不把演示指标解释为真实油田或管网绩效。", "CNQuote"))
story.append(PageBreak())

story.append(p("一 我对可视化的理解", "CNH1"))
story.append(p("可视化的价值不是给页面增加装饰，而是把数据、计算和决策之间的关系变成读者可以检查的证据。对于石油勘探开发这样的专业领域，读者通常先缺少对象和机理知识。如果页面直接给出模型名称、准确率或红色报警，读者很难判断模型是否读取了正确的数据，也不能理解输出为什么影响生产决策。因此，我把可视化分为概念理解、流程理解和结果验证三个层次。"))
story.append(p("概念理解解决“场景中发生了什么”。例如管道泄漏案例先显示入口流量、管存补偿、出口流量和质量平衡残差的关系；集输优化案例先显示井组、汇管、阀门和泵站的网络结构。图形使非石油专业读者在接触算法前先获得最小必要背景。"))
story.append(p("流程理解解决“模型怎样工作”。我没有只画一条抽象流程箭头，而是为每一步固定显示输入、处理和输出。例如腐蚀评估从多源台账开始，经过里程对齐和特征构造，输出管段风险，再进入工程师复检。这个结构能暴露常见断点：坐标是否对齐、缺测值怎样处理、风险是否进入可执行工单。"))
story.append(p("结果验证解决“这个结论是否由当前数据算出来”。五个交互演示都把参数控制、计算指标和图表放在同一屏幕。读者调整泄漏率、含气率或压力上限后，图表与指标立即重算。页面同时提供负向控制，例如关闭计量校正或屏蔽储罐热成像通道，以检查关键模块是否真实影响结果。"))
story.append(p("我认为好的可视化还必须诚实呈现边界。合成数据可以演示计算关系，却不能证明现场误报率、节能收益或计量精度。因此每个演示都标注“固定种子 教学合成数据 浏览器本地计算”和“非现场性能结论”。可视化不仅要让结果容易理解，也要让不确定性和未验证项容易看见。"))
img = Image(str(IMG / "home.png"), width=166 * mm, height=115 * mm)
story.append(img)
story.append(p("图 1  门户把 13 个环节和 61 个候选场景放在统一作业链中", "CNSmall"))
story.append(PageBreak())

story.append(p("二 大作业中使用的可视化技术", "CNH1"))
story.append(p("网站采用原生 HTML CSS JavaScript 实现，不依赖后端、数据库或在线模型服务。这样既满足纯前端要求，也允许直接打开 index.html 或部署到静态托管平台。主站负责导航、案例注册和标签页渲染，案例演示在 sandbox iframe 中执行，避免案例脚本污染主站。"))
story.append(p("背景部分使用六类声明式图形：流程图表示守恒或决策链，分层图表示油气水相和管壁层次，对比图区分随机噪声与系统偏差，融合图表示多传感器证据，网络图表示井组到泵站的拓扑，边界图明确已验证、未验证和待补充内容。这些图形由统一组件生成，案例清单只写语义数据，因此五个案例保持相同阅读方式。"))
story.append(p("流程部分为每一步生成输入、处理和输出图。文字同时说明预期效果和常见坑。读者能看到“有组件”与“进入决策链”的区别。例如集输优化不是只计算最低能耗，而是把产量和压力作为硬约束；关闭约束后，页面明确标记推荐方案不可执行。"))
story.append(p("演示部分使用 SVG 绘制时序曲线、风险矩阵和管网图。所有指标由当前控件状态和固定种子数据实时计算。固定种子保证答辩时结果可重复，参数交互则保证页面不是播放预先录好的答案。"))
story.append(table([
    ["案例", "主要图形", "计算结果", "负向控制"],
    ["管道泄漏", "三条时序曲线 阈值线 事件线", "报警 延迟 事前越阈点 残差", "泄漏调为零"],
    ["管道腐蚀", "32 单元风险矩阵", "高风险数 最高风险 剩余壁厚代理", "仅使用壁厚"],
    ["集输优化", "井组汇管泵站网络图", "泵速 阀位 能耗 可执行性", "关闭工艺约束"],
    ["计量校正", "原始 校正 真值对比曲线", "原始 MAPE 校正 MAPE 适用域", "关闭智能校正"],
    ["储罐监控", "液位与融合分数曲线", "报警 延迟 液位变化 通道状态", "屏蔽热成像"]
], [31 * mm, 44 * mm, 57 * mm, 34 * mm]))
story.append(Spacer(1, 5 * mm))
story.append(Image(str(IMG / "t3-demo.png"), width=166 * mm, height=115 * mm))
story.append(p("图 2  集输优化把控制参数 推荐动作 网络结构和约束状态放在同一视图", "CNSmall"))
story.append(PageBreak())

story.append(p("三 五个运输案例的实现效果", "CNH1"))
story.append(p("管道泄漏案例把入口和出口流量转换为质量平衡残差，再用健康窗口的均值和标准差计算异常分数。默认泄漏为 6 立方米每小时，页面给出已检测和零分钟延迟；把泄漏率调为零后，结果变为未报警，残差均值回到零。这说明报警由泄漏输入和残差计算共同产生。"))
story.append(p("管道腐蚀案例把壁厚损失、环境湿度和服役年限融合为管段风险。默认多源模型的最高风险为 62%，切换为仅壁厚后最高风险变为 27%。这个反事实说明环境和年限特征被模型真实读取。风险图只用于复检排序，页面明确提示它不能替代剩余强度规范评价。"))
story.append(p("集输优化案例枚举泵速和阀位组合，计算输量、压力和能耗。启用约束时，默认方案为 80% 泵速、100% 阀位、29.7 千瓦时，并满足约束；关闭约束后，算法选择 72% 泵速和 21.6 千瓦时，但页面标记方案不可执行。这个结果说明更低的目标值不等于可用方案。"))
story.append(p("油气计量案例模拟含气率、温度和仪表漂移造成的系统偏差。默认校正将 MAPE 从 8.04% 降到 0.50%；关闭校正后，校正后 MAPE 回到 8.04%，误差改善为零。含气率超过训练覆盖时，页面保留数值但显示域外警告，避免静默外推。"))
story.append(p("储罐监控案例融合液位质量平衡残差和热异常。默认两个通道共同产生已检测结果；屏蔽热成像后变为未报警。这个设计既展示多模态融合的价值，也暴露单一液位通道在当前信噪比下的检测边界。"))
story.append(p("以上数值是当前固定种子教学数据的浏览器运行结果，只证明交互计算和反事实因果链按设计工作。它们不是现场绩效，也不能用于安全、维修或生产决策。" , "CNQuote"))
story.append(p("四 工程实现与验证", "CNH1"))
story.append(p("五个案例采用单一源构建。每个 case.json 定义场景、方法、专业背景、案例流程和演示入口；构建脚本把同一份内容同时生成站内注册文件和独立 ZIP。这样可以避免站内版本与提交压缩包内容不同。"))
story.append(p("主站继续支持原有添加案例功能。新的 visual 字段是可选字段，旧案例不填写时仍按原方式显示。上传清单中的正文 HTML 经过允许列表清洗，脚本只在 sandbox iframe 中执行。"))
story.append(p("当前静态校验覆盖五个场景绑定、清单结构、四段背景、四步流程、可视化字段、演示文件、五个 ZIP 以及框架组件。真实浏览器验收确认五个场景都能显示教学数据说明、实验控制、指标和解释区。五组负向控制均改变了相关业务结果。"))
story.append(PageBreak())

story.append(p("五 学习收获和课程建议", "CNH1"))
story.append(p("这次作业让我认识到，可视化和模型开发不能分开。一个模型即使能输出数值，如果页面没有说明输入、过程、单位和适用边界，读者仍然无法判断结果是否可信。相反，守恒关系、约束状态和反事实开关可以让模型的作用变得可检查。"))
story.append(p("我也更加重视负向测试。最初的集输演示虽然提供了“关闭约束”开关，但默认参数下前后推荐没有变化；储罐演示则因事件索引和阈值设置错误，把正常检测显示为提前误报。只有实际切换控件并比较最终指标，才发现这些问题。修复后，关闭集输约束会得到不可执行方案，储罐默认结果也恢复为已检测。"))
story.append(p("课程可以增加一次关于“误导性可视化”的专题练习。学生不仅要画出图，还要解释坐标范围、统计口径、采样偏差和不确定性。可以提供同一组数据的多个图形，让学生判断哪些设计会夸大效果。"))
story.append(p("课程还可以要求每个作品提交一组负向控制。对于分类模型，可以删除关键特征；对于优化模型，可以关闭约束；对于多模态模型，可以屏蔽一个通道。评分时检查最终结果是否按预期变化。这样能区分真正接入的模块和只出现在界面或说明中的模块。"))
story.append(p("最后，建议在作业中给出一个最小的案例包自动校验器。它可以检查目录、清单、场景编号、演示入口和文件大小。学生仍然负责内容和可视化设计，但能在提交前发现格式错误，减少课堂答辩时间消耗在路径和压缩包问题上。"))

story.append(p("参考资料", "CNH2"))
refs = [
    "1. PHMSA. Leak Detection Systems Fact Sheet. https://primis.phmsa.dot.gov/stakeholder-comms/factsheets/fsleakdetectionsystems/",
    "2. PHMSA. Final Report on Pipeline Corrosion. https://www.phmsa.dot.gov/sites/phmsa.dot.gov/files/docs/technical-resources/pipeline/gas-distribution-integrity-management/65996/finalreportpipelinecorrosion.pdf",
    "3. U.S. Department of Energy. Improving Pumping System Performance. https://www1.eere.energy.gov/manufacturing/tech_assistance/pdfs/pump.pdf",
    "4. Measurement. Deep learning based multiphase flow metering study. https://doi.org/10.1016/j.measurement.2022.112254",
    "5. Journal of Physics Conference Series. Storage tank liquid level anomaly detection. https://doi.org/10.1088/1742-6596/2224/1/012013"
]
for ref in refs:
    story.append(p(ref, "CNNoIndent"))

doc = SimpleDocTemplate(str(TARGET), pagesize=A4, rightMargin=22 * mm, leftMargin=22 * mm, topMargin=18 * mm, bottomMargin=19 * mm, title="石油勘探开发智能化可能性地图结课报告", author="舒鼎立")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(TARGET)
