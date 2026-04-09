from __future__ import annotations

from pathlib import Path
import html
import os
import re
import shutil

import markdown

ROOT = Path(__file__).resolve().parent
WIKI = ROOT / 'wiki'
INVENTORIES = ROOT / 'inventories'
SITE = ROOT / 'site'
SITE_PREFIX = os.environ.get('SITE_PREFIX', '').rstrip('/')

STYLE = """
:root {
  --bg: #f4f7fb;
  --panel: #ffffff;
  --ink: #17212b;
  --muted: #5c6b7a;
  --line: #d8e1ec;
  --accent: #183A63;
  --accent2: #285a8c;
  --sidebar-ink: #f5f9ff;
  --sidebar-muted: #c9dbf2;
}
body { font-family: Inter, Arial, sans-serif; margin: 0; background: var(--bg); color: var(--ink); }
.wrap { display: grid; grid-template-columns: 300px 1fr; min-height: 100vh; }
.sidebar { background: linear-gradient(180deg, var(--accent), #102945); color: var(--sidebar-ink); padding: 22px; position: sticky; top: 0; height: 100vh; overflow-y: auto; box-sizing: border-box; }
.sidebar a { color: #f2f7ff; text-decoration: none; }
.sidebar a:hover { color: #ffffff; text-decoration: underline; }
.sidebar ul { padding-left: 18px; margin-top: 6px; }
.sidebar h2, .sidebar h3 { color: #ffffff; }
.sidebar h2 { margin-top: 0; }
.main { padding: 28px; max-width: 1100px; }
.content { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; padding: 28px; box-shadow: 0 8px 30px rgba(14, 31, 53, 0.06); }
code { background: #eef3f8; padding: 2px 5px; border-radius: 4px; }
pre { background: #eef3f8; padding: 12px; overflow-x: auto; border-radius: 10px; }
a { color: var(--accent2); }
h1, h2, h3 { color: var(--accent); }
h1 { margin-top: 0; }
.small { color: var(--sidebar-muted); font-size: 14px; }
table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }
th, td { border: 1px solid var(--line); padding: 10px; text-align: left; vertical-align: top; }
th { background: #eef4fb; }
tr:nth-child(even) td { background: #fbfdff; }
blockquote { border-left: 4px solid #b8cae0; margin-left: 0; padding-left: 14px; color: var(--muted); }
.badge { display: inline-block; background: #e8f1fb; color: var(--accent); border: 1px solid #cfe0f4; border-radius: 999px; padding: 4px 10px; font-size: 12px; font-weight: 700; margin-bottom: 10px; }
.topbar { margin-bottom: 16px; color: var(--muted); font-size: 14px; }
.hero { background: linear-gradient(135deg, #eff5fc, #ffffff); border: 1px solid #d8e4f3; border-radius: 18px; padding: 28px; margin-bottom: 24px; }
.hero p { font-size: 17px; color: #304255; margin-bottom: 0; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin: 22px 0; }
.card { background: #fbfdff; border: 1px solid var(--line); border-radius: 14px; padding: 18px; }
.card h3 { margin-top: 0; margin-bottom: 8px; font-size: 18px; }
.card p { margin: 0 0 10px 0; color: #425466; }
.card a { font-weight: 600; }
.note { background: #f8fbff; border-left: 4px solid #8db4df; padding: 14px 16px; border-radius: 10px; color: #425466; }
@media (max-width: 900px) {
  .wrap { grid-template-columns: 1fr; }
  .sidebar { position: static; height: auto; }
  .main { padding: 14px; }
  .content { padding: 18px; }
  .hero { padding: 20px; }
}
"""


def site_href(path: str) -> str:
    path = path.lstrip('/')
    if SITE_PREFIX:
        return f"{SITE_PREFIX}/{path}"
    return f"/{path}"


def normalize_wiki_links(md_text: str, current_md: Path) -> str:
    def replace_obsidian(match):
        target = match.group(1)
        label = match.group(2) or target
        target_path = (current_md.parent / target).resolve()
        try:
            rel = target_path.relative_to(WIKI).with_suffix('.html')
            href = site_href(str(rel))
        except Exception:
            href = '#'
        return f'[{label}]({href})'

    def replace_md_links(match):
        label = match.group(1)
        target = match.group(2)
        if target.startswith('http://') or target.startswith('https://'):
            return match.group(0)
        if target.endswith('.md'):
            target_path = (current_md.parent / target).resolve()
            try:
                rel = target_path.relative_to(WIKI).with_suffix('.html')
                href = site_href(str(rel))
            except Exception:
                try:
                    rel = target_path.relative_to(ROOT).with_suffix('.html')
                    href = site_href(str(rel))
                except Exception:
                    href = target.replace('.md', '.html')
            return f'[{label}]({href})'
        return match.group(0)

    md_text = re.sub(r'\[\[([^\]|]+)\|?([^\]]+)?\]\]', replace_obsidian, md_text)
    md_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_md_links, md_text)
    return md_text


def md_to_html(md_text: str, current_md: Path) -> str:
    md_text = normalize_wiki_links(md_text, current_md)
    return markdown.markdown(md_text, extensions=['tables', 'fenced_code'])


def display_name_for_md(path: Path) -> str:
    text = path.read_text(errors='ignore')
    lines = text.splitlines()
    if lines and lines[0].strip() == '---':
        for line in lines[1:40]:
            if line.startswith('title:'):
                return line.split(':', 1)[1].strip().strip('"')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    return path.stem.replace('-', ' ').title()


def nav_html() -> str:
    sections = {
        'Programs': sorted((WIKI / 'programs').glob('*.md')),
        'Trials': sorted((WIKI / 'trials').glob('*.md')),
        'Queries': sorted((WIKI / 'queries').glob('*.md')),
        'Disputes': sorted((WIKI / 'disputes').glob('*.md')),
    }
    out = ["<h2>ClinPharm Vault</h2>", "<div class='small'>Source-first clinical pharmacology knowledge base</div>"]
    out.append(f"<p><a href='{site_href('index.html')}'>Home</a></p>")
    for title, files in sections.items():
        out.append(f"<h3>{html.escape(title)}</h3><ul>")
        for f in files:
            rel = f.relative_to(WIKI)
            href = str(rel).replace('.md', '.html')
            name = display_name_for_md(f)
            out.append(f"<li><a href='{site_href(href)}'>{html.escape(name)}</a></li>")
        out.append("</ul>")
    return ''.join(out)


def wrap_page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>{html.escape(title)}</title>
  <style>{STYLE}</style>
</head>
<body>
<div class='wrap'>
  <aside class='sidebar'>{nav_html()}</aside>
  <main class='main'>
    <div class='topbar'>Generated static export from Obsidian-friendly vault markdown</div>
    <div class='content'>
      <div class='badge'>ClinPharm Vault</div>
      {body}
    </div>
  </main>
</div>
</body>
</html>"""


def render_file(md_path: Path, base_dir: Path):
    rel = md_path.relative_to(base_dir)
    out = SITE / rel.with_suffix('.html')
    out.parent.mkdir(parents=True, exist_ok=True)
    text = md_path.read_text()
    html_body = md_to_html(text, md_path)
    title = text.splitlines()[0].lstrip('# ').strip() if text.strip() else md_path.stem
    out.write_text(wrap_page(title, html_body))


def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True, exist_ok=True)
    for md_path in WIKI.rglob('*.md'):
        if md_path.name == 'README.md':
            continue
        render_file(md_path, WIKI)
    for md_path in [INVENTORIES / 'source_registry.md', INVENTORIES / 'dispute_index.md']:
        if md_path.exists():
            render_file(md_path, ROOT)
    index_md = WIKI / 'index.md'
    if index_md.exists():
        render_file(index_md, WIKI)
    print(f'Built site at {SITE}')


if __name__ == '__main__':
    main()
