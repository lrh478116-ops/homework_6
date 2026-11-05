"""Structural PDF checks, not a substitute for source review or visual QA.

Run: python tests/validate_report.py [path-to-pdf]
Requires pypdf and pdfplumber. The optional input supports negative controls.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pdfplumber
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'output/pdf/石油勘探开发智能化可能性地图结课报告.pdf'
reader = PdfReader(target)
assert len(reader.pages) == 10, f'Expected 10 pages, got {len(reader.pages)}'
texts = [page.extract_text() for page in reader.pages]
titles = [
    '五次作业的可视化实现', '我对可视化的理解', '第一次作业：把布局规则',
    '第二次作业：把AI收益', '第三次作业：让图表', '第四次作业：用实验',
    '第五次作业：让专业背景', '第五次作业：把计算结果', '横向总结、学习收获与课程建议',
    '实现依据与图示说明',
]
for i, (text, title) in enumerate(zip(texts, titles), 1):
    compact = ''.join(text.split())
    assert title in compact, f'Missing intended heading on page {i}: {title}'
    assert '舒鼎立' in compact and '2407040125' in compact, f'Identity missing on page {i}'
    assert len(compact) > 200, f'Unexpected near-empty page {i}'
    assert '\ufffd' not in text and '\x00' not in text, f'Invalid extracted glyph on page {i}'

alltext = ''.join(''.join(t.split()) for t in texts)
for required in ['课程建议', 'iframe.srcdoc', 'simulate', 'replay', 'conceptVisual',
                 'CSS网格', '没有训练机器学习或深度学习模型', '灰度预览', '源码位置']:
    assert required in alltext, f'Missing report requirement: {required}'
assert reader.metadata.author == '舒鼎立'
assert not reader.is_encrypted
with pdfplumber.open(target) as pdf:
    for i, page in enumerate(pdf.pages, 1):
        for line in page.extract_text_lines():
            assert line['text'].lstrip()[0] not in '，；：？！）》”’。', f'Forbidden line-start punctuation p{i}: {line["text"]}'
        for char in page.chars:
            assert 35 <= char['x0'] <= char['x1'] <= page.width - 25, f'Horizontal overflow p{i}'
            assert 20 <= char['top'] <= char['bottom'] <= page.height - 12, f'Vertical overflow p{i}'

result = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'scope': 'PDF structure/text/bounds only; visual and source review recorded separately',
    'pdf_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
    'authoring_script_sha256': hashlib.sha256((ROOT / 'tools/create_report.py').read_bytes()).hexdigest(),
    'page_count': len(reader.pages),
    'page_text_characters': [len(t) for t in texts],
    'checks_executed': ['intended section per page', 'identity', 'nonempty pages', 'required concepts',
                        'extractable glyphs', 'metadata', 'encryption', 'all text within page bounds', 'Chinese line-start punctuation'],
}
print(json.dumps(result, ensure_ascii=True, indent=2))
