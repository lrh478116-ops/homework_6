from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / ".build" / "video"
OUT = ROOT / "output" / "video"
sys.path.insert(0, str(ROOT / ".build" / "python-packages"))
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
segments = []
for slide in sorted(WORK.glob("slide-*.png")):
    idx = slide.stem.split("-")[-1]
    audio = WORK / f"audio-{idx}.wav"
    if not audio.exists():
        raise FileNotFoundError(audio)
    segment = WORK / f"segment-{idx}.mp4"
    cmd = [
        ffmpeg, "-y", "-loop", "1", "-framerate", "30", "-i", str(slide), "-i", str(audio),
        "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-shortest", "-movflags", "+faststart", str(segment)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    segments.append(segment)

concat = WORK / "concat.txt"
concat.write_text("\n".join("file '" + str(p).replace("'", "'\\''") + "'" for p in segments), encoding="utf-8")
target = OUT / "网站关键亮点讲解视频.mp4"
subprocess.run([ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", "-movflags", "+faststart", str(target)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

probe = subprocess.run([ffmpeg, "-i", str(target)], text=True, encoding="utf-8", errors="ignore", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
duration = "unknown"
for line in probe.stderr.splitlines():
    if "Duration:" in line:
        duration = line.strip().split("Duration:", 1)[1].split(",", 1)[0].strip()
        break
print(f"{target}\nDuration {duration}")
