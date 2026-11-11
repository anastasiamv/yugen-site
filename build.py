#!/usr/bin/env python3
"""Генерирует статические страницы из src/<lang>/<page>.md.
Запуск: python3 build.py"""
import html, re, pathlib

ROOT = pathlib.Path(__file__).parent
LANGS = {
    "en": {"name": "English", "support": "Support", "privacy": "Privacy Policy", "terms": "Terms of Use",
           "sources": "Sources", "other": "ru", "other_label": "Русский"},
    "ru": {"name": "Русский", "support": "Поддержка", "privacy": "Политика конфиденциальности",
           "terms": "Условия использования", "sources": "Источники", "other": "en", "other_label": "English"},
}
PAGES = ["support", "privacy", "terms"]

CSS = """
:root{--bg:#fbfaf7;--fg:#1d1d1b;--muted:#6b6a64;--line:#e4e1d8;--link:#2f5d62}
@media (prefers-color-scheme:dark){:root{--bg:#141514;--fg:#ecebe6;--muted:#9a9990;--line:#2c2d2a;--link:#8fc1c4}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.65 -apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",Helvetica,Arial,sans-serif;-webkit-text-size-adjust:100%}
.wrap{max-width:680px;margin:0 auto;padding:28px 20px 64px}
header{display:flex;justify-content:space-between;align-items:baseline;padding-bottom:18px;border-bottom:1px solid var(--line);margin-bottom:32px}
header a{color:var(--fg);text-decoration:none}
.brand{font-size:20px;letter-spacing:.02em}
.lang{font-size:15px;color:var(--muted)}
.lang a{color:var(--muted)}
h1{font-size:30px;line-height:1.2;margin:0 0 20px;font-weight:600}
h2{font-size:21px;line-height:1.3;margin:36px 0 12px;font-weight:600}
p{margin:0 0 14px}
ul{margin:0 0 14px;padding-left:22px}
li{margin:0 0 6px}
a{color:var(--link)}
footer{margin-top:48px;padding-top:18px;border-top:1px solid var(--line);font-size:15px;color:var(--muted)}
footer a{color:var(--muted);margin-right:16px;white-space:nowrap}
"""

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"&lt;(https?://[^\s&]+)&gt;", r'<a href="\1">\1</a>', t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return t

def md(text):
    out, para, items = [], [], []
    def flush():
        nonlocal para, items
        if para: out.append("<p>%s</p>" % inline(" ".join(para))); para = []
        if items: out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(i) for i in items)); items = []
    for line in text.splitlines():
        s = line.rstrip()
        if not s: flush(); continue
        m = re.match(r"(#{1,2}) (.+?)(?: \{#([\w-]+)\})?$", s)
        if m:
            flush()
            lvl = len(m.group(1)); idattr = ' id="%s"' % m.group(3) if m.group(3) else ""
            out.append("<h%d%s>%s</h%d>" % (lvl, idattr, inline(m.group(2)), lvl)); continue
        if s.startswith("- "):
            if para: flush()
            items.append(s[2:]); continue
        if items: flush()
        para.append(s)
    flush()
    return "\n".join(out)

def page(lang, name, body):
    L = LANGS[lang]
    title = re.search(r"<h1>(.+?)</h1>", body).group(1)
    title = re.sub(r"<[^>]+>", "", title)
    other = L["other"]
    footer = "".join('<a href="../%s/">%s</a>' % (p, L[p]) for p in PAGES)
    footer += '<a href="../support/#sources">%s</a>' % L["sources"]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header><a class="brand" href="../../">Yūgen</a><span class="lang"><a href="../../{other}/{name}/">{L['other_label']}</a></span></header>
<main>
{body}
</main>
<footer>{footer}</footer>
</div>
</body>
</html>
"""

def main():
    for lang in LANGS:
        for name in PAGES:
            body = md((ROOT / "src" / lang / f"{name}.md").read_text(encoding="utf-8"))
            d = ROOT / lang / name; d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(page(lang, name, body), encoding="utf-8")
    links = "".join('<li><a href="%s/support/">%s</a></li>' % (l, v["name"]) for l, v in LANGS.items())
    (ROOT / "index.html").write_text(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Yūgen</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header><span class="brand">Yūgen</span></header>
<main>
<p>A map of places where you can see unusual natural and human phenomena.<br>Карта мест, где можно увидеть необычные природные и рукотворные явления.</p>
<ul>{links}</ul>
</main>
</div>
</body>
</html>
""", encoding="utf-8")

main()
