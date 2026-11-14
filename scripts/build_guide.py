"""Build the public HTML and PDF editions from the reviewed guide source."""
from pathlib import Path
import html
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak,
    Preformatted, KeepTogether,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[1]
TEXT = ROOT / 'guide' / 'guide-v2.txt'
PDF = ROOT / 'Sylnar_DMA_Firmware_Guide_v2.pdf'
HTML = ROOT / 'docs' / 'firmware-guide-v2.html'


def blocks(text):
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line or line.startswith('@'):
            continue
        if line.startswith('```'):
            code = []
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i])
                i += 1
            i += 1
            yield 'code', '\n'.join(code)
        elif line.startswith('# '):
            yield 'h1', line[2:]
        elif line.startswith('## '):
            yield 'h2', line[3:]
        elif line.startswith('- '):
            yield 'bullet', line[2:]
        else:
            yield 'p', line


def register_fonts():
    # Use installed fonts on Windows; standard PDF fonts are the portable fallback.
    win = Path('C:/Windows/Fonts')
    if (win / 'arial.ttf').exists():
        for name, filename in [('Body', 'arial.ttf'), ('BodyBold', 'arialbd.ttf'),
                               ('Mono', 'consola.ttf')]:
            pdfmetrics.registerFont(TTFont(name, str(win / filename)))
        return 'Body', 'BodyBold', 'Mono'
    return 'Helvetica', 'Helvetica-Bold', 'Courier'


class GuideDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in ('Chapter', 'Subheading'):
            if flowable.style.name == 'Chapter':
                label = flowable.getPlainText()
                key = 'chapter-' + str(self.seq.nextf('chapter'))
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(label, key, 0)
                self.notify('TOCEntry', (0, label, self.page, key))


def build_pdf(content, disclaimer):
    body, bold, mono = register_fonts()
    teal = colors.HexColor('#008c7c')
    ink = colors.HexColor('#152438')
    muted = colors.HexColor('#536579')
    styles = {
        'p': ParagraphStyle('BodyText', fontName=body, fontSize=10.3, leading=15.2,
                            textColor=ink, spaceAfter=9),
        'bullet': ParagraphStyle('Bullet', fontName=body, fontSize=10.1, leading=14.8,
                                 textColor=ink, leftIndent=13, firstLineIndent=-10, spaceAfter=5),
        'h1': ParagraphStyle('Chapter', fontName=bold, fontSize=19, leading=24,
                             textColor=ink, spaceBefore=22, spaceAfter=12, keepWithNext=True),
        'h2': ParagraphStyle('Subheading', fontName=bold, fontSize=11.8, leading=16,
                             textColor=teal, spaceBefore=12, spaceAfter=7, keepWithNext=True),
        'legal': ParagraphStyle('Legal', fontName=body, fontSize=9.6, leading=13.9,
                                textColor=ink, spaceAfter=7),
        'reference': ParagraphStyle('Reference', fontName=body, fontSize=8.8, leading=12,
                                    textColor=ink, spaceAfter=7),
    }
    doc = GuideDoc(str(PDF), pagesize=A4, leftMargin=51, rightMargin=51,
                   topMargin=59, bottomMargin=53, title='PCIe DMA Firmware Engineering - Version 2.0',
                   author='Sylnar', subject='Public engineering reference',
                   allowSplitting=True)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal',
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    def page(canvas, _doc):
        w, h = A4
        if doc.page > 1:
            canvas.setStrokeColor(colors.HexColor('#d7e3e8'))
            canvas.setLineWidth(.6)
            canvas.line(51, h-36, w-51, h-36)
            canvas.setFont(bold, 8)
            canvas.setFillColor(teal)
            canvas.drawString(51, h-27, 'SYLNAR / ENGINEERING REFERENCE')
            canvas.setFillColor(muted)
            canvas.setFont(body, 8)
            canvas.drawRightString(w-51, h-27, 'VERSION 2.0')
        canvas.setFont(body, 8)
        canvas.setFillColor(muted)
        canvas.drawString(51, 30, 'PUBLIC EDITION  |  14 NOVEMBER 2026')
        canvas.drawRightString(w-51, 30, str(doc.page))

    doc.addPageTemplates(PageTemplate(id='normal', frames=frame, onPage=page))
    title = ParagraphStyle('Title', fontName=bold, fontSize=37, leading=43, textColor=ink, spaceAfter=20)
    deck = ParagraphStyle('Deck', fontName=body, fontSize=15, leading=23, textColor=muted)
    kicker = ParagraphStyle('Kicker', fontName=bold, fontSize=11, leading=15, textColor=teal, spaceAfter=17)
    story = [Spacer(1, 79), Paragraph('SYLNAR / COMMUNITY GUIDE', kicker),
             Paragraph('PCIe DMA<br/>Firmware<br/>Engineering', title),
             Paragraph('Version 2.0', kicker),
             Paragraph('Build deliberately. Verify behavior.<br/>Keep the evidence.', deck),
             Spacer(1, 25), Paragraph('A public reference for Artix-7 endpoint development, host integration, '
             'DMA correctness, HDL quality, reproducible builds and hardware validation.', styles['p']),
             Spacer(1, 30), Paragraph('Revised 14 November 2026<br/>Published by Sylnar for the community.', styles['p']),
             PageBreak(), Paragraph('Original disclaimer', styles['h1']),
             Paragraph('The version 1 disclaimer is retained below without changing its wording.', styles['p'])]
    # Preserve the source wording; PDF line wrapping is necessarily different.
    legal_text = ' '.join(disclaimer.split())
    story.extend([Paragraph(html.escape(legal_text), styles['legal']), PageBreak(),
                  Paragraph('Contents', styles['h1'])])
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle('TOC', fontName=body, fontSize=9.8, leading=14,
                                      textColor=ink, leftIndent=0, firstLineIndent=0, spaceBefore=1)]
    story.extend([toc, PageBreak()])
    code_style = ParagraphStyle('Code', fontName=mono, fontSize=7.8, leading=11.2,
                               backColor=colors.HexColor('#f0f5f7'), borderPadding=9,
                               textColor=ink, spaceBefore=6, spaceAfter=12)
    for kind, value in content:
        if kind == 'code':
            story.append(Preformatted(value, code_style, maxLineLength=98))
        elif kind == 'bullet':
            story.append(Paragraph('- ' + html.escape(value), styles[kind]))
        else:
            # Make public reference URLs clickable, with wrapping around path separators.
            escaped = html.escape(value)
            if kind == 'p':
                escaped = re.sub(r'https://[^\s]+', lambda m: '<link href="' + m.group(0) + '">' +
                                 m.group(0).replace('/', '/\u200b').replace('-', '-\u200b') + '</link>', escaped)
            selected_style = styles['reference'] if kind == 'p' and value.startswith('[R') else styles[kind]
            story.append(Paragraph(escaped, selected_style))
    doc.multiBuild(story)


def build_html(content, disclaimer):
    toc = []
    article = []
    idx = 0
    in_list = False
    for kind, value in content:
        if kind != 'bullet' and in_list:
            article.append('</ul>')
            in_list = False
        safe = html.escape(value)
        if kind == 'h1':
            idx += 1
            anchor = 'chapter-' + str(idx)
            toc.append(f'<a href="#{anchor}">{safe}</a>')
            article.append(f'<h2 id="{anchor}">{safe}</h2>')
        elif kind == 'h2':
            article.append(f'<h3>{safe}</h3>')
        elif kind == 'code':
            article.append(f'<pre><code>{safe}</code></pre>')
        elif kind == 'bullet':
            if not in_list:
                article.append('<ul>')
                in_list = True
            article.append(f'<li>{safe}</li>')
        else:
            safe = re.sub(r'https://[^\s]+', lambda m: f'<a href="{m.group(0)}">{m.group(0)}</a>', safe)
            article.append(f'<p>{safe}</p>')
    if in_list:
        article.append('</ul>')
    css = '''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f4f7f9;color:#192b3d;font:17px/1.75 system-ui,sans-serif}header,main,footer{max-width:940px;margin:auto;padding:36px 34px}header{padding-top:65px;border-top:4px solid #008c7c}h1{font-size:48px;line-height:1.1;letter-spacing:-2px;margin:14px 0 20px}h2{font-size:29px;line-height:1.3;border-top:1px solid #cddce2;padding-top:30px;margin-top:48px;scroll-margin-top:25px}h3{font-size:20px;color:#007767;margin-top:28px}p{margin:0 0 17px}a{color:#007767;overflow-wrap:anywhere}.eyebrow{font:700 12px monospace;letter-spacing:2px;color:#007767}.deck{font-size:22px;color:#536579}.actions{display:flex;gap:18px;flex-wrap:wrap;margin-top:25px}.button{background:#007e70;color:white;padding:10px 17px;text-decoration:none;border-radius:5px}.contents{background:white;border:1px solid #d3e0e6;padding:22px;border-radius:7px}.contents a{display:block;padding:3px 0;text-decoration:none}pre{padding:17px;background:#e6eef2;border-radius:5px;overflow-x:auto;font:13px/1.6 Consolas,monospace}li{padding-bottom:5px}.legal{font-size:14px;white-space:pre-wrap;color:#536579}footer{font-size:13px;color:#536579;border-top:1px solid #cddce2}@media print{body{background:white;font-size:10pt;line-height:1.5}header,main,footer{padding:0;max-width:none}.actions{display:none}h2,h3{break-after:avoid}pre{white-space:pre-wrap}a{color:inherit}.contents{break-after:page}header{break-after:page}}'''
    output = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PCIe DMA Firmware Engineering | Version 2 | Sylnar</title><meta name="description" content="Public engineering reference for Artix-7 PCIe endpoints, DMA correctness, build validation and firmware troubleshooting."><style>' + css + '</style></head><body>'
    output += '<header><div class="eyebrow">SYLNAR / COMMUNITY ENGINEERING GUIDE</div><h1>PCIe DMA Firmware Engineering</h1><p class="deck">Version 2.0 - Build deliberately. Verify behavior. Keep the evidence.</p><p>Revised 14 November 2026. A public engineering reference.</p><div class="actions"><a class="button" href="../Sylnar_DMA_Firmware_Guide_v2.pdf">Download PDF</a><a href="index.html">Guide collection</a></div></header><main><nav class="contents" aria-label="Contents"><strong>Contents</strong>'
    output += ''.join(toc) + '</nav>' + ''.join(article)
    output += '<h2>Original disclaimer</h2><p>The version 1 disclaimer is retained below without changing its wording.</p><div class="legal">' + html.escape(disclaimer) + '</div></main><footer>Sylnar / Public engineering reference / Version 2.0</footer></body></html>'
    HTML.write_text(output, encoding='utf-8')


if __name__ == '__main__':
    content = list(blocks(TEXT.read_text(encoding='utf-8')))
    disclaimer = (ROOT / 'guide' / 'disclaimer.txt').read_text(encoding='utf-8')
    build_html(content, disclaimer)
    build_pdf(content, disclaimer)
    print('Built', PDF.name, 'and', HTML.relative_to(ROOT))
