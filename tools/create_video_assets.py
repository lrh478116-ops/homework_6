from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "video"
WORK = ROOT / ".build" / "video"
SHOTS = ROOT / "output" / "media" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)
WORK.mkdir(parents=True, exist_ok=True)

W, H = 1280, 720
BG = "#F7F8F5"
INK = "#23302F"
MUTED = "#66716F"
JADE = "#286F62"
PALE = "#EAF3F0"
CLAY = "#A6614F"
FONT = "C:/Windows/Fonts/msyh.ttc"
BOLD = "C:/Windows/Fonts/msyhbd.ttc"


def f(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def fit_image(path, box, crop=False):
    im = Image.open(path).convert("RGB")
    if len(box) == 2:
        w, h = box
    else:
        _, _, w, h = box
    if crop:
        scale = max(w / im.width, h / im.height)
    else:
        scale = min(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    if crop:
        left = max(0, (im.width - w) // 2)
        top = max(0, (im.height - h) // 2)
        im = im.crop((left, top, left + w, top + h))
    canvas = Image.new("RGB", (w, h), "white")
    canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return canvas


def base(title, subtitle, no):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 8), fill=JADE)
    d.text((54, 32), title, font=f(34, True), fill=INK)
    d.text((56, 82), subtitle, font=f(18), fill=MUTED)
    d.rounded_rectangle((1155, 33, 1226, 73), radius=20, fill=PALE, outline=JADE, width=2)
    d.text((1174, 42), f"{no:02d}", font=f(18, True), fill=JADE)
    return im, d


def screenshot_slide(no, title, subtitle, shot, note):
    im, d = base(title, subtitle, no)
    panel = fit_image(SHOTS / shot, (1110, 515))
    im.paste(panel, (85, 130))
    d.rounded_rectangle((78, 123, 1202, 652), radius=9, outline="#CDD8D4", width=2)
    d.rectangle((85, 607, 1195, 645), fill=(247, 248, 245))
    d.text((103, 614), note, font=f(15), fill=JADE)
    return im


slides = []
narration = []

im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
d.rectangle((0, 0, W, 10), fill=JADE)
d.text((74, 75), "石油勘探开发的", font=f(28), fill=MUTED)
d.text((70, 125), "智能化可能性地图", font=f(58, True), fill=INK)
d.rectangle((72, 212, 235, 218), fill=CLAY)
d.text((75, 260), "运输环节 5 个智能化案例", font=f(29, True), fill=JADE)
d.text((75, 315), "舒鼎立  2407040125", font=f(23), fill=INK)
d.rounded_rectangle((75, 420, 1180, 565), radius=12, fill=PALE, outline="#A9C9C0", width=2)
d.text((105, 450), "纯前端 · 固定种子教学数据 · 三层可视化 · 可独立上传", font=f(25, True), fill=INK)
d.text((105, 505), "本视频只演示计算关系，不把合成数据指标当作现场绩效。", font=f(20), fill=MUTED)
slides.append(im)
narration.append("大家好，我是舒鼎立，学号二四零七零四零一二五。我的项目是石油勘探开发的智能化可能性地图。按照学号循环，我完成的是第十二类运输环节，共五个必做案例。整个网站采用纯前端实现，本视频展示主要设计和交互结果。")

slides.append(screenshot_slide(2, "门户总览", "保留完整作业链，在同一入口浏览案例", "home.png", "13 个环节 · 61 个候选场景 · 6 个已接入案例"))
narration.append("首页保留了原框架的十三个作业环节和六十一个候选场景，可以按作业链或智能方法查找。运输环节新增的五个案例都能从场景页进入。主页仍保留添加案例按钮，其他同学按原有清单和演示目录制作的案例可以继续上传。")

slides.append(screenshot_slide(3, "案例一 管道泄漏智能检测", "质量平衡残差与时序确认", "t1-demo.png", "把泄漏率调为零后，判定由已检测变为未报警"))
narration.append("管道泄漏案例先用入口流量减去出口流量和管存变化，得到可解释的质量平衡残差，再用健康窗口计算异常分数，并要求连续越过阈值。演示同时显示入口、出口、异常分数、阈值和事件起点。把泄漏率调为零后，报警消失，残差均值也回到零。")

slides.append(screenshot_slide(4, "案例二 管道腐蚀智能评估", "壁厚 环境 年限的多源风险分区", "t2-demo.png", "切换为仅壁厚后，最高风险从 62% 降到 27%"))
narration.append("管道腐蚀案例把三十二个检测单元画成风险矩阵。每个单元融合壁厚损失、环境湿度和服役年限，用于安排复检优先级。切换成仅使用壁厚后，最高风险从百分之六十二变成百分之二十七，说明多源特征确实进入了计算。页面也强调风险排序不能替代工程规范。")

slides.append(screenshot_slide(5, "案例三 集输系统工况优化", "泵速 阀位 能耗和硬约束共同决定推荐", "t3-demo.png", "关闭约束后能耗更低，但方案被明确标为不可执行"))
narration.append("集输优化案例用网络图显示井组、汇管和泵站。算法枚举泵速和阀位，同时检查目标输量和压力上限。启用约束时，推荐百分之八十泵速并满足边界；关闭约束后，能耗虽然降低，输量却不达标，所以页面明确标记为不可执行。这说明优化结果首先要满足工艺条件。")

im, d = base("案例四和案例五", "计量校正与储罐多模态监控", 6)
left = fit_image(SHOTS / "t4-demo.png", (535, 455), crop=True)
right = fit_image(SHOTS / "t5-demo.png", (535, 455), crop=True)
im.paste(left, (75, 145)); im.paste(right, (670, 145))
d.rounded_rectangle((68, 138, 617, 610), radius=8, outline="#CDD8D4", width=2)
d.rounded_rectangle((663, 138, 1212, 610), radius=8, outline="#CDD8D4", width=2)
d.text((85, 625), "计量：关闭校正后误差改善归零", font=f(16, True), fill=JADE)
d.text((680, 625), "储罐：屏蔽热通道后由已检测变为未报警", font=f(16, True), fill=JADE)
slides.append(im)
narration.append("油气计量案例用含气率、温度和仪表漂移估计系统偏差。默认校正把平均相对误差从百分之八点零四降到百分之零点五，关闭校正后改善归零。储罐案例融合液位质量平衡和热异常，屏蔽热成像通道后由已检测变成未报警，展示了多模态输入的真实作用和单通道边界。")

im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
d.rectangle((0, 0, W, 9), fill=JADE)
d.text((70, 55), "项目亮点与边界", font=f(40, True), fill=INK)
cards = [
    ("专业背景可视化", "流程 分层 融合 网络和边界图", 95, 150),
    ("流程逐步可视化", "每一步都有输入 处理 输出和常见坑", 655, 150),
    ("结果可反事实验证", "五组负向控制均改变相关业务结果", 95, 345),
    ("单一源构建", "同一份配置生成站内案例与独立 ZIP", 655, 345),
]
for title, body, x, y in cards:
    d.rounded_rectangle((x, y, x + 510, y + 150), radius=12, fill="white", outline="#C9D6D2", width=2)
    d.text((x + 25, y + 25), title, font=f(24, True), fill=JADE)
    d.text((x + 25, y + 78), body, font=f(18), fill=MUTED)
d.rounded_rectangle((95, 555, 1165, 640), radius=10, fill=PALE, outline=JADE, width=2)
d.text((125, 580), "证据边界：固定种子教学数据不能证明现场检测率 节能收益或计量精度", font=f(20, True), fill=INK)
slides.append(im)
narration.append("我认为项目做得比较好的地方有四点。第一，先解释石油机理，再解释模型。第二，专业背景、案例流程和计算结果都使用可视化。第三，五个演示都有负向控制，能检查模块是否真正影响结果。第四，案例包和站内版本由同一源构建。需要强调的是，所有结果都是教学合成数据，真实现场还需要历史事件、盲测、规范和联锁验证。谢谢老师。")

for i, slide in enumerate(slides, 1):
    slide.save(WORK / f"slide-{i:02d}.png", quality=95)

payload = [{"index": i + 1, "text": text} for i, text in enumerate(narration)]
(WORK / "narration.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
(OUT / "视频讲稿.txt").write_text("\n\n".join(f"第 {i+1} 段\n{text}" for i, text in enumerate(narration)), encoding="utf-8")
print(f"created {len(slides)} slides")
