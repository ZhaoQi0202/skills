#!/usr/bin/env python3
import argparse
import html
import re
from pathlib import Path

URL_RE = re.compile(r'(https?://[^\s<>"]+)')
SECTION_RE = re.compile(r'^##\s+(.+?)\s*$')
TITLE_RE = re.compile(r'^#(?!#)\s+(.+?)\s*$')
BOLD_LINE_RE = re.compile(r'^\*\*(.+?)\*\*$')

TITLE_STYLE = 'margin:0 0 24px 0;font-size:28px;line-height:1.45;font-weight:700;color:#111;'
SECTION_STYLE = 'margin:32px 0 14px 0;font-size:20px;line-height:1.5;font-weight:700;color:#111;'
PARA_STYLE = 'margin:0 0 16px 0;font-size:16px;line-height:1.9;color:#222;'
LIST_STYLE = 'margin:0 0 12px 0;font-size:16px;line-height:1.9;color:#222;padding-left:1.2em;text-indent:-1.2em;'
LINK_FALLBACK_STYLE = 'margin:-6px 0 16px 0;font-size:13px;line-height:1.8;color:#666;word-break:break-all;'
SECTION_MAP = {
    '结论': '一、结论',
    '指数与市场情绪': '二、指数与市场情绪',
    '今日主线': '三、今日主线',
    '盘面理解': '四、盘面理解',
    '催化与后续观察': '五、催化与后续观察',
    '明日重点观察': '六、明日重点观察',
    '小五一句话收口': '七、小五一句话收口',
}


def render_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', escaped)
    def repl(match):
        url = match.group(1)
        safe = html.escape(url, quote=True)
        return f'<a href="{safe}">{safe}</a>'
    return URL_RE.sub(repl, escaped)


def maybe_link_block(line: str) -> str | None:
    m = URL_RE.search(line)
    if not m:
        return None
    url = m.group(1)
    prefix = line[:m.start()].strip()
    label = prefix[:-1].strip() if prefix.endswith('：') or prefix.endswith(':') else prefix
    label = html.escape(label or '原文链接')
    safe = html.escape(url, quote=True)
    main = f'<p style="{PARA_STYLE}">{label}：<a href="{safe}">{label}</a></p>'
    fallback = f'<p style="{LINK_FALLBACK_STYLE}">备用地址：{safe}</p>'
    return main + '\n' + fallback


def normalize_section_title(title: str) -> str:
    title = title.strip()
    return SECTION_MAP.get(title, title)


def render_markdown(text: str) -> str:
    parts = ['<section>']
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if m := TITLE_RE.match(line):
            parts.append(f'<p style="{TITLE_STYLE}">{html.escape(m.group(1))}</p>')
            continue
        if m := SECTION_RE.match(line):
            parts.append(f'<p style="{SECTION_STYLE}">{html.escape(normalize_section_title(m.group(1)))}</p>')
            continue
        if m := BOLD_LINE_RE.match(line):
            parts.append(f'<p style="{SECTION_STYLE}">{html.escape(normalize_section_title(m.group(1)))}</p>')
            continue
        if line.startswith('- '):
            maybe = maybe_link_block(line[2:].strip())
            if maybe:
                parts.append(maybe)
            else:
                parts.append(f'<p style="{LIST_STYLE}">• {render_inline(line[2:].strip())}</p>')
            continue
        maybe = maybe_link_block(line)
        if maybe:
            parts.append(maybe)
        else:
            parts.append(f'<p style="{PARA_STYLE}">{render_inline(line)}</p>')
    parts.append('</section>')
    return '\n'.join(parts) + '\n'


def main() -> int:
    parser = argparse.ArgumentParser(description='Render Xiaowu article markdown into WeChat-friendly HTML.')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    source = Path(args.input).read_text(encoding='utf-8')
    rendered = render_markdown(source)
    Path(args.output).write_text(rendered, encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
